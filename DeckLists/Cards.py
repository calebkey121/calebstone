from Card import Ally
from Card import Building
import DeckLists.effects as effects

Protected_Cub =       Ally(name="Protected Cub",       cost=1,  attack=0,  health=7,  play_effect=effects.heal_hero, amount=[15], text="Heal your hero for 5 damage.")
Wolf_Spirit   =       Ally(name="Wolf Spirit",         cost=2,  attack=6,  health=4,  play_effect=effects.heal_all_allies, amount=[7], text="Heal all allies for 11 damage.") 
Bear_Spirit   =       Ally(name="Bear Spirit",         cost=3,  attack=5,  health=10,  play_effect=effects.heal_all_allies, amount=[10], text="Heal all allies for 14 damage.")
Upset_Spirit  =       Ally(name="Upset Spirit",        cost=4,  attack=15,  health=5,  play_effect=effects.damage_enemy_hero, amount=[6], text="Deal 10 damage to the enemy hero.")
Forest_Spirit =       Ally(name="Forest Spirit",       cost=5,  attack=9, health=16,  play_effect=effects.get_gold, amount=[3], text="Gain 3 gold.")
Spider_Cart   =       Ally(name="Spider Cart",         cost=6,  attack=4,  health=26,  play_effect=effects.get_income, amount=[2], text="Gain 2 income.")
Haunted_Soul =        Ally(name="Haunted Soul",        cost=7,  attack=17,  health=18,  play_effect=effects.steal_gold, amount=[3], text="Steal 3 gold from opposing player.")
Dire_Wolf     =       Ally(name="Dire Wolf",           cost=8,  attack=25,  health=15,  play_effect=effects.draw_cards, amount=[2], text="Draw 2 cards.")
Alpha_Beast   =       Ally(name="Alpha Beast",         cost=9,  attack=13,  health=32, play_effect=effects.draw_cards, amount=[2], text="Draw 2 cards.")
Mother_Spider =       Ally(name="Mother Spider",       cost=10,  attack=11,  health=39, play_effect=effects.damage_all_enemies, amount=[5], text="Deal 5 damage to all enemies.")
Menacing_Presence =   Ally(name="Menacing Presence",   cost=11,  attack=23,  health=27, play_effect=effects.steal_income, amount=[1], text="Steal 1 income from opposing player.")
Undead_Creatures =    Ally(name="Undead Creatures",    cost=12,  attack=30,  health=30,  play_effect=effects.damage_all_enemies, amount=[8], text="Deal 10 damage to all enemies.")
Frost_Owl =           Ally(name="Frost Owl",           cost=13, attack=40,  health=25, play_effect=effects.draw_cards, amount=[3], text="Draw 3 cards.")
Spider_Giant =        Ally(name="Spider Giant",        cost=14, attack=35, health=35, play_effect=effects.damage_all_enemies, amount=[10], text="Deal 15 damage to all enemies.")
Guard_of_the_Forest = Ally(name="Guard of the Forest", cost=15,  attack=15,  health=60, play_effect=effects.heal_all_friendly_characters, amount=[50], text="Heal all friendly characters for 50 damage.")

Haunted_House =   Building(name="Haunted House",   cost=15, health=60, play_effect=effects.heal_all_friendly_characters, amount=[50], text="This is the text for a building")
Decrepit_Mansion =   Building(name="Decrepit Mansion",   cost=15, health=60, play_effect=effects.heal_all_friendly_characters, amount=[50], text="This is the text for a building")
Misty_Graveyard = Building(name="Misty Graveyard", cost=15, health=60, play_effect=effects.heal_all_friendly_characters, amount=[50], text="This is the text for a building")
Silent_Forest = Building(name="Silent Forest", cost=15, health=60, play_effect=effects.heal_all_friendly_characters, amount=[50], text="This is the text for a building")

# Play Effects
# damage_enemy_hero
# damage_all_enemies
# draw_cards
# heal_hero
# heal_all_allies
# heal_all_friendly_characters
# get_gold
# get_income
# steal_gold
# steal_income
# Gold to Stat Ratio (2.5)
# 1 : 5
# 2 : 10
# 3 : 15
# 4 : 20
# 5 : 25
# 6 : 30
# 7 : 35
# 8 : 40
# 9 : 45
#10 : 50
#11 : 55
#12 : 60
#13 : 65
#14 : 70
#15 : 75
#16 : 80