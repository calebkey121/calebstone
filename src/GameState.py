from src.Player import Player
from enum import Enum, auto
from src.GameLogic import GameLogic
from src.GameStatistics import GameStatistics

"""
Purpose:
    This class represents the current state of the game. It should hold everything you need to know about the game at a given point, including player states and the overall game flow (turns, rounds, etc.).
Responsibilities:
    Hold references to player states (self.player1, self.player2).
    Track game metadata like the round count and current turn.
    Provide helper methods to serialize the game state (e.g., converting it into a vector of integers for reinforcement learning or saving it).
Notes:
    Keep this class as a snapshot of the current game. It’s a container for the state but doesn’t control what happens (that’s the job of the GameManager).
    Probably extend it later with more attributes and helper methods as needed.
"""

class GameResult(Enum):
    IN_PROGRESS = auto()
    TIE = auto()
    PLAYER1_WIN = auto()
    PLAYER2_WIN = auto()

class GameState:
    def __init__(self, player1Hero, player1Deck, player2Hero, player2Deck, statistics=None):
        # Initialize base stats dictionary with hero-specific stats
        self.stats = statistics or GameStatistics()

        # Create both players with all subscriber types
        self.player1 = Player(
            playerName="player1",
            heroName=player1Hero,
            deckList=player1Deck,
            ally_subscribers=self.stats.create_ally_stat_subscribers("player1"),
            player_subscribers=self.stats.create_player_stat_subscribers("player1"),
            hero_subscribers=self.stats.create_hero_stat_subscribers("player1")
        )
        
        self.player2 = Player(
            playerName="player2",
            heroName=player2Hero,
            deckList=player2Deck,
            ally_subscribers=self.stats.create_ally_stat_subscribers("player2"),
            player_subscribers=self.stats.create_player_stat_subscribers("player2"),
            hero_subscribers=self.stats.create_hero_stat_subscribers("player2")
        )

        self.current_player = None
        self.opponent_player = None
        self.current_round = 0
        self.who_went_first = None
        self.total_turns = 0 # how many total turns have been taken?
        self.is_first_turn_of_round = True  # Track position within round

    
    def switch_turn(self):
        # Swap players
        self.current_player, self.opponent_player = self.opponent_player, self.current_player
        
        # Increment turn counter
        self.total_turns += 1
        
        # Update round tracking
        if self.is_first_turn_of_round:
            self.is_first_turn_of_round = False
        else:
            self.is_first_turn_of_round = True
            self.current_round += 1
    
    def is_player1_turn(self):
        return self.current_player is self.player1
    
    # Possible Actions
    def possible_cards_to_play(self):
        if self.current_player._army.is_full():
            return []
        actions = []
        playable_cards = self.current_player.playable_cards()
        for card in playable_cards:
            actions.append({
                "type": "play_card",
                "card_index": card
            })
        return actions
    
    def possible_attacks(self):
        actions = []
        attackers = self.current_player.available_attackers()
        targets = self.opponent_player.available_targets()
        for attacker in attackers:
            for target in targets:
                actions.append({
                    "type": "attack",
                    "attacker_index": attacker,
                    "target_index": target
                })
        return actions

    def possible_actions(self):
        actions = self.possible_cards_to_play() + self.possible_attacks()
        if not actions:
            actions.append({
                "type": "end_turn"
            })
        return actions
    # Possible Actions

    def get_result(self) -> GameResult:
        if not GameLogic.is_game_over(self):
            return GameResult.IN_PROGRESS
        
        if self.player1.is_dead() and self.player2.is_dead():
            return GameResult.TIE
        elif self.player1.is_dead():
            return GameResult.PLAYER2_WIN
        else:
            return GameResult.PLAYER1_WIN

    def to_vector(self):
        # Convert game state to vector (for ML or saving)
        return [
            self.player1.health, len(self.player1.hand), len(self.player1.army), 
            self.player2.health, len(self.player2.hand), len(self.player2.army),
            self.round_count, self.total_turns
        ]
