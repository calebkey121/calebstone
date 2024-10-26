# test_framework.py
from typing import Optional, List
from src.GameState import GameState
from src.Player import Player

class GameTestCase:
    def setUp(self):
        self.game_state = GameState(
            player1Hero="TestPlayer1",
            player2Hero="TestPlayer2",
            player1Deck=[],
            player2Deck=[]
        )
    
    def assert_player_state(self, player, expected_values: dict, message: str = ""):
        """Assert specific values for a player's state without comparing entire objects"""
        failures = []
        
        # Check hero state
        if 'hero_health' in expected_values:
            if player._hero.health != expected_values['hero_health']:
                failures.append(f"Hero health: expected {expected_values['hero_health']}, got {player._hero.health}")
        
        # Check resources
        if 'gold' in expected_values:
            if player.gold != expected_values['gold']:
                failures.append(f"Gold: expected {expected_values['gold']}, got {player.gold}")
        if 'income' in expected_values:
            if player.income != expected_values['income']:
                failures.append(f"Income: expected {expected_values['income']}, got {player.income}")
        
        # Check hand
        if 'hand' in expected_values:
            hand = expected_values['hand']
            if len(player._hand) != len(hand):
                failures.append(f"Hand size: expected {len(hand)}, got {len(player._hand)}")
            else:
                for i, (exp, actual) in enumerate(zip(hand, player._hand)):
                    if exp['name'] != actual._name:
                        failures.append(f"Hand card {i} name: expected {exp['name']}, got {actual._name}")
                    if 'health' in exp and exp['health'] != actual.health:
                        failures.append(f"Hand card {i} health: expected {exp['health']}, got {actual.health}")
                    if 'attack' in exp and exp['attack'] != actual._attack:
                        failures.append(f"Hand card {i} attack: expected {exp['attack']}, got {actual._attack}")
        
        # Check board state
        if 'board' in expected_values:
            board = expected_values['board']
            army = player._army.get_army()
            if len(army) != len(board):
                failures.append(f"Board size: expected {len(board)}, got {len(army)}")
            else:
                for i, (exp, actual) in enumerate(zip(board, army)):
                    if exp['name'] != actual._name:
                        failures.append(f"Board card {i} name: expected {exp['name']}, got {actual._name}")
                    if 'health' in exp and exp['health'] != actual.health:
                        failures.append(f"Board card {i} health: expected {exp['health']}, got {actual.health}")
                    if 'attack' in exp and exp['attack'] != actual._attack:
                        failures.append(f"Board card {i} attack: expected {exp['attack']}, got {actual._attack}")
        
        if failures:
            raise AssertionError(f"{message}\n" + "\n".join(failures))

    def create_player(self,
                     player_name: str = "Test Player",
                     hero_name: str = "Test Hero",
                     hero_health: int = 200,
                     gold: int = 0,
                     income: int = 0,
                     hand: List = None,
                     board: List = None,
                     deck_list: List = []) -> Player:
        """Creates a player with the specified state"""
        player = Player(
            playerName=player_name,
            heroName=hero_name,
            deckList=deck_list,
            player_subscribers=None,
            ally_subscribers=None,
            hero_subscribers=None
        )
        player._hero._health = hero_health
        player._gold = gold
        player._income = income
        player._hand = hand or []
        player._army._army = board or []
        player._army.set_army_size()
        
        # Set up any necessary signal connections
        for ally in player._army._army:
            ally.on_death.connect(player._army.toll_the_dead)
            ally.ready_up()
        
        return player
