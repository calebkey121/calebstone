from src.Player import Player
from enum import Enum, auto
from src.GameLogic import GameLogic

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
    def __init__(self, player1Hero, player1Deck, player2Hero, player2Deck):
        # Initialize base stats dictionary with hero-specific stats
        self.stats = {
            "player1": self.player_stats(),
            "player2": self.player_stats(),
        }

        # Create both players with all subscriber types
        self.player1 = Player(
            playerName="player1",
            heroName=player1Hero,
            deckList=player1Deck,
            ally_subscribers=self.create_ally_subscribers("player1"),
            player_subscribers=self.create_player_subscribers("player1"),
            hero_subscribers=self.create_hero_subscribers("player1")
        )
        
        self.player2 = Player(
            playerName="player2",
            heroName=player2Hero,
            deckList=player2Deck,
            ally_subscribers=self.create_ally_subscribers("player2"),
            player_subscribers=self.create_player_subscribers("player2"),
            hero_subscribers=self.create_hero_subscribers("player2")
        )

        self.current_player = None
        self.opponent_player = None
        self.turns = 0 # how many total turns have been taken?
        self.rounds = 0
        self.who_went_first = None

    def increment_stat(self, player, stat, amount=1):
        """Increment a stat for the given player by a specific amount."""
        self.stats[player][stat] += amount
    
    def player_stats(self):
        return {
            "gold_spent": 0,
            "gold_gained": 0,
            "income_gained": 0,
            "income_lost": 0,
            "damage_dealt_by_allies": 0,
            "total_attacks_by_allies": 0,
            # "allies_killed": 0, # redundant with allied_died
            "allies_died": 0,
            "allies_damage_taken": 0,
            "fatigue_damage": 0,
            "cards_played": 0,
            "hero_damage_taken": 0,
            "hero_damage_dealt": 0,
            "hero_attacks_made": 0,
            "hero_healing_received": 0,
            "total_healing_received": 0,  # Both hero and allies
            "hero_kills": 0  # When hero gets the killing blow
        }

    def create_hero_subscribers(self, player_id):
        """Create subscribers for hero-specific signals"""
        return {
            "on_death": [
                # Hero death might need special handling in the future
                lambda hero=None: None  # Placeholder for now
            ],
            "on_damage_taken": [
                lambda damage=0: self.increment_stat(player_id, "hero_damage_taken", damage)
            ],
            "on_heal": [
                lambda amount=0: self.increment_stat(player_id, "hero_healing_received", amount),
                lambda amount=0: self.increment_stat(player_id, "total_healing_received", amount)
            ],
            "on_attack": [
                lambda: self.increment_stat(player_id, "hero_attacks_made", 1)
            ],
            "on_damage_dealt": [
                lambda damage=0: self.increment_stat(player_id, "hero_damage_dealt", damage)
            ]
        }
    
    def create_ally_subscribers(self, player_id):
        """Create subscribers for ally-specific signals. Must be same name as Ally attributes (check Card.py)"""
        return {
            "on_death": [
                lambda card=None: self.increment_stat(player_id, "allies_died", 1)
            ],
            "on_attack": [
                lambda damage=None: self.increment_stat(player_id, "total_attacks_by_allies", 1)
            ],
            "on_damage_dealt": [
                lambda damage=0: self.increment_stat(player_id, "damage_dealt_by_allies", damage)
            ],
            "on_damage_taken": [
                lambda damage=0: self.increment_stat(player_id, "allies_damage_taken", damage)
            ]
        }
    
    def create_player_subscribers(self, player_id):
        """Create subscribers for player-specific signals"""
        return {
            "on_fatigue": [
                lambda damage=0: self.increment_stat(player_id, "fatigue_damage", damage)
            ],
            "on_card_played": [
                lambda card=None: self.increment_stat(player_id, "cards_played", 1)
            ],
            "on_gold_gained": [
                lambda amount=0: self.increment_stat(player_id, "gold_gained", amount)
            ],
            "on_gold_spent": [
                lambda amount=0: self.increment_stat(player_id, "gold_spent", amount)
            ],
            "on_income_gained": [
                lambda amount=0: self.increment_stat(player_id, "income_gained", amount)
            ],
            "on_income_lost": [
                lambda amount=0: self.increment_stat(player_id, "income_lost", amount)
            ]
        }

    
    def switch_turn(self):
        self.current_player, self.opponent_player = self.opponent_player, self.current_player
        self.turns += 1
        self.rounds = ( self.turns + 1 ) // 2
    
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
            self.round_count, self.turns
        ]
