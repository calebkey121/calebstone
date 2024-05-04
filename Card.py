import pygame
import os # used to find avatar pictures in avatar directory
import settings
import Hero # used to type check for hero

class Card:
    width = settings.card_size[0]
    height = settings.card_size[1]
    def __init__(self, cost=-1, name=None, text=None, showText = False, selected=False, play_effect=None, amount=None):
        self._cost = cost
        self._name = name
        self._text = text
        self._showText = showText # used when hovering over a card to read it's text
        self._selected = selected
        self._playEffect = play_effect
        self._amount = amount # a list of numbers for whatever the card is doing
        self._sprite = None # None until self.draw(x, y) is called, then a sprite is set at the appropriate spot on screen
        
        # If appropriate avatar is in directory then use it, otherwise use a default picture
        if os.path.exists(os.path.join("avatars", "cards", f"{self._name}.jpg")):
            self.image = pygame.image.load(os.path.join("avatars", "cards", f"{self._name}.jpg"))
        elif os.path.exists(os.path.join("avatars", "cards", f"{self._name}.png")):
            self.image = pygame.image.load(os.path.join("avatars", "cards", f"{self._name}.png"))
        else:
            self.image = pygame.image.load(os.path.join("avatars", "cards", "raccoon.jpg"))
        self._avatar = pygame.transform.scale(self.image, (Card.width, Card.height - settings.sub_font.get_height() - settings.small_font.get_height()))

# GETTERS/SETTERS ********************************************************************************************
    def name(self, n=None):
        if isinstance(n, str):
            self._name = n
        return self._name
    def cost(self, c=None):
        if isinstance(c, int):
            self._cost = c
        return self._cost
    def text(self, t=None):
        if isinstance(t, str):
            self._text = t
        return self._text
    def showText(self, b=None):
        if isinstance(b, bool):
            self._showText = b
        return self._showText
# ************************************************************************************************************
    @staticmethod 
    def draw_card_back(WIN, x, y):
        # may later want to add the option of drawing a specific cardback, dont really care rn, 
        # the cardback.png would be stored in the hero class attributes, as that is what calls draw_card_back
        image = pygame.image.load(os.path.join("avatars", "cardBacks", "cardBack.png"))
        avatar = pygame.transform.scale(image, (Card.width, Card.height))
        WIN.blit(avatar, (x, y))

        x = pygame.Rect(x, y, Card.width, Card.height)
        pygame.draw.rect(WIN, settings.light_grey, x, settings.card_border_size) # Border


class Ally(Card):
    def __init__(self, orig=None, cost=-1, name=None, attack=-1, health=-1, text=None, showText=False, selected=False, play_effect=None, amount=None):
        if orig:
            super().__init__(orig._cost, orig._name, orig._text, orig._showText, orig._selected, orig._playEffect, orig._amount)
            self._attack = orig._attack
            self._maxHealth = orig._maxHealth
            self._health = orig._health
            self._ready = False
            self._targeted = False
        else:
            super().__init__(cost, name, text, showText, selected, play_effect, amount)
            self._attack = attack
            self._maxHealth = health
            self._health = health
            self._ready = False
            self._targeted = False
        
# GETTERS/SETTERS ********************************************************************************************
    def attack(self, a=None):
        if isinstance(a, int):
            self._attack = a
        return self._attack

    def health(self, h=None):
        if isinstance(h, int):
            self._health = h
        return self._health
# ************************************************************************************************************
# READY ******************************************************************************************************
    def ready_up(self):
        if self._attack > 0:
            self._ready = True
    def ready_down(self):
        self._ready = False
    def is_ready(self):
        return self._ready
# ************************************************************************************************************
# Select *****************************************************************************************************
    def select(self):
        self._selected = True
    def unselect(self):
        self._selected = False
    def is_selected(self):
        return self._selected
# ************************************************************************************************************
# BATTLE *****************************************************************************************************
    # Lower your own health by damage amount 
    def lower_health(self, damage):
        self._health -= damage

    def heal(self, healAmount):
        self._health += healAmount
        if self._health  > self._maxHealth:
            self._health = self._maxHealth

    # Attack enemy target
    # Parameters: 
    #   Enemy -> Ally or Hero type
    # Outcome:
    #   Deal appropriate damage to self and enemy
    # Return:
    #   None if successful, string if something went wrong
    def attack_enemy(self, enemy, attackingPlayer):

        # Type check, must be Ally or Hero
        if type(enemy) != Ally and type(enemy) != Hero.Hero:
            return f'Parameter is type {type(enemy)}, must be type Ally or Hero'

        if self.is_ready():
            if self.attack() >= 0:
                enemy.lower_health(self.attack())
            if enemy.attack() >= 0:
                self.lower_health(enemy.attack())
            if enemy.health() < 0:
                enemy.health(0)
                attackingPlayer.get_bounty(2)
            self.ready_down()
        else:
            return f'{self.name()} is not ready!'
        return None
# ************************************************************************************************************
# PYGAME *****************************************************************************************************
    def draw(self, WIN, x, y, yourTurn):

        WIN.blit(self._avatar, (x, y + settings.small_font.get_height()))
         # Stat Labels
        health_label = settings.sub_font.render(f"{self._health}", 1, settings.health_color) 
        attack_label = settings.sub_font.render(f"{self._attack}", 1, settings.attack_color) 
        
        # Stat Area
        health_border = pygame.Rect(x, y + Card.height - settings.sub_font.get_height(), Card.width / 2, settings.sub_font.get_height())
        attack_border = pygame.Rect(x + Card.width / 2, y + Card.height - settings.sub_font.get_height(), Card.width / 2,  settings.sub_font.get_height())
        pygame.draw.rect(WIN, settings.dark_grey, health_border)
        pygame.draw.rect(WIN, settings.dark_grey, attack_border)
        pygame.draw.rect(WIN, settings.light_grey, health_border, settings.card_border_size)
        pygame.draw.rect(WIN, settings.light_grey, attack_border, settings.card_border_size)

        name_label = settings.sub_font.render(f"{self._name}", 1, settings.white) 

        # Dynamically Lowers Font until the name fits
        fontSize = 20
        while name_label.get_width() >= Card.width - 5:
            fontSize -= 1
            newFont = pygame.font.SysFont(settings.font_type, fontSize)
            name_label = newFont.render(f"{self._name}", 1, settings.white)
        # have to reset main avatar now that font has changed
        self._avatar = pygame.transform.scale(self.image, (Card.width, Card.height - settings.sub_font.get_height() - settings.small_font.get_height()))

        name_rect = pygame.Rect(x, y, Card.width, settings.small_font.get_height())
        pygame.draw.rect(WIN, settings.dark_grey, name_rect)
        pygame.draw.rect(WIN, settings.light_grey, name_rect, 1)
        WIN.blit(name_label, (name_rect.center[0] - name_label.get_width() / 2, name_rect.center[1] - name_label.get_height() / 2))
        # Cost
        cost_label = settings.sub_font.render(f"{self._cost}", 1, settings.gold) 
        cost_rect = pygame.Rect(x + settings.card_border_size, y + settings.small_font.get_height(), cost_label.get_width(),  settings.small_font.get_height())
        pygame.draw.rect(WIN, settings.dark_grey, cost_rect)
        pygame.draw.rect(WIN, settings.light_grey, cost_rect, 1)
        WIN.blit(cost_label, (cost_rect.center[0] - cost_label.get_width() / 2, cost_rect.center[1] - cost_label.get_height() / 2))

        WIN.blit(health_label, (health_border.center[0] - health_label.get_width() / 2, health_border.center[1] - health_label.get_height() / 2))
        WIN.blit(attack_label, (attack_border.center[0] - attack_label.get_width() / 2, attack_border.center[1] - attack_label.get_height() / 2))
        
        # Ally Avatar
        # Final Border
        finalBorderColor = settings.light_grey
        if self.is_ready() and yourTurn:
            finalBorderColor = settings.ready_color
        if self._selected:
            finalBorderColor = settings.selected_color
        if self._targeted:
            finalBorderColor = settings.targeted_color
        self._sprite = pygame.Rect(x, y, Card.width, Card.height)
        pygame.draw.rect(WIN, finalBorderColor, self._sprite, settings.card_border_size)

    def draw_text_window(self, WIN):
        x = self._sprite.right
        y = self._sprite.y
        # make sure we specify card type ALLY
        numLines = 1
        text_pairs = []
        text_label = settings.small_font.render("Ally", 1, settings.white)
        text_rect = pygame.Rect(x, y + ((numLines - 1) * settings.small_font.get_height()), text_label.get_width(), text_label.get_height())
        text_pairs.append((text_label, text_rect))

        remainingWords = self._text.split(" ")
        remainingText = self._text

        while (len(remainingWords) != 0): # while we still have words to write
            numLines += 1

            # check the length of the text and we'll see if it fits
            text_label = settings.small_font.render(remainingText, 1, settings.white, settings.dark_grey)

            # reset the index for our word list, and text string
            wordIdx = len(remainingWords) - 1
            strIdx = len(remainingText)

            # While the width of our text is greater than the desired width
            while text_label.get_width() > settings.text_box_width:
                # take away words from the end of the string, until they fit
                # strIdx goes to the end of the previous word
                strIdx -= len(remainingWords[wordIdx]) + 1 # + 1 accounts for the space
                wordIdx -= 1 # wordIdx goes to previous word
                checkText = remainingText[:strIdx]
                text_label = settings.small_font.render(checkText, 1, settings.white)
            
            text_rect = pygame.Rect(x, y + ((numLines - 1) * settings.small_font.get_height()), text_label.get_width(), text_label.get_height())
            text_pairs.append((text_label, text_rect))
            wordIdx += 1
            remainingWords = remainingWords[wordIdx:]
            remainingText = remainingText[strIdx + 1:]

        text_box_rect = pygame.Rect(x, y, settings.text_box_width + 5, text_label.get_height() * (numLines))
        pygame.draw.rect(WIN, settings.dark_grey, text_box_rect)
        for text_pair in text_pairs:
            WIN.blit(text_pair[0], text_pair[1])
        pygame.draw.rect(WIN, settings.white, text_box_rect, 1)
# ************************************************************************************************************

class Building(Card):
    def __init__(self, orig=None, cost=-1, name=None, health=-1, text=None, showText=False, selected=False, play_effect=None, amount=None):
        if orig:
            super().__init__(orig._cost, orig._name, orig._text, orig._showText, orig._selected, orig._playEffect, orig._amount)
            self._maxHealth = orig._maxHealth
            self._health = orig._health
            self._targeted = False
        else:
            super().__init__(cost, name, text, showText, selected, play_effect, amount)
            self._maxHealth = health
            self._health = health
            self._targeted = False
        
# GETTERS/SETTERS ********************************************************************************************
    def health(self, h=None):
        if isinstance(h, int):
            self._health = h
        return self._health
# ************************************************************************************************************
# Select *****************************************************************************************************
    def select(self):
        self._selected = True
    def unselect(self):
        self._selected = False
    def is_selected(self):
        return self._selected
# ************************************************************************************************************
# BATTLE *****************************************************************************************************
    # Lower your own health by damage amount 
    def lower_health(self, damage):
        self._health -= damage

    def heal(self, healAmount):
        self._health += healAmount
        if self._health  > self._maxHealth:
            self._health = self._maxHealth

# ************************************************************************************************************
# PYGAME *****************************************************************************************************
    def draw(self, WIN, x, y, yourTurn):

        WIN.blit(self._avatar, (x, y + settings.small_font.get_height()))
         # Stat Labels
        health_label = settings.sub_font.render(f"{self._health}", 1, settings.health_color) 
        
        # Stat Area
        health_border = pygame.Rect(x, y + Card.height - settings.sub_font.get_height(), Card.width, settings.sub_font.get_height())
        pygame.draw.rect(WIN, settings.dark_grey, health_border)
        pygame.draw.rect(WIN, settings.light_grey, health_border, settings.card_border_size)

        name_label = settings.sub_font.render(f"{self._name}", 1, settings.white) 

        # Dynamically Lowers Font until the name fits
        fontSize = 20
        while name_label.get_width() >= Card.width - 5:
            fontSize -= 1
            newFont = pygame.font.SysFont(settings.font_type, fontSize)
            name_label = newFont.render(f"{self._name}", 1, settings.white)
        # have to reset main avatar now that font has changed
        self._avatar = pygame.transform.scale(self.image, (Card.width, Card.height - settings.sub_font.get_height() - settings.small_font.get_height()))

        name_rect = pygame.Rect(x, y, Card.width, settings.small_font.get_height())
        pygame.draw.rect(WIN, settings.dark_grey, name_rect)
        pygame.draw.rect(WIN, settings.light_grey, name_rect, 1)
        WIN.blit(name_label, (name_rect.center[0] - name_label.get_width() / 2, name_rect.center[1] - name_label.get_height() / 2))
        # Cost
        cost_label = settings.sub_font.render(f"{self._cost}", 1, settings.gold) 
        cost_rect = pygame.Rect(x + settings.card_border_size, y + settings.small_font.get_height(), cost_label.get_width(),  settings.small_font.get_height())
        pygame.draw.rect(WIN, settings.dark_grey, cost_rect)
        pygame.draw.rect(WIN, settings.light_grey, cost_rect, 1)
        WIN.blit(cost_label, (cost_rect.center[0] - cost_label.get_width() / 2, cost_rect.center[1] - cost_label.get_height() / 2))

        WIN.blit(health_label, (health_border.center[0] - health_label.get_width() / 2, health_border.center[1] - health_label.get_height() / 2))
        
        # Ally Avatar
        # Final Border
        finalBorderColor = settings.light_grey
        if self._selected:
            finalBorderColor = settings.selected_color
        if self._targeted:
            finalBorderColor = settings.targeted_color
        self._sprite = pygame.Rect(x, y, Card.width, Card.height)
        pygame.draw.rect(WIN, finalBorderColor, self._sprite, settings.card_border_size)

    def draw_text_window(self, WIN):
        x = self._sprite.right
        y = self._sprite.y
        # make sure we specify card type BUILDING, dont need to! its its own subclass!
        numLines = 1
        text_pairs = []
        text_label = settings.small_font.render("Building", 1, settings.white)
        text_rect = pygame.Rect(x, y + ((numLines - 1) * settings.small_font.get_height()), text_label.get_width(), text_label.get_height())
        text_pairs.append((text_label, text_rect))

        remainingWords = self._text.split(" ")
        remainingText = self._text

        while (len(remainingWords) != 0): # while we still have words to write
            numLines += 1

            # check the length of the text and we'll see if it fits
            text_label = settings.small_font.render(remainingText, 1, settings.white, settings.dark_grey)

            # reset the index for our word list, and text string
            wordIdx = len(remainingWords) - 1
            strIdx = len(remainingText)

            # While the width of our text is greater than the desired width
            while text_label.get_width() > settings.text_box_width:
                # take away words from the end of the string, until they fit
                # strIdx goes to the end of the previous word
                strIdx -= len(remainingWords[wordIdx]) + 1 # + 1 accounts for the space
                wordIdx -= 1 # wordIdx goes to previous word
                checkText = remainingText[:strIdx]
                text_label = settings.small_font.render(checkText, 1, settings.white)
            
            text_rect = pygame.Rect(x, y + ((numLines - 1) * settings.small_font.get_height()), text_label.get_width(), text_label.get_height())
            text_pairs.append((text_label, text_rect))
            wordIdx += 1
            remainingWords = remainingWords[wordIdx:]
            remainingText = remainingText[strIdx + 1:]

        text_box_rect = pygame.Rect(x, y, settings.text_box_width + 5, text_label.get_height() * (numLines))
        pygame.draw.rect(WIN, settings.dark_grey, text_box_rect)
        for text_pair in text_pairs:
            WIN.blit(text_pair[0], text_pair[1])
        pygame.draw.rect(WIN, settings.white, text_box_rect, 1)
# ************************************************************************************************************
