import pygame
import os # used to find avatar pictures in avatar directory
import settings
import Hero # used to type check for hero

class Card:
    def __init__(self, cost=-1, name=None):
        self._cost = cost
        self._name = name
        self._sprite = None # None until self.draw(x, y) is called, then a sprite is set at the appropriate spot on screen
        
        # If appropriate avatar is in directory then use it, otherwise use a default picture
        if os.path.exists(os.path.join("avatars", "cards", f"{self._name}.jpg")):
            image = pygame.image.load(os.path.join("avatars", "cards", f"{self._name}.jpg"))
        elif os.path.exists(os.path.join("avatars", "cards", f"{self._name}.png")):
            image = pygame.image.load(os.path.join("avatars", "cards", f"{self._name}.png"))
        else:
            image = pygame.image.load(os.path.join("avatars", "cards", "raccoon.jpg"))
        self._avatar = pygame.transform.scale(image, (settings.card_size[0], settings.card_size[1] - settings.sub_font.get_height() - settings.small_font.get_height()))

# GETTERS/SETTERS ********************************************************************************************
    def name(self, n=None):
        if isinstance(n, str):
            self._name = n
        return self._name

    def cost(self, c=None):
        if isinstance(c, int):
            self._cost = c
        return self._cost
# GETTERS/SETTERS ********************************************************************************************

    @staticmethod 
    def draw_card_back(WIN, x, y):
        x = pygame.Rect(x, y, settings.card_size[0], settings.card_size[1])
        pygame.draw.rect(WIN, settings.dark_grey, x) # BACKDROP
        pygame.draw.rect(WIN, settings.light_grey, x, settings.card_border_size)

class Ally(Card):
    def __init__(self, cost=-1, name=None, attack=-1, health=-1):
        super().__init__(cost, name)
        self._attack = attack
        self._health = health
        self._ready = False
        self._selected = False
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
# GETTERS/SETTERS ********************************************************************************************

    # Lower your own health by damage amount 
    def lower_health(self, damage):
        self._health -= damage

    # Ready Self
    def ready_up(self):
        self._ready = True
    def ready_down(self):
        self._ready = False
    def is_ready(self):
        return self._ready
    
    # Select Self
    def select(self):
        self._selected = True
    def unselect(self):
        self._selected = False

    # Attack enemy target
    # Parameters: 
    #   Enemy -> Ally or Hero type
    # Outcome:
    #   Deal appropriate damage to self and enemy
    # Return:
    #   None if successful, string if something went wrong
    def attack_enemy(self, enemy):

        # Type check, must be Ally or Hero
        if type(enemy != Ally and enemy != Hero):
            return f'Parameter is type {type(enemy)}, must be type Ally or Hero'

        if self.is_ready():
            if self.attack() >= 0:
                enemy.lower_health(self.attack())
            if enemy.attack() >= 0:
                self.lower_health(enemy.attack())
            self.ready_down()
        else:
            return f'{self.name()} is not ready!'
        return None


    # PYGAME Draw Ally
    def draw(self, WIN, x, y, yourTurn):

        WIN.blit(self._avatar, (x, y + settings.small_font.get_height()))
         # Stat Labels
        health_label = settings.sub_font.render(f"{self._health}", 1, settings.health_color) 
        attack_label = settings.sub_font.render(f"{self._attack}", 1, settings.attack_color) 
        
        # Stat Area
        health_border = pygame.Rect(x, y + settings.card_size[1] - settings.sub_font.get_height(), settings.card_size[0] / 2, settings.sub_font.get_height())
        attack_border = pygame.Rect(x + settings.card_size[0] / 2, y + settings.card_size[1] - settings.sub_font.get_height(), settings.card_size[0] / 2,  settings.sub_font.get_height())
        pygame.draw.rect(WIN, settings.dark_grey, health_border)
        pygame.draw.rect(WIN, settings.dark_grey, attack_border)
        pygame.draw.rect(WIN, settings.light_grey, health_border, settings.card_border_size)
        pygame.draw.rect(WIN, settings.light_grey, attack_border, settings.card_border_size)

        name_label = settings.sub_font.render(f"{self._name}", 1, settings.white) 
        name_rect = pygame.Rect(x, y, settings.card_size[0], settings.small_font.get_height())
        pygame.draw.rect(WIN, settings.dark_grey, name_rect)
        pygame.draw.rect(WIN, settings.light_grey, name_rect, 1)
        WIN.blit(name_label, (name_rect.center[0] - name_label.get_width() / 2, name_rect.center[1] - name_label.get_height() / 2))
        # Cost
        cost_label = settings.sub_font.render(f"{self._cost}", 1, settings.gold) 
        cost_rect = pygame.Rect(x + settings.card_size[0] - cost_label.get_width() - settings.card_border_size, y + settings.small_font.get_height(), cost_label.get_width(),  settings.small_font.get_height())
        pygame.draw.rect(WIN, settings.dark_grey, cost_rect)
        pygame.draw.rect(WIN, settings.light_grey, cost_rect, 1)
        WIN.blit(cost_label, (cost_rect.center[0] - cost_label.get_width() / 2, cost_rect.center[1] - cost_label.get_height() / 2))

        WIN.blit(health_label, (health_border.center[0] - health_label.get_width() / 2, health_border.center[1] - health_label.get_height() / 2))
        WIN.blit(attack_label, (attack_border.center[0] - attack_label.get_width() / 2, attack_border.center[1] - attack_label.get_height() / 2))
        
        # Ally Avatar
        # Final Border
        # Final Border
        finalBorderColor = settings.light_grey
        if self.is_ready() and yourTurn:
            finalBorderColor = settings.ready_color
        if self._selected and yourTurn:
            finalBorderColor = settings.selected_color
        if self._targeted:
            finalBorderColor = settings.targeted_color
        self._sprite = pygame.Rect(x, y, settings.card_size[0], settings.card_size[1])
        pygame.draw.rect(WIN, finalBorderColor, self._sprite, settings.card_border_size)