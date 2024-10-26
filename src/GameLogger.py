from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime
import uuid
import json

@dataclass
class GameLog:
    """Represents a single game's worth of statistics and events"""
    game_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    
    # Game Overview
    winner: Optional[str] = None
    first_player: Optional[str] = None
    total_turns: int = 0
    
    # Card Play Stats
    cards_played_by_cost: Dict[int, int] = field(default_factory=dict)
    
    # Economy Stats
    gold_by_turn: Dict[str, List[int]] = field(default_factory=lambda: {"player1": [], "player2": []})
    income_by_turn: Dict[str, List[int]] = field(default_factory=lambda: {"player1": [], "player2": []})
    
    # Combat Stats
    damage_dealt: Dict[str, Dict[str, int]] = field(default_factory=lambda: {
        "player1": {"hero": 0, "allies": 0, "effects": 0, "fatigue": 0},
        "player2": {"hero": 0, "allies": 0, "effects": 0, "fatigue": 0}
    })
    
    def to_dict(self) -> dict:
        """Convert the game log to a dictionary for serialization"""
        return {
            "game_id": self.game_id,
            "timestamp": self.timestamp.isoformat(),
            "winner": self.winner,
            "first_player": self.first_player,
            "total_turns": self.total_turns,
            "cards_played_by_cost": self.cards_played_by_cost,
            "gold_by_turn": self.gold_by_turn,
            "income_by_turn": self.income_by_turn,
            "damage_dealt": self.damage_dealt
        }

class GameLogger:
    def __init__(self, log_file: Optional[str] = None):
        self.current_game: Optional[GameLog] = None
        self.completed_games: List[GameLog] = []
        self.log_file = log_file
    
    def start_game(self, game_state) -> None:
        """Initialize logging for a new game"""
        self.current_game = GameLog(
            first_player=game_state.who_went_first._name
        )
        
        # Subscribe to player signals
        for player_id, player in [("player1", game_state.player1), ("player2", game_state.player2)]:
            # Gold/Income signals
            player.signals.on_gold_gained.connect(
                lambda amount, pid=player_id: self._on_gold_gained(pid, amount)
            )
            player.signals.on_gold_spent.connect(
                lambda amount, pid=player_id: self._on_gold_spent(pid, amount)
            )
            player.signals.on_income_gained.connect(
                lambda amount, pid=player_id: self._on_income_gained(pid, amount)
            )
            player.signals.on_card_played.connect(
                lambda card, pid=player_id: self._on_card_played(pid, card)
            )
            player.signals.on_fatigue.connect(
                lambda damage, pid=player_id: self._on_fatigue_damage(pid, damage)
            )
            
            # Hero signals
            player._hero.signals.on_damage_taken.connect(
                lambda damage, pid=player_id: self._on_hero_damage(pid, damage)
            )
    
    def end_game(self, game_state) -> None:
        """Finalize logging for the current game"""
        if game_state.get_result().name == "TIE":
            self.current_game.winner = "tie"
        else:
            self.current_game.winner = "player1" if game_state.get_result().name == "PLAYER1_WIN" else "player2"
        
        self.current_game.total_turns = game_state.total_turns
        
        # Store final gold/income values
        for player_id, player in [("player1", game_state.player1), ("player2", game_state.player2)]:
            self.current_game.gold_by_turn[player_id].append(player.gold)
            self.current_game.income_by_turn[player_id].append(player.income)
        
        self.completed_games.append(self.current_game)
        
        if self.log_file:
            self._write_to_file()
        
        self.current_game = None
    
    def _on_card_played(self, player_id: str, card) -> None:
        """Track card play statistics"""
        cost = card._cost
        self.current_game.cards_played_by_cost[cost] = \
            self.current_game.cards_played_by_cost.get(cost, 0) + 1
    
    def _on_gold_gained(self, player_id: str, amount: int) -> None:
        """Track gold gained"""
        self.current_game.gold_by_turn[player_id].append(amount)
    
    def _on_gold_spent(self, player_id: str, amount: int) -> None:
        """Track gold spent"""
        self.current_game.gold_by_turn[player_id].append(-amount)
    
    def _on_income_gained(self, player_id: str, amount: int) -> None:
        """Track income changes"""
        self.current_game.income_by_turn[player_id].append(amount)
    
    def _on_hero_damage(self, player_id: str, damage: int) -> None:
        """Track hero damage taken"""
        self.current_game.damage_dealt[player_id]["hero"] += damage
    
    def _on_fatigue_damage(self, player_id: str, damage: int) -> None:
        """Track fatigue damage"""
        self.current_game.damage_dealt[player_id]["fatigue"] += damage
    
    def _write_to_file(self) -> None:
        """Write completed game to log file"""
        if not self.log_file:
            return
            
        game_data = self.current_game.to_dict()
        with open(self.log_file, 'a') as f:
            json.dump(game_data, f)
            f.write('\n')  # One game per line
    
    def get_summary_stats(self) -> dict:
        """Generate summary statistics across all completed games"""
        if not self.completed_games:
            return {}
            
        total_games = len(self.completed_games)
        wins = {"player1": 0, "player2": 0, "tie": 0}
        total_turns = 0
        total_rounds = 0
        first_player_wins = 0
        
        for game in self.completed_games:
            wins[game.winner] += 1
            total_turns += game.total_turns
            total_rounds += ( game.total_turns + 1 ) // 2
            if game.winner == game.first_player:
                first_player_wins += 1
        
        return {
            "total_games": total_games,
            "win_rates": {
                "player1": (wins["player1"] / total_games) * 100,
                "player2": (wins["player2"] / total_games) * 100,
                "ties": (wins["tie"] / total_games) * 100
            },
            "first_player_winrate": (first_player_wins / total_games) * 100,
            "average_game_length": total_turns / total_games,
            "average_num_rounds": total_rounds / total_games
        }
