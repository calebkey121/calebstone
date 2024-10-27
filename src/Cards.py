from src.Ally import Ally
from src.Building import Building
from src.Effects import *

# Central definition of all cards in the game
SIEGE_ENGINEER = Ally(
    name="Siege Engineer",
    cost=1,
    attack_value=0,
    health=7,
    effect=HealAllAlliesEffect(
        amount=[15],
        timing=TimingWindow.ON_PLAY,
    )
)

ROYAL_FALCONER = Ally(
    name="Royal Falconer",
    cost=2,
    attack_value=6,
    health=4,
    effect=DamageEnemyHeroEffect(
        amount=[7],
        timing=TimingWindow.ON_DEATH,
    )
)

WANDERING_MINSTREL = Ally(
    name="Wandering Minstrel",
    cost=3,
    attack_value=5,
    health=10,
    effect=HealAllAlliesEffect(
        amount=[10],
        timing=TimingWindow.END_OF_TURN,
    )
)

COURT_ALCHEMIST = Ally(
    name="Court Alchemist",
    cost=4,
    attack_value=15,
    health=5,
    effect=DamageAllEnemiesEffect(
        amount=[6],
        timing=TimingWindow.ON_PLAY,
    )
)

MERCENARY_CAPTAIN = Ally(
    name="Mercenary Captain",
    cost=5,
    attack_value=9,
    health=16,
    effect=GainGoldEffect(
        amount=[3],
        timing=TimingWindow.ON_PLAY,
    )
)

VILLAGE_BLACKSMITH = Ally(
    name="Village Blacksmith",
    cost=6,
    attack_value=4,
    health=26,
    effect=GainIncomeEffect(
        amount=[2],
        timing=TimingWindow.ON_PLAY,
    )
)

JOUSTING_CHAMPION = Ally(
    name="Jousting Champion",
    cost=7,
    attack_value=17,
    health=18,
    effect=GainGoldEffect(
        amount=[3],
        timing=TimingWindow.END_OF_TURN,
    )
)

DIRE_WOLF = Ally(
    name="Dire Wolf",
    cost=8,
    attack_value=25,
    health=15,
    effect=DrawCardsEffect(
        amount=[2],
        timing=TimingWindow.ON_PLAY,
    )
)

CASTLE_WARD = Ally(
    name="Castle Ward",
    cost=9,
    attack_value=13,
    health=32,
    effect=None  # This card has no effect
)

HIGHWAYMANS_AMBUSH = Ally(
    name="Highwayman's Ambush",
    cost=10,
    attack_value=11,
    health=39,
    effect=DamageAllEnemiesEffect(
        amount=[5],
        timing=TimingWindow.ON_PLAY,
    )
)

BANDIT_OUTLAW = Ally(
    name="Bandit Outlaw",
    cost=11,
    attack_value=23,
    health=27,
    effect=GainGoldEffect(
        amount=[2],
        timing=TimingWindow.ON_DEATH,
    )
)

UNDEAD_CREATURES = Ally(
    name="Undead Creatures",
    cost=12,
    attack_value=30,
    health=30,
    effect=DamageAllEnemiesEffect(
        amount=[8],
        timing=TimingWindow.END_OF_TURN,
    )
)

HIGHLAND_SCOUT = Ally(
    name="Highland Scout",
    cost=13,
    attack_value=40,
    health=25,
    effect=DrawCardsEffect(
        amount=[3],
        timing=TimingWindow.ON_PLAY,
    )
)

BOW_MARSHAL = Ally(
    name="Bow Marshal",
    cost=14,
    attack_value=35,
    health=35,
    effect=DamageAllEnemiesEffect(
        amount=[10],
        timing=TimingWindow.ON_PLAY,
    )
)

FOREST_GUARDIAN = Ally(
    name="Forest Guardian",
    cost=15,
    attack_value=15,
    health=60,
    effect=HealAllAlliesEffect(
        amount=[50],
        timing=TimingWindow.ON_PLAY,
    )
)

# Export all cards in a dictionary for easy reference
CARD_CATALOG = {
    "SIEGE_ENGINEER": SIEGE_ENGINEER,
    "ROYAL_FALCONER": ROYAL_FALCONER,
    "WANDERING_MINSTREL": WANDERING_MINSTREL,
    "COURT_ALCHEMIST": COURT_ALCHEMIST,
    "MERCENARY_CAPTAIN": MERCENARY_CAPTAIN,
    "VILLAGE_BLACKSMITH": VILLAGE_BLACKSMITH,
    "JOUSTING_CHAMPION": JOUSTING_CHAMPION,
    "DIRE_WOLF": DIRE_WOLF,
    "CASTLE_WARD": CASTLE_WARD,
    "HIGHWAYMANS_AMBUSH": HIGHWAYMANS_AMBUSH,
    "BANDIT_OUTLAW": BANDIT_OUTLAW,
    "UNDEAD_CREATURES": UNDEAD_CREATURES,
    "HIGHLAND_SCOUT": HIGHLAND_SCOUT,
    "BOW_MARSHAL": BOW_MARSHAL,
    "FOREST_GUARDIAN": FOREST_GUARDIAN
}
