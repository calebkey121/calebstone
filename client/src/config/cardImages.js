import siegeEngineer from "../assets/images/cards/Siege Engineer.png";
import royalFalconer from "../assets/images/cards/Royal Falconer.png";
import wanderingMinstrel from "../assets/images/cards/Wandering Minstrel.png";
import courtAlchemist from "../assets/images/cards/Court Alchemist.png";
import mercenaryCaptain from "../assets/images/cards/Mercenary Captain.png";
import villageBlacksmith from "../assets/images/cards/Village Blacksmith.png";
import joustingChampion from "../assets/images/cards/Jousting Champion.png";
import direWolf from "../assets/images/cards/Dire Wolf.png";
import castleWard from "../assets/images/cards/Castle Ward.png";
import highwaymansAmbush from "../assets/images/cards/Highwayman's Ambush.png";
import banditOutlaw from "../assets/images/cards/Bandit Outlaw.png";
import undeadCreatures from "../assets/images/cards/Undead Creatures.png";
import highlandScout from "../assets/images/cards/Highland Scout.png";
import bowMarshal from "../assets/images/cards/Bow Marshal.png";
import forestGuardian from "../assets/images/cards/Forest Guardian.png";
import titanOverlord from "../assets/images/cards/raccoon.jpg";

export const CARD_IMAGES = {
  SIEGE_ENGINEER: siegeEngineer,
  ROYAL_FALCONER: royalFalconer,
  WANDERING_MINSTREL: wanderingMinstrel,
  COURT_ALCHEMIST: courtAlchemist,
  MERCENARY_CAPTAIN: mercenaryCaptain,
  VILLAGE_BLACKSMITH: villageBlacksmith,
  JOUSTING_CHAMPION: joustingChampion,
  DIRE_WOLF: direWolf,
  CASTLE_WARD: castleWard,
  HIGHWAYMANS_AMBUSH: highwaymansAmbush,
  BANDIT_OUTLAW: banditOutlaw,
  UNDEAD_CREATURES: undeadCreatures,
  HIGHLAND_SCOUT: highlandScout,
  BOW_MARSHAL: bowMarshal,
  FOREST_GUARDIAN: forestGuardian,
  TITAN_OVERLORD: titanOverlord,
};

// Optional: Create a function to get card image by ID
export const getCardImage = (cardId) => {
  return CARD_IMAGES[cardId] || "/raccoon.jpg";
};

// CARD_CATALOG = {
//   SIEGE_ENGINEER: SIEGE_ENGINEER,
//   ROYAL_FALCONER: ROYAL_FALCONER,
//   WANDERING_MINSTREL: WANDERING_MINSTREL,
//   COURT_ALCHEMIST: COURT_ALCHEMIST,
//   MERCENARY_CAPTAIN: MERCENARY_CAPTAIN,
//   VILLAGE_BLACKSMITH: VILLAGE_BLACKSMITH,
//   JOUSTING_CHAMPION: JOUSTING_CHAMPION,
//   DIRE_WOLF: DIRE_WOLF,
//   CASTLE_WARD: CASTLE_WARD,
//   HIGHWAYMANS_AMBUSH: HIGHWAYMANS_AMBUSH,
//   BANDIT_OUTLAW: BANDIT_OUTLAW,
//   UNDEAD_CREATURES: UNDEAD_CREATURES,
//   HIGHLAND_SCOUT: HIGHLAND_SCOUT,
//   BOW_MARSHAL: BOW_MARSHAL,
//   FOREST_GUARDIAN: FOREST_GUARDIAN,
//   TITAN_OVERLORD: TITAN_OVERLORD,
// };
