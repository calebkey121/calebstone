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
    ON_ATTACK = "on_attack" # before attack is started
    ON_DAMAGE_DEALT = "on_damage_dealt" # tougher, have to consider effects too
    ON_DAMAGE_TAKEN = "on_damage_taken" # a lot easier, just on health dropping
    AFTER_ATTACK = "after_attack" # after attack is resolved
    ON_HEAL = "on_heal"
    ALWAYS = "always"

class Effect:
    def __init__(self, amount: list[int], timing: TimingWindow, text: str):
        self.amount = amount
        self.timing = timing
        self.text = text

    def __eq__(self, other: 'Effect') -> bool:
        if not isinstance(other, Effect):
            return NotImplemented
        return (
            self.amount == other.amount and
            self.timing == other.timing and
            self.text == other.text
        )
    
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
# EFFECTS = {
#     # On Play Effects
#     "HEAL_5": HealAllAlliesEffect(
#         amount=[5],
#         timing=TimingWindow.ON_PLAY,
#         text="When played, heal all allies for 5 health"
#     ),
#     "DAMAGE_HERO_3": DamageEnemyHeroEffect(
#         amount=[3],
#         timing=TimingWindow.ON_PLAY,
#         text="When played, deal 3 damage to the enemy hero"
#     ),
#     
#     # On Death Effects
#     "DEATH_DAMAGE_2": DamageAllEnemiesEffect(
#         amount=[2],
#         timing=TimingWindow.ON_DEATH,
#         text="When this dies, deal 2 damage to all enemies"
#     ),
#     "DEATH_DRAW": DrawCardsEffect(
#         amount=[1],
#         timing=TimingWindow.ON_DEATH,
#         text="When this dies, draw a card"
#     ),
#     
#     # End of Turn Effects
#     "EOT_GOLD_1": GainGoldEffect(
#         amount=[1],
#         timing=TimingWindow.END_OF_TURN,
#         text="At the end of your turn, gain 1 gold"
#     ),
#     "EOT_INCOME_1": GainIncomeEffect(
#         amount=[1],
#         timing=TimingWindow.END_OF_TURN,
#         text="At the end of your turn, gain 1 income"
#     )
# }
# 
# # Example of how a card could be defined in JSON
# EXAMPLE_CARD_JSON = """
# {
#     "name": "Wealthy Merchant",
#     "cost": 4,
#     "attack": 2,
#     "health": 5,
#     "effect": "EOT_GOLD_1",
#     "timing": "END_OF_TURN"
# }
# """
