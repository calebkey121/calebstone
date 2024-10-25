from config.GameSettings import *
import random
from Signal import Signal
from dataclasses import dataclass, field
from Effects import TimingWindow

# @dataclass
# class GameSignals:
#     """Core game flow signals"""
#     on_turn_end: Signal = field(default_factory=Signal)
#     on_turn_start: Signal = field(default_factory=Signal)
#     on_play_card: Signal = field(default_factory=Signal)
#     # Could add more timing windows later like:
#     # on_round_start, on_draw_card, etc.

class GameLogic():
    # def __init__(self):
    #     # Initialize game-wide signals
    #     self.signals = GameSignals()
    
    @staticmethod
    def process_turn(game_state, action):
        # Here the action is validated and applied to the game state
        current_player = game_state.current_player
        opponent = game_state.opponent_player
        
        # Resolve action depending on its type
        if action['type'] == 'play_card':
            card_index = action['card_index']
            if current_player.has_enough_gold(card_index):
                # Handle ON_PLAY effects immediately - direct call
                card = current_player._hand[card_index]
                current_player.play_ally(card)
                if card._effect and card._effect.timing == TimingWindow.ON_PLAY:
                    card._effect.execute(game_state, card)
                
                # Only subscribe death effects
                if card._effect and card._effect.timing == TimingWindow.ON_DEATH:
                    card.on_death.connect(
                        lambda source: card._effect.execute(game_state, source)
                    )
        
        elif action['type'] == 'attack':
            attacker = current_player.all_characters()[action['attacker_index']]
            target = opponent.all_characters()[action['target_index']]
            attacker.attack(target)
            # potential addl. attack resolution

        return game_state
    
    @staticmethod
    def is_game_over(game_state):
        # Check if either player's health has reached 0
        return game_state.player1.is_dead() or game_state.player2.is_dead()

    @staticmethod
    def start_game(game_state):
        if game_state.turn != 0 or game_state.current_player or game_state.opponent_player:
            raise ValueError("Tried starting the game on non turn zero")

        if random.choice([True, False]): # Coin Flip
            game_state.current_player = game_state.player1
            game_state.opponent_player = game_state.player2
        else:
            game_state.current_player = game_state.player2
            game_state.opponent_player = game_state.player1
        
        first_player = game_state.current_player
        game_state.who_went_first = first_player # useful info
        second_player = game_state.opponent_player
        
        # Give each player starting gold/income
        first_player.gold = GAME_START_GOLD_FIRST
        second_player.gold = GAME_START_GOLD_SECOND
        first_player.income = GAME_START_INCOME_FIRST
        second_player.income = GAME_START_INCOME_SECOND

        # Let each player draw cards
        first_player.draw_cards(GAME_START_CARDS_DRAWN_FIRST)
        second_player.draw_cards(GAME_START_CARDS_DRAWN_SECOND)

        game_state.turn += 1
    
    @staticmethod
    def end_turn(game_state):
        # Directly execute end turn effects - no signals needed
        for ally in game_state.current_player._army.get_army():
            if (ally._effect and 
                ally._effect.timing == TimingWindow.END_OF_TURN):
                ally._effect.execute(game_state, ally)
        if (game_state.round % X_ROUNDS) == 0:
            game_state.current_player.income += INCOME_PER_X_ROUNDS
        game_state.switch_turn()
    
    @staticmethod
    def start_turn(game_state):
        game_state.current_player.draw_card()
        game_state.current_player.ready_up()
        game_state.current_player.gold += game_state.current_player.income
