import pygame
import os
import settings

class Card:
    @staticmethod 
    def draw_card_back(WIN, x, y):
        x = pygame.Rect(x, y, settings.card_size[0], settings.card_size[1])
        pygame.draw.rect(WIN, settings.dark_grey, x) # BACKDROP
        pygame.draw.rect(WIN, settings.light_grey, x, settings.card_border_size)

    def __init__(self, **kwargs):
        self._cost = kwargs['cost'] if 'cost' in kwargs else -1
        self._name = kwargs['name'] if 'name' in kwargs else 'No Name'
        self._avatar = pygame.transform.scale(pygame.image.load(os.path.join("avatars", "cards", "raccoon.jpg")), (settings.card_size[0], settings.card_size[1] - settings.sub_font.get_height() - settings.small_font.get_height()))
        self._sprite = None

    def name(self, name=None):
        if name:
            self._name = name
        return self._name

    def cost(self, cost=None):
        if cost:
            self._cost = cost
        return self._cost


    # def __repr__(self):
    #     return f'
    #     Card: {self.name()}
    #     Cost: {self.cost()}
    #     '
        

class Ally(Card):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._attack = kwargs['attack'] if 'attack' in kwargs else 0
        self._health = kwargs['health'] if 'health' in kwargs else 0
        self._ready = False
        self._selected = False
        self._targeted = False
        

    def attack(self, a=None):
        if a:
            self._attack = a
        return self._attack

    def health(self, h=None):
        if isinstance(h, int):
            self._health = h
        return self._health

    def lower_health(self, attackVal):
        self._health -= attackVal

    def ready_up(self):
        self._ready = True

    def ready_down(self):
        self._ready = False

    def is_ready(self):
        return self._ready

    def attack_enemy(self, enemy):
        if self.is_ready():
            if self.attack() >= 0:
                enemy.lower_health(self.attack())
            if enemy.attack() >= 0:
                self.lower_health(enemy.attack())
            self.ready_down()
        else:
            print(f'{self.name()} is not ready!')

    def select(self):
        self._selected = True
    
    def unselect(self):
        self._selected = False

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