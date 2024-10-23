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
                # subscribe stats to track
                player = "player1" if game_state.is_player1_turn() else "player2"
                subscribers = [lambda card=None : game_state.increment_stat(player, "allies_died", 1)]
                current_player.play_card(card_index, subscribers)
        
        elif action['type'] == 'attack':
            attacker = current_player.all_characters()[action['attacker_index']]
            target = opponent.all_characters()[action['target_index']]
            target.take_damage(attacker._attack)
            attacker.take_damage(target._attack)
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
        
        first_player = game_state.current_player
        second_player = game_state.opponent_player
        
        # Set Signals
        pf, ps = ("player1", "player2") if first_player is game_state.player1 else ("player2", "player1")
        first_player.gold_gained.connect(lambda amount=0 : game_state.increment_stat(pf, "gold_gained", amount))
        first_player.gold_spent.connect(lambda amount=0 : game_state.increment_stat(pf, "gold_spent", amount))
        first_player.income_gained.connect(lambda amount=0 : game_state.increment_stat(pf, "income_gained", amount))
        first_player.income_lost.connect(lambda amount=0 : game_state.increment_stat(pf, "income_lost", amount))
        second_player.gold_gained.connect(lambda amount=0 : game_state.increment_stat(ps, "gold_gained", amount))
        second_player.gold_spent.connect(lambda amount=0 : game_state.increment_stat(ps, "gold_spent", amount))
        second_player.income_gained.connect(lambda amount=0 : game_state.increment_stat(ps, "income_gained", amount))
        second_player.income_lost.connect(lambda amount=0 : game_state.increment_stat(ps, "income_lost", amount))
        
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
        if (game_state.round % X_ROUNDS) == 0:
            game_state.current_player.income += INCOME_PER_X_ROUNDS
        game_state.switch_turn()
    
    @staticmethod
    def start_turn(game_state):
        game_state.current_player.draw_card()
        game_state.current_player.ready_up()
        game_state.current_player.gold += game_state.current_player.income
