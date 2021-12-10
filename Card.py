import pygame
import os
import settings

class Card:
    def __init__(self, **kwargs):
        self._cost = kwargs['cost'] if 'cost' in kwargs else -1
        self._name = kwargs['name'] if 'name' in kwargs else 'No Name'
        self._avatar = pygame.transform.scale(pygame.image.load(os.path.join("avatars", "cards", self._name + ".png")), settings.card_size)
        self._ready = False

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
        if self._ready:
            if self.attack() >= 0:
                enemy.lower_health(self.attack())
            if enemy.attack() >= 0:
                self.lower_health(enemy.attack())
            self.ready_down()
        else:
            print(f'{self.name()} is not ready!')

    def draw(self, WIN, x, y, side1):
        # Ally Avatar
        WIN.blit(self._avatar, (x, y))

         # Stat Labels
        health_label = settings.sub_font.render(f"{self._health}", 1, (255,0,0)) # better way to choose rgb? is needed??
        attack_label = settings.sub_font.render(f"{self._attack}", 1, (255,188,0)) # better way to choose rgb? is needed??
        max_label = settings.sub_font.render(f"100", 1, (0,0,0)) # better way to choose rgb? is needed??
        
        # Stat Area
        health_border, attack_border = 0, 0
        if side1 == True:
            pygame.draw.rect(WIN, (30, 30, 30), (x + self._avatar.get_width(), y, max_label.get_width(), self._avatar.get_height())) # BACKDROP
            health_border = pygame.Rect(x + self._avatar.get_width(), y, max_label.get_width(), self._avatar.get_height() / 2) # BORDER health
            attack_border = pygame.Rect(x + self._avatar.get_width(), y + self._avatar.get_height() / 2, max_label.get_width(), self._avatar.get_height() / 2) # BORDER attack
        else:
            pygame.draw.rect(WIN, (30, 30, 30), (x - max_label.get_width(), y, max_label.get_width(), self._avatar.get_height())) # BACKDROP
            health_border = pygame.Rect(x - max_label.get_width(), y, max_label.get_width(), self._avatar.get_height() / 2) # BORDER health
            attack_border = pygame.Rect(x - max_label.get_width(), y + self._avatar.get_height() / 2, max_label.get_width(), self._avatar.get_height() / 2) # BORDER attack
        
        pygame.draw.rect(WIN, (200, 200, 200), health_border, 5) # BORDER health
        pygame.draw.rect(WIN, (200, 200, 200), attack_border, 5) # BORDER attack
        WIN.blit(health_label, (health_border.center[0] - health_label.get_width() / 2, health_border.center[1] - health_label.get_height() / 2))
        WIN.blit(attack_label, (attack_border.center[0] - attack_label.get_width() / 2, attack_border.center[1] - attack_label.get_height() / 2))
        
        # Final Border
        pygame.draw.rect(WIN, (255,255,255), (x, y, self._avatar.get_width(), self._avatar.get_height()), 5)

    # Representation - Weird String is me trying to make the output look cool
    def __repr__(self):
        return f'~__{self.name()}__~ \t\tCost: {self.cost():2d} \tAttack: {self.attack():2d} \tHealth: {self.health():2d}'