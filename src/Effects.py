from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.GameState import GameState
    from src.Ally import Ally

class TimingWindow(Enum):
    ON_PLAY = "on_play"
    ON_DEATH = "on_death"
    END_OF_TURN = "end_of_turn"
    START_OF_TURN = "start_of_turn"
    ON_ATTACK = "on_attack"
    ON_DAMAGE_DEALT = "on_damage_dealt"
    ON_DAMAGE_TAKEN = "on_damage_taken"
    AFTER_ATTACK = "after_attack"
    ON_HEAL = "on_heal"
    ALWAYS = "always"

    @property
    def flavor_name(self):
        return {
            TimingWindow.ON_PLAY: "Battlecry",
            TimingWindow.ON_DEATH: "Toll of the Dead",
            TimingWindow.END_OF_TURN: "At end of turn",
            TimingWindow.START_OF_TURN: "At start of turn",
            TimingWindow.ON_ATTACK: "When attacking",
            TimingWindow.ON_DAMAGE_DEALT: "After dealing damage",
            TimingWindow.ON_DAMAGE_TAKEN: "After taking damage",
            TimingWindow.AFTER_ATTACK: "After attacking",
            TimingWindow.ON_HEAL: "After being healed",
            TimingWindow.ALWAYS: "Presence"
        }[self]

class Effect:
    def __init__(self, amount: list[int], timing: TimingWindow):
        self.amount = amount
        self.timing = timing
        self.text = self.generate_text()

    def __eq__(self, other: 'Effect') -> bool:
        if not isinstance(other, Effect):
            return NotImplemented
        return (
            self.amount == other.amount and
            self.timing == other.timing
        )

    def generate_text(self) -> str:
        """Generate effect text based on timing and amounts"""
        return f"{self.timing.flavor_name}: {self.effect_text}"

    @property
    def effect_text(self) -> str:
        """Should be overridden by child classes to provide specific effect text"""
        raise NotImplementedError

    def execute(self, game_state: 'GameState', source: 'Ally') -> 'GameState':
        """Execute the effect on the game state"""
        raise NotImplementedError

class GainGoldEffect(Effect):
    @property
    def effect_text(self) -> str:
        return f"Gain {self.amount[0]} gold"

    def execute(self, game_state: 'GameState', source: 'Ally') -> 'GameState':
        current_player = game_state.current_player
        current_player.gold += self.amount[0]
        return game_state

class GainIncomeEffect(Effect):
    @property
    def effect_text(self) -> str:
        return f"Gain {self.amount[0]} income"

    def execute(self, game_state: 'GameState', source: 'Ally') -> 'GameState':
        current_player = game_state.current_player
        current_player.income += self.amount[0]
        return game_state

class HealAllAlliesEffect(Effect):
    @property
    def effect_text(self) -> str:
        return f"Heal all allies for {self.amount[0]}"

    def execute(self, game_state: 'GameState', source: 'Ally') -> 'GameState':
        current_player = game_state.current_player
        for ally in current_player.army.allies:
            ally.heal(source=source, amount=self.amount[0])
        return game_state

class DamageEnemyHeroEffect(Effect):
    @property
    def effect_text(self) -> str:
        return f"Deal {self.amount[0]} damage to the enemy hero"

    def execute(self, game_state: 'GameState', source: 'Ally') -> 'GameState':
        opponent = game_state.opponent_player
        opponent.damage_hero(self.amount[0])
        return game_state

class DamageAllEnemiesEffect(Effect):
    @property
    def effect_text(self) -> str:
        return f"Deal {self.amount[0]} damage to all enemies"

    def execute(self, game_state: 'GameState', source: 'Ally') -> 'GameState':
        opponent = game_state.opponent_player
        for character in opponent.army.get_all():
            character.damage(source=source, amount=self.amount[0])
        return game_state

class DrawCardsEffect(Effect):
    @property
    def effect_text(self) -> str:
        return f"Draw {self.amount[0]} card{'s' if self.amount[0] > 1 else ''}"

    def execute(self, game_state: 'GameState', source: 'Ally') -> 'GameState':
        current_player = game_state.current_player
        current_player.draw_cards(self.amount[0])
        return game_state
