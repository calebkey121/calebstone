from GameState import GameState
from Controller import RandomController, TerminalController
from OutputHandler import TerminalOutputHandler
from GameLogic import GameLogic
import DeckLists.PlayerOneList as p1d
import DeckLists.PlayerTwoList as p2d
import pprint

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
        self.start_game()
    
    def start_game(self):
        GameLogic.start_game(self.game_state)
        self.run_game

    def run_game(self):
        while not GameLogic.is_game_over(self.game_state):
            GameLogic.start_turn(self.game_state)
            # Display or log the result of the action
            
            current_controller = self.player1_controller if self.game_state.is_player1_turn() else self.player2_controller

            while ( action := current_controller.get_action(self.game_state) )["type"] != "end_turn":
                self.output_handler.display_action(action, self.game_state)
                GameLogic.process_turn(self.game_state, action)
                if GameLogic.is_game_over(self.game_state):
                    break

            GameLogic.end_turn(self.game_state)
            
        #self.output_handler.display_state(self.game_state) # move
        if self.game_state.player1.is_dead() and self.game_state.player2.is_dead():
            print("It's a tie!")
        elif self.game_state.player1.is_dead():
            print("Player 2 Wins!")
        else:
            print("Player 1 Wins!")
        stats = self.game_state.stats
        pprint.pprint(stats)
        player1_stats = stats['player1']
        player2_stats = stats['player2']

        for stat in player1_stats:
            value1 = player1_stats[stat]
            value2 = player2_stats[stat]

            if value1 > value2:
                diff = value1 - value2
                print(f"Player 1 had (+{diff}) {stat.replace('_', ' ')} ({value1} vs {value2})")
            elif value2 > value1:
                diff = value2 - value1
                print(f"Player 2 had (+{diff}) {stat.replace('_', ' ')} ({value2} vs {value1})")
            else:
                print(f"Both players had equal {stat.replace('_', ' ')} ({value1})")
    

def main():
    game = GameManager()
    game.run_game()

if __name__ == "__main__":
    main()
