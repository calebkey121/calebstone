from src.Signal import Signal
from dataclasses import dataclass, field
from typing import Optional
from src.Effects import TimingWindow

class Card:
    def __init__(self, cost=-1, name=None, effect=None, text=None):
        self._cost = cost
        self._name = name
        self._effect = effect
        self._text = text or (effect.text if effect else "")
    
    def __repr__(self):
        return self._name

    def __eq__(self, other: 'Card') -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return (
            self._cost == other._cost and
            self._name == other._name and
            self._effect == other._effect and
            self._text == other._text
        )

class Ally(Card):
    def __init__(self, orig=None, cost=-1, name=None, attack=-1, health=-1, effect=None):
        if orig:
            super().__init__(orig._cost, orig._name, orig._effect, orig._text)
            self._attack = orig._attack
            self._maxHealth = orig._maxHealth
            self._health = orig._health
            self._ready = False
            # Copy the effect if it exists
            self._effect = orig._effect  # Effect objects are stateless, safe to share
        else:
            super().__init__(cost, name, effect)
            self._attack = attack
            self._maxHealth = health
            self._health = health
            self._ready = False
        
        # Initialize Signals
        self.on_death = Signal()  # Signal for when this ally dies
        self.on_attack = Signal() # Signal for when this ally attacks
        self.on_damage_dealt = Signal()  # Signal for when this ally deals damage
        self.on_damage_taken = Signal()  # Signal for when this ally takes damage
    
    def __eq__(self, other: 'Ally') -> bool:
        if not isinstance(other, Ally):
            return NotImplemented
        return (
            super().__eq__(other) and
            self._attack == other._attack and
            self._health == other._health and
            self._maxHealth == other._maxHealth and
            self._ready == other._ready
        )
    
    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, new_amount):
        change_amount = new_amount - self.health
        if change_amount >= 0:
            new_amount = min(new_amount, self._maxHealth)
            pass # Could add healing signal here if needed
        else:
            if new_amount <= 0:
                change_amount -= new_amount # even if they overkill, only register down to 0
                self.die()
            self.on_damage_taken.emit(-change_amount) # want real value of hp lost
        self._health = new_amount
    
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
    # Attack
    def attack(self, target):
        # for now lets just do total damage dealt
        self.on_attack.emit()
        self.on_damage_dealt.emit(min(self._attack, target.health))
        target.defend(self) # simple place to tell target to emit when its being attacked
        target.health -= self._attack
        self.health -= target._attack
        self.ready_down()

    
    def defend(self, attacker):
        self.on_damage_dealt.emit(min(self._attack, attacker.health))
    
    def die(self):
        self.on_death.emit(self)

    # Move this to health setter
    # def heal_damage(self, heal):
    #     if not isinstance(heal, int) or heal < 0:
    #         raise ValueError(f"Heal amount must be a positive integer. Got: {heal}")
    #     self._health += heal
    #     if self._health  > self._maxHealth:
    #         self._health = self._maxHealth

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
