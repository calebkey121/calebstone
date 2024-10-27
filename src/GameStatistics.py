class GameStatistics():
    def __init__(self):
        self.stats = {
            "player1": self.player_stats(),
            "player2": self.player_stats(),
        }

    def increment_stat(self, player, stat, amount=1):
        self.stats[player][stat] += amount

    def player_stats(self):
        return {
            "gold_spent": 0,
            "gold_gained": 0,
            "income_gained": 0,
            "income_lost": 0,
            "damage_dealt_by_allies": 0,
            "total_attacks_by_allies": 0,
            "allies_died": 0,
            "allies_damage_taken": 0,
            "fatigue_damage": 0,
            "cards_played": 0,
            "hero_damage_taken": 0,
            "hero_damage_dealt": 0,
            "hero_attacks_made": 0,
            "hero_healing_received": 0,
            "total_healing_received": 0,
            "hero_kills": 0,
            "hero_extra_damage_taken": 0,
            "total_damage_taken": 0,
            "total_extra_damage_taken": 0,
            "hero_extra_damage_dealt": 0,
            "total_damage_dealt": 0,
            "total_extra_damage_dealt": 0,
            "hero_attacks_endured": 0,
            "hero_overhealing_received": 0,
            "damage_extra_dealt_by_allies": 0,
            "total_overhealing_received": 0,
            "allied_attacks_endured": 0
        }

    def create_hero_stat_subscribers(self, player_id):
        """Create subscribers for hero-specific signals"""
        return {
            "on_heal_received": [
                lambda data: (
                    self.increment_stat(player_id, "hero_healing_received", data.effective_heal),
                    self.increment_stat(player_id, "total_healing_received", data.effective_heal),
                    self.increment_stat(player_id, "hero_overhealing_received", data.extra_heal),
                    self.increment_stat(player_id, "total_overhealing_received", data.extra_heal),
                )
            ],
            "on_damage_taken": [
                lambda data: self.increment_stat(player_id, "hero_damage_taken", data.effective_damage),
                lambda data: self.increment_stat(player_id, "hero_extra_damage_taken", data.extra_damage),
                lambda data: self.increment_stat(player_id, "total_damage_taken", data.effective_damage),
                lambda data: self.increment_stat(player_id, "total_extra_damage_taken", data.extra_damage),
            ],
            "on_damage_dealt": [
                lambda data: self.increment_stat(player_id, "hero_damage_dealt", data.effective_damage),
                lambda data: self.increment_stat(player_id, "hero_extra_damage_dealt", data.extra_damage),
                lambda data: self.increment_stat(player_id, "total_damage_dealt", data.effective_damage),
                lambda data: self.increment_stat(player_id, "total_extra_damage_dealt", data.extra_damage),
            ],
            "on_attack": [
                lambda data: self.increment_stat(player_id, "hero_attacks_made", 1)
            ],
            "on_attacked": [
                lambda data: self.increment_stat(player_id, "hero_attacks_endured", 1)
            ],
        }

    def create_ally_stat_subscribers(self, player_id):
        return {
            "on_death": [
                lambda data: self.increment_stat(player_id, "allies_died", 1)
            ],
            "on_heal_received": [
                lambda data: (
                    self.increment_stat(player_id, "hero_healing_received", data.effective_heal),
                    self.increment_stat(player_id, "total_healing_received", data.effective_heal),
                    self.increment_stat(player_id, "hero_overhealing_received", data.extra_heal),
                    self.increment_stat(player_id, "total_overhealing_received", data.extra_heal),
                )
            ],
            "on_attack": [
                lambda data: self.increment_stat(player_id, "total_attacks_by_allies", 1)
            ],
            "on_attacked": [
                lambda data: self.increment_stat(player_id, "allied_attacks_endured", 1)
            ],
            "on_damage_dealt": [
                lambda data: self.increment_stat(player_id, "damage_dealt_by_allies", data.effective_damage),
                lambda data: self.increment_stat(player_id, "damage_extra_dealt_by_allies", data.extra_damage),
                lambda data: self.increment_stat(player_id, "total_damage_dealt", data.effective_damage),
                lambda data: self.increment_stat(player_id, "total_extra_damage_dealt", data.extra_damage),
            ],
            "on_damage_taken": [
                lambda data: self.increment_stat(player_id, "allies_damage_taken", data.effective_damage)
            ]
        }

    def create_player_stat_subscribers(self, player_id):
        return {
            "on_fatigue": [
                lambda data: self.increment_stat(player_id, "fatigue_damage", data.damage)
            ],
            "on_card_played": [
                lambda data: self.increment_stat(player_id, "cards_played", 1)
            ],
            "on_gold_gained": [
                lambda data: self.increment_stat(player_id, "gold_gained", data.amount)
            ],
            "on_gold_spent": [
                lambda data: self.increment_stat(player_id, "gold_spent", data.amount)
            ],
            "on_income_gained": [
                lambda data: self.increment_stat(player_id, "income_gained", data.amount)
            ],
            "on_income_lost": [
                lambda data: self.increment_stat(player_id, "income_lost", data.amount)
            ]
        }
