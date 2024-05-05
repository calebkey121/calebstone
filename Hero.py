import pygame
import os
import settings
from Army import Army
from Deck import Deck
from Card import Card

# This represents the player - Human or AI
class Hero:
    width = settings.hero_size[0]
    height = settings.hero_size[1]
    def __init__(self, **kwargs):
        # Heros are the player and hold all the variables that the player will have in game
        self._name = kwargs['hero']
        self._text = "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam"
        self._showText = False
        self._maxHealth = 200
        self._health = 200
        self._attack = 0
        self._gold = 0
        self._maxGold = 50
        self._income = 2

        self._deck = Deck(kwargs['deckList'])
        self._army = Army()
        self._hand = [] # hand is a part of Hero, not its own class
        self._maxHandSize = 10

        # If appropriate avatar is in directory then use it, otherwise use a default picture
        if os.path.exists(os.path.join("art", "heros", f"{self._name}.jpg")):
            self._image = pygame.image.load(os.path.join("art", "heros", f"{self._name}.jpg"))
        elif os.path.exists(os.path.join("art", "heros", f"{self._name}.png")):
            self._image = pygame.image.load(os.path.join("art", "heros", f"{self._name}.png"))
        else:
            self._image = pygame.image.load(os.path.join("art", "cards", "raccoon.jpg"))
        self._avatar = pygame.transform.scale(self._image, (Hero.width, Hero.height- settings.main_font.get_height() * 2))

        
        self._side1 = kwargs['side1'] # says if the hero is on the left or right side
        self._sprite = None
        self._ready = False
        self._targeted = False
        self._selected = False
        self._yourTurn = False # is it your turn

# GETTERS/SETTERS ********************************************************************************************
    def name(self, name=None):
        if name:
            self._name = name
        return self._name
    def health(self, health=None):
        if health:
            self._health = health
        return self._health
    def attack(self, attack=None):
        if attack:
            self._attack = attack
        return self._attack
    def gold(self, g=None):
        if g:
            self._gold = g
        return self._gold
    def income(self, i=None):
        if i:
            self._income = i
        return self._income
    def army(self, a=None):
        if a:  
            self._army = a
        return self._army.get_army()
    def text(self, t=None):
        if t:  
            self._text = t
        return self._text
    def hand(self, hand=None):
        if hand:
            self._hand = hand
        return self._hand
    def showText(self, showText=None):
        if showText != None:
            self._showText = showText
        return self._showText
# ************************************************************************************************************
# Ready ******************************************************************************************************
    def ready_up(self):
        if self._attack > 0:
            self._ready = True
        for card in self._army._army:
            card.ready_up()
    def ready_down(self):
        self._ready = False
    def should_target(self):
        if self._ready and self._selected:
            return True
        for ally in self.army():
            if ally.is_ready() and ally.is_selected():
                return True
        return False
# ************************************************************************************************************
# Selecting **************************************************************************************************
    def select(self):
        self._selected = True
    def unselect(self):
        self._selected = False
# ************************************************************************************************************
# Targeting **************************************************************************************************
    def target_all(self):
        self._targeted = True
        for ally in self._army.get_army():
            ally._targeted = True
    def untarget_all(self):
        self._targeted = False
        for ally in self._army.get_army():
            ally._targeted = False
# ************************************************************************************************************
# Hand *******************************************************************************************************
    def max_hand_size(self, newSize=None):
        if newSize:
            self._maxHandSize = newSize
        return self._maxHandSize

    def current_hand_size(self):
        return len(self._hand)

    def remove_from_hand(self, card):
        for i in self._hand:
            if i == card:
                self._hand.remove(i)

    def get_from_hand(self, position):
        return self._hand[position]

    def any_cards(self):
        if len(self._hand) > 0:
            return True
        else:
            return False

    def draw_card(self):
        # CASE: Your hand is NOT FULL
        if len(self._hand) < self.max_hand_size():
            # CASE: Out of Cards!! Take damage equal to the amount of cards that you have overdrawn
            if self._deck.get_current_num_cards() <= 0:
                damage = self._deck.draw_card(self._hand)
                self._health += damage
                #return (f'Fatigue: {-damage} damage delt to {self.name()}')
            else:
                self._deck.draw_card(self._hand)
                #return (self.name() + ' drew ' + draw.name() + '\n')
        # CASE: Your hand is FULL
        else:
            if self._deck.get_current_num_cards() > 0:
                self._deck.burn_card()
                #return (self._name + '\'s hand is too full!\n' + self._name + ' burned:' + self._deck.burn_card())
            else:
                damage = self._deck.draw_card(self._hand)
                self._health += damage

    def draw_cards(self, number):
        drawnCards = []
        for i in range(number):
            drawnCards.append(self.draw_card())
        return drawnCards

    def playable_cards(self): # Are there any playable cards in my hand?
        playable = False
        for i in self._hand:
            if i.cost() <= self._gold:
                playable = True
        return playable

    def playable_card(self, card):
        playable = False
        if card.cost() <= self.gold():
            playable = True
        return playable

    def playable_hand(self):
        playable = []
        for i in self._hand:
            if i.cost() <= self._gold:
                playable.append(i)
        return playable

    def in_hand(self, card):
        if card in self._hand:
            return True
        return False
# ************************************************************************************************************
# Army *******************************************************************************************************
    def call_to_arms(self, ally=None):
        if ally:
            self._army.add_ally(ally)
        return self._army

    def get_army_size(self):
        return self.call_to_arms().army_size()

    def play_ally(self, card, opposingPlayer):
        if not self._army.is_full() and card._cost <= self._gold:
            self._army.add_ally(card)
            card.ready_down()
            self._gold -= card.cost()
            self.remove_from_hand(card)

            # handle battlecry
            if card._playEffect:
                card._playEffect(amount=card._amount[0], player=self, opposingPlayer=opposingPlayer)
            self._army.toll_the_dead()
            opposingPlayer._army.toll_the_dead()
        else: return None # unsuccessful

    # Play building
    def play_building(self, card, opposingPlayer):
        print("pass")
        pass

    def available_targets(self): # attackable allies
        availableTargets = []
        availableTargets.append(self)
        for i in self._army._army:
            availableTargets.append(i)
        return availableTargets

    def available_attackers(self):
        available_attackers = []
        if (self._ready and (self._attack >= 0)):
            available_attackers.append(self)
        for i in self._army._army:
            if (i._ready and (i._attack > 0)):
                available_attackers.append(i)
        return available_attackers

    def in_army(self, ally):
        if self._army.in_army(ally):
            return True
        return False

# ************************************************************************************************************
# Battle *****************************************************************************************************
    def lower_health(self, attackVal):
        self._health -= attackVal

    def attack_enemy(self, enemy, attackingPlayer):
        if self._ready:
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

    def heal(self, healAmount):
        self._health += healAmount
        if self._health  > self._maxHealth:
            self._health = self._maxHealth

    def heal_allies(self, healAmount):
        for ally in self.army():
            ally.heal(healAmount)
        
# ************************************************************************************************************
# Gold *******************************************************************************************************
    def set_gold(self, roundNumber): # Players have a certain income, they earn that much gold per turn
        if (roundNumber % 3) == 0:
            self._income += 1
        self._gold += self._income
        if self._gold > self._maxGold: self._gold = self._maxGold

    def get_bounty(self, amount):
        self._gold += amount

    def change_income(self, amount):
        self._income += amount
        if self._income < 0:
            self._income = 0

    def steal_gold_from(self, opposingPlayer, amount):
        opposingPlayer._gold -= amount
        if opposingPlayer._gold < 0:
            stolenAmount = amount + opposingPlayer._gold # ex stealing 5, has 4 -> ._gold = -1: 5 + -1 = 4 (how much was actually stolen)
            opposingPlayer._gold = 0 # cant go below 0
        else:
            stolenAmount = amount
        self.get_bounty(stolenAmount)
    def steal_income_from(self, opposingPlayer, amount):
        if amount > 0 and opposingPlayer:
            opposingPlayer.change_income(-amount)
            if opposingPlayer._income < 0:
                stolenAmount = amount + opposingPlayer._income # ex stealing 5, has 4 -> ._gold = -1: 5 + -1 = 4 (how much was actually stolen)
                opposingPlayer._income = 0 # cant go below 0
            else:
                stolenAmount = amount
            self.change_income(stolenAmount)
        else:
            raise ValueError("Using Hero.steal_income_from incorrectly")

# ************************************************************************************************************
# PYGAME DRAW FUNCTIONS **************************************************************************************
    def draw(self, WIN):
        # X and Y
        x = settings.hero_zone_buffer
        if self._side1:
            y = settings.HEIGHT / 2 - settings.hero_zone_buffer - Hero.height
        else:
            y = settings.HEIGHT / 2 + settings.hero_zone_buffer

        # Stat Area
        # Player Health
        health_label = settings.main_font.render(f"{self._health}", 1, settings.health_color) 
        health_rect = pygame.Rect(x, y + Hero.height - health_label.get_height(), Hero.width / 2, health_label.get_height())
        pygame.draw.rect(WIN, settings.dark_grey, health_rect) # Backdrop
        pygame.draw.rect(WIN, settings.light_grey, health_rect, 5) # Border
        WIN.blit(health_label, (x + self._avatar.get_width() / 4 - health_label.get_width() / 2, y + Hero.height - settings.main_font.get_height()))

        # Player Attack
        attack_label = settings.main_font.render(f"{self._attack}", 1, settings.attack_color)
        attack_rect = pygame.Rect(x + Hero.width / 2, y + Hero.height - health_label.get_height(), Hero.width / 2, health_label.get_height())
        pygame.draw.rect(WIN, settings.dark_grey, attack_rect) # Backdrop
        pygame.draw.rect(WIN, settings.light_grey, attack_rect, settings.card_border_size) # Border
        WIN.blit(attack_label, (x + self._avatar.get_width() * 3 / 4 - attack_label.get_width() / 2, y + Hero.height - settings.main_font.get_height()))
        
        # Player Name
        name_label = settings.main_font.render(f"{self._name}", 1, settings.white)

        # Dynamically Lowers Font until the name fits
        fontSize = 35
        while name_label.get_width() >= Hero.width - 5:
            fontSize -= 1
            newFont = pygame.font.SysFont(settings.font_type, fontSize)
            name_label = newFont.render(f"{self._name}", 1, settings.white)
        # have to reset main avatar now that font has changed
        self._avatar = pygame.transform.scale(self._image, (Hero.width, Hero.height- settings.main_font.get_height() - name_label.get_height()))


        name_rect = pygame.Rect(x, y, Hero.width, name_label.get_height())
        pygame.draw.rect(WIN, settings.dark_grey, name_rect) # BACKDROP
        pygame.draw.rect(WIN, settings.light_grey, name_rect, settings.card_border_size) # BORDER
        WIN.blit(name_label, (x + Hero.width / 2 - name_label.get_width() / 2, y))
        
        # Players Avatar
        WIN.blit(self._avatar, (x, y + name_label.get_height()))
        # Final Border
        finalBorderColor = settings.light_grey
        if self._ready and self._yourTurn:
            finalBorderColor = settings.ready_color
        if self._selected:
            finalBorderColor = settings.selected_color
        if self._targeted:
            finalBorderColor = settings.targeted_color
        if self._side1:
            self._sprite = pygame.Rect(x, y, Hero.width, Hero.height)
        else:
            self._sprite = pygame.Rect(x, y, Hero.width, Hero.height)
        pygame.draw.rect(WIN, finalBorderColor, self._sprite, 5)

    def draw_army(self, WIN):
        # example to get the size of card and label
        if (self._side1):
            y = settings.HEIGHT / 2 - (settings.card_zone_buffer + Card.height)
        else: y = (settings.HEIGHT / 2) + settings.card_zone_buffer

        armySize = self.get_army_size()
        # left side is cut off, lets get that starting point
        starting_point = 2 * settings.hero_zone_buffer + self._avatar.get_width()
        middle = (settings.WIDTH + starting_point) / 2
        settings.card_buffer = 5

        x = middle - (Card.width / 2) * armySize
        x -= settings.card_buffer * (armySize - 1)
        for card in self._army.get_army():
            card.draw(WIN, x, y, self._yourTurn)
            x += card._avatar.get_width()
            x += settings.card_buffer * 2

    def draw_deck(self, WIN):

        if self._deck._deckList == []:
            pass 
            # deck is empty, display something saying that
        else: # deck is not empty
            x = settings.WIDTH - settings.card_zone_buffer - Card.width
            y = settings.card_zone_buffer
            if not self._side1:
                y = settings.HEIGHT - settings.card_zone_buffer - Card.height
            Card.draw_card_back(WIN, x, y)
        remaining_cards = settings.small_font.render(f"Remaining Cards:{self._deck.get_current_num_cards()}", 1, settings.black)
        WIN.blit(remaining_cards, (x + Card.width / 2 - remaining_cards.get_width() / 2, y + settings.card_buffer))

    def draw_hand(self, WIN, hidden=False):
        if self._hand == []:
            pass 
            # hand is empty, maybe display something saying that
        else: # hand is not empty
            x = settings.endHeroZone + settings.card_zone_buffer
            y = settings.card_zone_buffer
            focus = None
            if not self._side1:
                y = settings.HEIGHT - settings.card_zone_buffer - Card.height
            for card in self._hand:
                if card.showText(): # or card.is_selected()
                    focus = card
                    focusX, focusY = x, y
                if hidden:
                    Card.draw_card_back(WIN, x, y)
                else: card.draw(WIN, x, y, self._yourTurn)
                x += 49
            if focus:
                focus.draw(WIN, focusX, focusY, self._yourTurn)

    def draw_text_window(self, WIN):
        x = self._sprite.right
        y = self._sprite.y
        numLines = 0

        remainingWords = self._text.split(" ")
        remainingText = self._text
        text_pairs = []

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
