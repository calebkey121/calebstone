import Hero # used to type check for hero
from Signal import Signal

class Card:
    def __init__(self, cost=-1, name=None, play_effect=None, amount=None, text=None):
        self._cost = cost
        self._name = name
        self._playEffect = play_effect
        self._text = text # description of playEffect
        self._amount = amount # a list of numbers for whatever the card is doing
    
    def __repr__(self):
        return self._name

class Ally(Card):
    def __init__(self, orig=None, cost=-1, name=None, attack=-1, health=-1, play_effect=None, amount=None, text=None):
        if orig:
            super().__init__(orig._cost, orig._name, orig._playEffect, orig._amount, orig._text)
            self._attack = orig._attack
            self._maxHealth = orig._maxHealth
            self._health = orig._health
            self._ready = False
        else:
            super().__init__(cost, name, play_effect, amount, text)
            self._attack = attack
            self._maxHealth = health
            self._health = health
            self._ready = False
        self.on_death = Signal()  # Signal for when this ally dies

    # READY
    def ready_up(self):
        if self._attack > 0:
            self._ready = True

    def ready_down(self):
        self._ready = False

    def is_ready(self):
        return self._ready
    
    def can_attack(self):
        return self._ready and self._attack > 0

    # BATTLE
    # Lower your own health by damage amount 
    def take_damage(self, damage):
        if not isinstance(damage, int) or damage < 0:
            raise ValueError(f"Damage must be a positive integer. Got: {damage}")
        self._health -= damage
        if self._health <= 0:
            self.die()
    
    def die(self):
        self.on_death.emit(self)

    def heal_damage(self, heal):
        if not isinstance(heal, int) or heal < 0:
            raise ValueError(f"Heal amount must be a positive integer. Got: {heal}")
        self._health += heal
        if self._health  > self._maxHealth:
            self._health = self._maxHealth

    # Attack enemy target
    # Parameters: 
    #   Enemy -> Ally or Hero type
    # Outcome:
    #   Deal appropriate damage to self and enemy
    # Return:
    #   None if successful, string if something went wrong
    # TODO: Move this out of card, to the game manager
    # def attack_enemy(self, enemy, attackingPlayer):
    #    # Type check, must be Ally or Hero
    #    if type(enemy) != Ally and type(enemy) != Hero.Hero:
    #        return f'Parameter is type {type(enemy)}, must be type Ally or Hero'
    #
    #    if self.is_ready():
    #        if self.attack() >= 0:
    #            enemy.lower_health(self.attack())
    #        if enemy.attack() >= 0:
    #            self.lower_health(enemy.attack())
    #        if enemy.health() < 0:
    #            enemy.health(0)
    #            attackingPlayer.get_bounty(2)
    #        self.ready_down()
    #    else:
    #        return f'{self.name()} is not ready!'
    #    return None

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
