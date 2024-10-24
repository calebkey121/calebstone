from dataclasses import dataclass
from enum import Enum
from typing import Optional, Callable, TYPE_CHECKING
if TYPE_CHECKING:
    import GameState
    from Card import Ally

class TimingWindow(Enum):
    ON_PLAY = "on_play"
    ON_DEATH = "on_death"
    END_OF_TURN = "end_of_turn"

class Effect:
    def __init__(self, amount: list[int], timing: TimingWindow, text: str):
        self.amount = amount
        self.timing = timing
        self.text = text
    
    def execute(self, game_state: 'GameState', source: 'Ally') -> 'GameState':
        """Execute the effect on the game state"""
        raise NotImplementedError

class GainGoldEffect(Effect):
    def execute(self, game_state: 'GameState', source: 'Ally') -> 'GameState':
        # Find the controlling player
        current_player = game_state.current_player
        # Apply effect
        current_player.gold += self.amount[0]
        return game_state

class GainIncomeEffect(Effect):
    def execute(self, game_state: 'GameState', source: 'Ally') -> 'GameState':
        # Find the controlling player
        current_player = game_state.current_player
        # Apply effect
        current_player.income += self.amount[0]
        return game_state

class HealAllAlliesEffect(Effect):
    def execute(self, game_state: 'GameState', source: 'Ally') -> 'GameState':
        # Get current player's army
        current_player = game_state.current_player
        # Heal all friendly allies
        current_player.heal_army(self.amount[0])
        return game_state

class DamageEnemyHeroEffect(Effect):
    def execute(self, game_state: 'GameState', source: 'Ally') -> 'GameState':
        # Damage enemy hero
        opponent = game_state.opponent_player
        opponent.damage_hero(self.amount[0])
        return game_state

class DamageAllEnemiesEffect(Effect):
    def execute(self, game_state: 'GameState', source: 'Ally') -> 'GameState':
        # Get opponent
        opponent = game_state.opponent_player
        opponent.damage_all(self.amount[0])
        return game_state

class DrawCardsEffect(Effect):
    def execute(self, game_state: 'GameState', source: 'Ally') -> 'GameState':
        # Find the controlling player
        current_player = game_state.current_player
        # Draw cards
        current_player.draw_cards(self.amount[0])
        return game_state

# Preset effects that can be used when creating cards
EFFECTS = {
    # On Play Effects
    "HEAL_5": HealAllAlliesEffect(
        amount=[5],
        timing=TimingWindow.ON_PLAY,
        text="When played, heal all allies for 5 health"
    ),
    "DAMAGE_HERO_3": DamageEnemyHeroEffect(
        amount=[3],
        timing=TimingWindow.ON_PLAY,
        text="When played, deal 3 damage to the enemy hero"
    ),
    
    # On Death Effects
    "DEATH_DAMAGE_2": DamageAllEnemiesEffect(
        amount=[2],
        timing=TimingWindow.ON_DEATH,
        text="When this dies, deal 2 damage to all enemies"
    ),
    "DEATH_DRAW": DrawCardsEffect(
        amount=[1],
        timing=TimingWindow.ON_DEATH,
        text="When this dies, draw a card"
    ),
    
    # End of Turn Effects
    "EOT_GOLD_1": GainGoldEffect(
        amount=[1],
        timing=TimingWindow.END_OF_TURN,
        text="At the end of your turn, gain 1 gold"
    ),
    "EOT_INCOME_1": GainIncomeEffect(
        amount=[1],
        timing=TimingWindow.END_OF_TURN,
        text="At the end of your turn, gain 1 income"
    )
}

# Example of how a card could be defined in JSON
EXAMPLE_CARD_JSON = """
{
    "name": "Wealthy Merchant",
    "cost": 4,
    "attack": 2,
    "health": 5,
    "effect": "EOT_GOLD_1",
    "timing": "END_OF_TURN"
}
"""