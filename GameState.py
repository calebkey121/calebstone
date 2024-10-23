from Player import Player

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
class GameState:
    def __init__(self, player1Hero, player1Deck, player2Hero, player2Deck):
        self.player1 = Player(heroName=player1Hero, deckList=player1Deck)
        self.player2 = Player(heroName=player2Hero, deckList=player2Deck)
        self.current_player = None
        self.opponent_player = None
        self.turn = 0 # how many total turns have been taken?
        self.round = self.turn // 2 # round is how many turns a player has taken
        self.stats = {
            "player1": self.player_stats(),
            "player2": self.player_stats(),
        }

    def increment_stat(self, player, stat, amount=1):
        """Increment a stat for the given player by a specific amount."""
        self.stats[player][stat] += amount
    
    def player_stats(self):
        return {
            "gold_spent": 0,
            "gold_gained": 0,
            "income_gained": 0,
            "income_lost": 0,
            "damage_dealt_by_allies": 0, # rn all damage is from allies
            "total_attacks_by_allies": 0,
            "hero_damage_taken": 0,
            "allies_damage_taken": 0,
            "allies_killed": 0,
            "allies_died": 0,
            "fatigue_damage": 0,
            "cards_played": 0
        }
    
    def switch_turn(self):
        self.current_player, self.opponent_player = self.opponent_player, self.current_player
        self.turn += 1
    
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

    def to_vector(self):
        # Convert game state to vector (for ML or saving)
        return [
            self.player1.health, len(self.player1.hand), len(self.player1.army), 
            self.player2.health, len(self.player2.hand), len(self.player2.army),
            self.round_count, self.turn
        ]
