# test_framework.py
from typing import Optional, List, TYPE_CHECKING
from src.GameState import GameState
from src.Player import Player
from src.Card import Ally

# test_framework.py
class GameTestCase:
    def setUp(self):
        self.game_state = GameState(
            player1Hero="TestPlayer1",
            player2Hero="TestPlayer2",
            player1Deck=[],
            player2Deck=[]
        )
    
    def assert_gamestate(self,
                        expected_player1: Optional[Player] = None,
                        expected_player2: Optional[Player] = None,
                        message: str = ""):
        if expected_player1:
            actual = self.game_state.player1
            if expected_player1 != actual:
                raise AssertionError(
                    f"Player 1 state mismatch. {message}\n"
                    f"{self._get_mismatch_details(expected_player1, actual)}"
                )
        
        if expected_player2:
            actual = self.game_state.player2
            if expected_player2 != actual:
                raise AssertionError(
                    f"Player 2 state mismatch. {message}\n"
                    f"{self._get_mismatch_details(expected_player2, actual)}"
                )
    
    def _get_mismatch_details(self, expected: Player, actual: Player) -> str:
        mismatches = []
        
        # Check hero
        if expected._hero != actual._hero:
            hero_diffs = []
            if expected._hero._health != actual._hero._health:
                hero_diffs.append(f"health: expected {expected._hero._health}, got {actual._hero._health}")
            if expected._hero._attack != actual._hero._attack:
                hero_diffs.append(f"attack: expected {expected._hero._attack}, got {actual._hero._attack}")
            if expected._hero._ready != actual._hero._ready:
                hero_diffs.append(f"ready: expected {expected._hero._ready}, got {actual._hero._ready}")
            mismatches.append(f"Hero mismatches: {', '.join(hero_diffs)}")
        
        # Check resources
        if expected._gold != actual._gold:
            mismatches.append(f"Gold: expected {expected._gold}, got {actual._gold}")
        if expected._income != actual._income:
            mismatches.append(f"Income: expected {expected._income}, got {actual._income}")
        
        # Check hand
        if len(expected._hand) != len(actual._hand):
            mismatches.append(f"Hand size: expected {len(expected._hand)}, got {len(actual._hand)}")
        else:
            hand_diffs = []
            for i, (exp_card, act_card) in enumerate(zip(expected._hand, actual._hand)):
                if exp_card != act_card:
                    card_diffs = []
                    if exp_card._health != act_card._health:
                        card_diffs.append(f"health: {exp_card._health} vs {act_card._health}")
                    if exp_card._attack != act_card._attack:
                        card_diffs.append(f"attack: {exp_card._attack} vs {act_card._attack}")
                    if exp_card._ready != act_card._ready:
                        card_diffs.append(f"ready: {exp_card._ready} vs {act_card._ready}")
                    hand_diffs.append(f"Card {i} ({exp_card._name}): {', '.join(card_diffs)}")
            if hand_diffs:
                mismatches.append(f"Hand mismatches:\n  " + "\n  ".join(hand_diffs))
        
        # Check board
        if len(expected._army._army) != len(actual._army._army):
            mismatches.append(f"Board size: expected {len(expected._army._army)}, got {len(actual._army._army)}")
        else:
            board_diffs = []
            for i, (exp_card, act_card) in enumerate(zip(expected._army._army, actual._army._army)):
                if exp_card != act_card:
                    card_diffs = []
                    if exp_card._health != act_card._health:
                        card_diffs.append(f"health: {exp_card._health} vs {act_card._health}")
                    if exp_card._attack != act_card._attack:
                        card_diffs.append(f"attack: {exp_card._attack} vs {act_card._attack}")
                    if exp_card._ready != act_card._ready:
                        card_diffs.append(f"ready: {exp_card._ready} vs {act_card._ready}")
                    board_diffs.append(f"Card {i} ({exp_card._name}): {', '.join(card_diffs)}")
            if board_diffs:
                mismatches.append(f"Board mismatches:\n  " + "\n  ".join(board_diffs))
        
        return "\n".join(mismatches)

    def create_player(self, 
                     hero_name: str = "Test Hero",
                     hero_health: int = 200,
                     gold: int = 0,
                     income: int = 0,
                     hand: List[Ally] = None,
                     board: List[Ally] = None) -> tuple[Player, Player]:
        """Creates two identical players - one for testing, one for expected state"""
        # Create test player
        test_player = Player(
            heroName=hero_name,
            deckList=[],
            player_subscribers=None,
            ally_subscribers=None,
            hero_subscribers=None
        )
        test_player._hero._health = hero_health
        test_player._gold = gold
        test_player._income = income
        test_player._hand = hand or []
        test_player._army._army = board or []
        test_player._army.set_army_size()

        for ally in test_player._army._army:
            ally.on_death.connect(test_player._army.toll_the_dead)
            ally.ready_up()


        # Create identical expected player
        expected_player = Player(
            heroName=hero_name,
            deckList=[],
            player_subscribers=None,
            ally_subscribers=None,
            hero_subscribers=None
        )
        expected_player._hero._health = hero_health
        expected_player._gold = gold
        expected_player._income = income
        expected_player._hand = hand.copy() if hand else []
        expected_player._army._army = board.copy() if board else []
        expected_player._army.set_army_size()

        for ally in expected_player._army._army:
            ally.on_death.connect(expected_player._army.toll_the_dead)
            ally.ready_up()
        
        return test_player, expected_player
