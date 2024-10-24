from config.GameSettings import *
from Signal import Signal
from dataclasses import dataclass, field

@dataclass
class HeroSignals:
    """Signals owned by the hero"""
    on_death: Signal = field(default_factory=Signal)
    on_damage_taken: Signal = field(default_factory=Signal)
    on_heal: Signal = field(default_factory=Signal)
    on_attack: Signal = field(default_factory=Signal)
    on_damage_dealt: Signal = field(default_factory=Signal)

class Hero:
    def __init__(self, heroName, hero_subscribers: dict = None):
        self._name = heroName
        self._maxHealth = HERO_MAX_HEALTH
        self._health = HERO_STARTING_HEALTH
        self._attack = 0
        self._ready = False
        
        # Initialize signals
        self.signals = HeroSignals()
        
        # Connect hero-level subscribers if provided
        if hero_subscribers:
            for signal_name, callbacks in hero_subscribers.items():
                if hasattr(self.signals, signal_name):
                    signal = getattr(self.signals, signal_name)
                    signal.connect(callbacks)
    
    @property
    def health(self):
        return self._health
        
    @health.setter
    def health(self, new_amount):
        change_amount = new_amount - self.health
        if change_amount >= 0:
            self.signals.on_heal.emit(change_amount)
        else:
            if new_amount <= 0:
                change_amount -= new_amount  # even if they overkill, only register down to 0
                self.signals.on_death.emit(self)
            self.signals.on_damage_taken.emit(-change_amount)  # want real value of hp lost
        self._health = max(0, new_amount)  # Prevent negative health
    
    # Helpers
    def can_attack(self):
        return self._ready and self._attack > 0
    
    def ready_up(self):
        if self._attack > 0:
            self._ready = True
    
    def ready_down(self):
        self._ready = False
    
    def attack(self, target):
        if not self.can_attack():
            raise ValueError("Hero cannot attack right now")
            
        self.signals.on_attack.emit()
        damage_dealt = min(self._attack, target.health)
        self.signals.on_damage_dealt.emit(damage_dealt)
        
        target.defend(self)
        target.health -= self._attack
        self.health -= target._attack  # Counterattack damage
        self.ready_down()
    
    def defend(self, attacker):
        if self._attack > 0:  # Only emit damage dealt if hero can actually deal damage
            damage_dealt = min(self._attack, attacker.health)
            self.signals.on_damage_dealt.emit(damage_dealt)
