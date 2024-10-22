from GameState import GameState
from Controller import RandomController
from OutputHandler import TerminalOutputHandler
import DeckLists.PlayerOneList as p1d
import DeckLists.PlayerTwoList as p2d

"""
Purpose:
    This class manages the game flow and game logic. It controls what happens during a player’s turn and resolves interactions between players, allies, heroes, etc.
Responsibilities:
    Run the main game loop, switching between players and calling methods on GameState and the Player class.
    Resolve actions: When a player performs an action (play card, attack), the GameManager ensures it’s valid and calls the appropriate methods on the game state and players.
    Handle inter-player interactions (e.g., Player 1 attacking Player 2’s ally).
Notes:
    The GameManager orchestrates the game flow but doesn’t hold the game state directly (that’s the job of GameState).
    It interacts with the Player class and GameState to execute actions, but it doesn’t modify state directly—this is done via the player methods (play_card(), take_damage(), etc.).
"""
class GameManager:
    def __init__(self):
        self.game_state = GameState(player1Hero="Caleb", player2Hero="Dio", player1Deck=p1d.deck_list, player2Deck=p2d.deck_list)
        self.player1_controller = RandomController()
        self.player2_controller = RandomController()
        self.output_handler = TerminalOutputHandler()

    def run_game(self):
        while not self.is_game_over():
            current_controller = self.player1_controller if self.game_state.turn else self.player2_controller
            action = current_controller.get_action(self.game_state)

            # Process the action
            if action['type'] == 'end_turn':
                self.game_state.switch_turn()
                continue
            self.process_turn(action)
            
            # Display or log the result of the action
            self.output_handler.display_result(action, self.game_state)
        if self.game_state.player1.is_dead() and self.game_state.player2.is_dead():
            print("It's a tie!")
        elif self.game_state.player1.is_dead():
            print("Player 2 Wins!")
        else:
            print("Player 1 Wins!")

    def process_turn(self, action):
        # Here the action is validated and applied to the game state
        current_player = self.game_state.current_player()
        opponent = self.game_state.opponent()
        
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
            if target.health <= 0:
                opponent.toll_the_dead(target)
            if attacker.health <= 0:
                current_player.toll_the_dead(attacker)
    
    def setup_game(self):
        

    def is_game_over(self):
        # Check if either player's health has reached 0
        return self.game_state.player1.is_dead() or self.game_state.player2.is_dead()
    

def main():
    game = GameManager()
    game.run_game()

if __name__ == "__main__":
    main()
