

class GameStatistics():
    def __init__(self):
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

    def create_hero_stat_subscribers(self, player_id):
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
    
    def create_ally_stat_subscribers(self, player_id):
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
    
    def create_player_stat_subscribers(self, player_id):
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