from config.GameSettings import *
import random

class GameLogic():
    @staticmethod
    def process_turn(game_state, action):
        # Here the action is validated and applied to the game state
        current_player = game_state.current_player
        opponent = game_state.opponent_player
        
        # Resolve action depending on its type
        if action['type'] == 'play_card':
            card_index = action['card_index']
            if current_player.has_enough_gold(card_index):
                current_player.play_card(card_index)
        
        elif action['type'] == 'attack':
            attacker = current_player.all_characters()[action['attacker_index']]
            target = opponent.all_characters()[action['target_index']]
            target.take_damage(attacker._attack)
            attacker.take_damage(target._attack)
            if target._health <= 0:
                opponent.toll_the_dead()
            if attacker._health <= 0:
                current_player.toll_the_dead()
            attacker.ready_down()
        
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
        
        # Give each player starting gold/income
        game_state.current_player._gold = GAME_START_GOLD_FIRST
        game_state.opponent_player._gold = GAME_START_GOLD_LAST
        game_state.current_player._income = GAME_START_INCOME_FIRST
        game_state.opponent_player._income = GAME_START_INCOME_LAST

        # Let each player draw cards
        game_state.current_player.draw_cards(GAME_START_CARDS_DRAWN_FIRST)
        game_state.opponent_player.draw_cards(GAME_START_CARDS_DRAWN_LAST)

        game_state.turn += 1
    
    @staticmethod
    def end_turn(game_state):
        if (game_state.round % X_ROUNDS) == 0:
            game_state.current_player._income += INCOME_PER_X_ROUNDS
        game_state.switch_turn()
    
    @staticmethod
    def start_turn(game_state):
        game_state.current_player.draw_card()
        game_state.current_player.ready_up()
        game_state.current_player._gold += game_state.current_player._income
