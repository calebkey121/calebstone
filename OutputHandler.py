from abc import ABC, abstractmethod

class OutputHandler(ABC):
    @abstractmethod
    def display_result(self, action, game_state):
        pass

class TerminalOutputHandler(OutputHandler):
    def display_result(self, action, game_state):
        current_player = game_state.current_player()
        if action['type'] == 'play_card':
            card = current_player.hand[action['card_index']]
            print(f"{current_player.name} played {card.name}")
        elif action['type'] == 'attack':
            attacker = current_player.army[action['attacker_index']]
            target = game_state.opponent().army[action['target_index']]
            print(f"{current_player.name}'s {attacker.name} attacked {target.name}")
        self.print_state(game_state)
    
    def print_state(game_state):
        # Get Player 1's status
        player1_hero_status = game_state.player1.get_hero_status()
        player1_army_status = game_state.player1.get_army_status()
        player1_hand_status = game_state.player1.get_hand_status()

        # Get Player 2's status
        player2_hero_status = game_state.player2.get_hero_status()
        player2_army_status = game_state.player2.get_army_status()
        player2_hand_status = game_state.player2.get_hand_status()

        # Display Player 1's Status
        print("\nPlayer 1's Hero:")
        print(f"Hero: {player1_hero_status['name']} | Attack: {player1_hero_status['attack']} | Health: {player1_hero_status['health']}")
        
        print("\nPlayer 1's Army:")
        if player1_army_status:
            for i, ally in enumerate(player1_army_status):
                print(f"Ally {i+1}: {ally['name']} | Attack: {ally['attack']} | Health: {ally['health']} | Cost: {ally['cost']}")
        else:
            print("No allies on the field.")

        print("\nPlayer 1's Hand:")
        if player1_hand_status:
            for i, card in enumerate(player1_hand_status):
                print(f"Card {i+1}: {card['name']} | Attack: {card['attack']} | Health: {card['health']} | Cost: {card['cost']}")
        else:
            print("No cards in hand.")

        # Display Player 2's Status
        print("\nPlayer 2's Hero:")
        print(f"Hero: {player2_hero_status['name']} | Attack: {player2_hero_status['attack']} | Health: {player2_hero_status['health']}")
        
        print("\nPlayer 2's Army:")
        if player2_army_status:
            for i, ally in enumerate(player2_army_status):
                print(f"Ally {i+1}: {ally['name']} | Attack: {ally['attack']} | Health: {ally['health']} | Cost: {ally['cost']}")
        else:
            print("No allies on the field.")

        print("\nPlayer 2's Hand:")
        if player2_hand_status:
            for i, card in enumerate(player2_hand_status):
                print(f"Card {i+1}: {card['name']} | Attack: {card['attack']} | Health: {card['health']} | Cost: {card['cost']}")
        else:
            print("No cards in hand.")

class LogFileOutputHandler(OutputHandler):
    def __init__(self, log_file):
        self.log_file = log_file

    def display_result(self, action, game_state):
        with open(self.log_file, 'a') as file:
            current_player = game_state.current_player()
            if action['type'] == 'play_card':
                card = current_player.hand[action['card_index']]
                file.write(f"{current_player.name} played {card.name}\n")
            elif action['type'] == 'attack':
                attacker = current_player.army[action['attacker_index']]
                target = game_state.opponent().army[action['target_index']]
                file.write(f"{current_player.name}'s {attacker.name} attacked {target.name}\n")
            file.write(f"Player 1 health: {game_state.player1.health}, Player 2 health: {game_state.player2.health}\n")

class NoOutputHandler(OutputHandler):
    def display_result(self, action, game_state):
        pass  # Do nothing
