from Card import Ally
from Card import Building
import DeckLists.effects as effects

# TODO: fix the way effects work man
Siege_Engineer = Ally(name="Siege Engineer", cost=1, attack=0, health=7, play_effect=effects.heal_hero, amount=[15], text="Heal your hero for 5 damage.")
Royal_Falconer = Ally(name="Royal Falconer", cost=2,  attack=6,  health=4, play_effect=effects.heal_all_allies, amount=[7], text="Heal all allies for 11 damage.") 
Wandering_Minstrel = Ally(name="Wandering Minstrel", cost=3, attack=5,  health=10, play_effect=effects.heal_all_allies, amount=[10], text="Heal all allies for 14 damage.")
Court_Alchemist = Ally(name="Court Alchemist", cost=4, attack=15, health=5, play_effect=effects.damage_enemy_hero, amount=[6], text="Deal 10 damage to the enemy hero.")
Mercenary_Captain = Ally(name="Mercenary Captain", cost=5,  attack=9, health=16, play_effect=effects.get_gold, amount=[3], text="Gain 3 gold.")
Village_Blacksmith = Ally(name="Village Blacksmith", cost=6, attack=4, health=26, play_effect=effects.get_income, amount=[2], text="Gain 2 income.")
Jousting_Champion = Ally(name="Jousting Champion", cost=7, attack=17, health=18, play_effect=effects.steal_gold, amount=[3], text="Steal 3 gold from opposing player.")
Dire_Wolf = Ally(name="Dire Wolf", cost=8, attack=25, health=15, play_effect=effects.draw_cards, amount=[2], text="Draw 2 cards.")
Castle_Ward = Ally(name="Castle Ward", cost=9, attack=13, health=32, play_effect=effects.draw_cards, amount=[2], text="Draw 2 cards.")
Highwaymans_Ambush = Ally(name="Highwayman's Ambush", cost=10, attack=11, health=39, play_effect=effects.damage_all_enemies, amount=[5], text="Deal 5 damage to all enemies.")
Bandit_Outlaw = Ally(name="Bandit Outlaw", cost=11, attack=23, health=27, play_effect=effects.steal_income, amount=[1], text="Steal 1 income from opposing player.")
Undead_Creatures = Ally(name="Undead Creatures", cost=12, attack=30,  health=30, play_effect=effects.damage_all_enemies, amount=[8], text="Deal 10 damage to all enemies.")
Highland_Scout = Ally(name="Highland Scout", cost=13, attack=40, health=25, play_effect=effects.draw_cards, amount=[3], text="Draw 3 cards.")
Bow_Marshal = Ally(name="Bow Marshal", cost=14, attack=35, health=35, play_effect=effects.damage_all_enemies, amount=[10], text="Deal 15 damage to all enemies.")
Forest_Guardian = Ally(name="Forest Guardian", cost=15, attack=15, health=60, play_effect=effects.heal_all_friendly_characters, amount=[50], text="Heal all friendly characters for 50 damage.")


# Not being used currently
Haunted_House = Building(name="Haunted House", cost=15, health=60, play_effect=effects.heal_all_friendly_characters, amount=[50], text="This is the text for a building")
Decrepit_Mansion = Building(name="Decrepit Mansion", cost=15, health=60, play_effect=effects.heal_all_friendly_characters, amount=[50], text="This is the text for a building")
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

# Hearthstones ratio

# Mana / Attack / Health
# 0 Mana: 1/1 (Duh)
# 1 Mana: 1.29/1.46
# 2 Mana: 1.87/2.41
# 3 Mana: 2.51/3.17
# 4 Mana: 3.18/3.84 Assuming Lightspawn has 5 Attack.
# 5 Mana: 3.91/4.87 Assuming Validated Doomsayer has 0 ATK and Lana'thel has 1 ATK.
# 6 Mana: 4.76/5.05
# 7 Mana: 5.53/6.09
# 8 Mana: 6.58/7.26
# 9 Mana: 5.83/8.39
# 10 Mana: 8.73/9.27

# Mana / Stats per mana
# 0 	infinity
# 1 	2.75
# 2 	2.14
# 3 	1.89
# 4 	1.76
# 5 	1.76
# 6 	1.64
# 7 	1.66
# 8 	1.73
# 9 	1.58
# 10 	1.8 
