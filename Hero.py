from config.GameSettings import *

class Hero:
    def __init__(self, heroName):
        self._name = heroName
        self._maxHealth = HERO_MAX_HEALTH
        self._health = HERO_STARTING_HEALTH
        self._attack = 0
        self._ready = False

    def name(self, name=None):
        if name:
            self._name = name
        return self._name
    def maxHealth(self, maxHealth=None):
        if maxHealth:
            self._maxHealth = maxHealth
        return self._maxHealth
    def health(self, health=None):
        if health:
            self._health = health
        return self._health
    def attack(self, attack=None):
        if attack:
            self._attack = attack
        return self._attack
    
    @property
    def attack(self):
        return self._attack
    @attack.setter
    def attack(self, a):
        if isinstance(a, int) and a >= 0:
            self._attack = a
        return self._attack
    
    # Helpers
    def can_attack(self):
        return self._ready and self._attack > 0

    # Hero Actions
    def take_damage(self, damage):
        if not isinstance(damage, int):
            raise ValueError(f"Damage must be an integer. Got: {damage}")
        if damage > 0:
            self.health -= damage
    
    def heal_damage(self, heal):
        if not isinstance(heal, int):
            raise ValueError(f"Heal amount must be an integer. Got: {heal}")
        if heal > 0:
            self.health += heal
    
    def ready_up(self):
        if self._attack > 0:
            self._ready = True
    
    def ready_down(self):
        self._ready = False # yes i know this can be one function with ready_up, i like it this way
    

