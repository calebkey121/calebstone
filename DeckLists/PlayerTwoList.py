from Cards import CARD_CATALOG
from Ally import Ally

# Keep the deck composition definition as is
DECK_COMPOSITION = {
    "SIEGE_ENGINEER": 3,
    "ROYAL_FALCONER": 3,
    "WANDERING_MINSTREL": 3,
    "COURT_ALCHEMIST": 3,
    "MERCENARY_CAPTAIN": 3,
    "VILLAGE_BLACKSMITH": 3,
    "JOUSTING_CHAMPION": 3,
    "DIRE_WOLF": 3,
    "CASTLE_WARD": 3,
    "HIGHWAYMANS_AMBUSH": 3,
    "BANDIT_OUTLAW": 3,
    "UNDEAD_CREATURES": 3,
    "HIGHLAND_SCOUT": 3,
    "BOW_MARSHAL": 3,
    "FOREST_GUARDIAN": 3
}

def create_deck():
    """Creates a fresh deck from the composition"""
    deck_list = []
    for card_name, copies in DECK_COMPOSITION.items():
        card = CARD_CATALOG[card_name]
        for _ in range(copies):
            deck_list.append(Ally(orig=card))
    return deck_list
