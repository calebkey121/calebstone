from config.GameSettings import *

class Hero:
    def __init__(self, heroName):
        self._name = heroName
        self._maxHealth = HERO_MAX_HEALTH
        self._health = HERO_STARTING_HEALTH
        self._attack = 0
        self._ready = False
    
    @property
    def health(self):
        return self._health
    @health.setter
    def health(self, new_amount):
        change_amount = new_amount - self.health
        if change_amount >= 0:
            pass # self.on_heal.emit(change_amount)
        else:
            pass # self.on_damage.emit(change_amount)
        self._health = new_amount
    
    # Helpers
    def can_attack(self):
        return self._ready and self._attack > 0
    
    def ready_up(self):
        if self._attack > 0:
            self._ready = True
    
    def ready_down(self):
        self._ready = False
    
    def defend(self, attacker):
        pass # might want to emit stuff once hero is actually attacking
