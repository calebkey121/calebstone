from Hero import Hero

# god... we need to redo play_effects, make it a class come on

# Damage *****************************************************************************************************
# Card Text: Deal X damage to the enemy hero.
def damage_enemy_hero(amount: int, player: Hero=None, opposingPlayer: Hero=None):
    if opposingPlayer:
        opposingPlayer.lower_health(amount)
# Card Text: Deal X damage to all enemies.
def damage_all_enemies(amount: int, player: Hero=None, opposingPlayer: Hero=None):
    if opposingPlayer:
        opposingPlayer.lower_health(amount)
        for ally in opposingPlayer.army():
            ally.lower_health(amount)
# ************************************************************************************************************
# Card Draw **************************************************************************************************
# Card Text: Draw X cards.
def draw_cards(amount: int, player: Hero=None, opposingPlayer: Hero=None):
    if player:
        player.draw_cards(amount)
# ************************************************************************************************************
# Healing ****************************************************************************************************
# Card Text: Heal your hero for X damage.
def heal_hero(amount: int, player: Hero=None, opposingPlayer: Hero=None):
    if player:
        player.heal(amount)
# Card Text: Heal all allies for X damage.
def heal_all_allies(amount: int, player: Hero=None, opposingPlayer: Hero=None):
    if player:
        player.heal_allies(amount)
# Card Text: Heal all friendly characters for X damage.
def heal_all_friendly_characters(amount: int, player: Hero=None, opposingPlayer: Hero=None):
    if player:
        player.heal(amount)
        player.heal_allies(amount)
# ************************************************************************************************************
# Gold *******************************************************************************************************
# Card Text: Gain X gold.
def get_gold(amount: int, player: Hero=None, opposingPlayer: Hero=None):
    if player:
        player.get_bounty(amount)
# Card Text: Gain X income.
def get_income(amount: int, player: Hero=None, opposingPlayer: Hero=None):
    if player:
        player.change_income(amount)
# Card Text: Steal X gold from the other player.
def steal_gold(amount: int, player: Hero=None, opposingPlayer: Hero=None):
    if opposingPlayer and player:
        player.steal_gold_from(opposingPlayer=opposingPlayer, amount=amount)
# Card Text: Steal X income from the other player.
def steal_income(amount: int, player: Hero=None, opposingPlayer: Hero=None):
    if opposingPlayer and player:
        player.steal_income_from(opposingPlayer=opposingPlayer, amount=amount)
# ************************************************************************************************************
