from abc import ABC, abstractmethod
import random
"""
Purpose:
    The controller takes in input from the player or AI and passes that information to the GameManager to process it. This class could also handle AI logic or reinforcement learning input depending on how the game is being played.
Responsibilities:
    Capture player input: Whether from a human or AI, the controller gathers actions (e.g., “play card X,” “attack with ally Y”).
    Pass actions to the GameManager for resolution.
    Can be extended to handle input from different sources (human player, AI agent, or RL agent).
Notes:
    This class should be extensible so that it can handle different types of inputs (e.g., human input, AI input, or input from a reinforcement learning algorithm).
    You can extend it later to handle multiple types of controllers (e.g., a human controller, an AI controller).
"""

class Controller(ABC):
    @abstractmethod
    def get_action(self, game_state):
        pass

class RandomController(Controller):
    def get_action(self, game_state):
        possible_actions = game_state.possible_actions()
        return random.choice(possible_actions)

class TerminalController(Controller):
    def get_action(self, game_state):
        current_player = game_state.current_player()
        print(f"Player {current_player.name}'s turn!")

        # Present action choices
        action_type = input("Choose an action (play_card, attack, end_turn): ").strip()
        
        if action_type == 'play_card':
            if current_player.hand:
                card_index = int(input(f"Choose a card (0 to {len(current_player.hand)-1}): "))
                return {'type': 'play_card', 'card_index': card_index}
        
        elif action_type == 'attack':
            if current_player.army and game_state.opponent().army:
                attacker_index = int(input(f"Choose attacker (0 to {len(current_player.army)-1}): "))
                target_index = int(input(f"Choose target (0 to {len(game_state.opponent().army)-1}): "))
                return {'type': 'attack', 'attacker_index': attacker_index, 'target_index': target_index}
        
        return {'type': 'end_turn'}
