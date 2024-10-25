from Army import Army
from Deck import Deck
from Card import Card
from Ally import Ally
from Hero import Hero
from Signal import Signal
from config.GameSettings import *
from dataclasses import dataclass, field

@dataclass
class PlayerSignals:
    """Signals owned by the player"""
    on_gold_gained: Signal = field(default_factory=Signal)
    on_gold_spent: Signal = field(default_factory=Signal)
    on_income_gained: Signal = field(default_factory=Signal)
    on_income_lost: Signal = field(default_factory=Signal)
    on_fatigue: Signal = field(default_factory=Signal)
    on_card_played: Signal = field(default_factory=Signal)

class Player:
    def __init__(self,
                 heroName,
                 deckList,
                 player_subscribers: dict = None,
                 ally_subscribers: dict = None,
                 hero_subscribers: dict = None):
        
        # Store hero subscribers for hero initialization
        self._hero_subscribers = hero_subscribers or {
            "on_death": [],
            "on_damage_taken": [],
            "on_heal": [],
            "on_attack": [],
            "on_damage_dealt": []
        }
        
        # Initialize hero with subscribers
        self._hero = Hero(heroName, hero_subscribers=self._hero_subscribers)
        self._name = heroName # for now, we'll see
        self._deck = Deck(deckList)
        self._army = Army()
        self._hand = []
        self._maxHandSize = PLAYER_MAX_HAND_SIZE
        self._gold = 0
        self._income = 0

        # Player-owned signals
        self.signals = PlayerSignals()
        
        # Store ally subscribers for use when allies are played
        self._ally_subscribers = ally_subscribers or {
            "on_death": [],
            "on_attack": [],
            "on_damage_dealt": [],
            "on_damage_taken": []
        }
        self._ally_subscribers["on_death"].append(self._army.toll_the_dead)

        # Connect player-level subscribers
        for signal_name, callbacks in (player_subscribers or {}).items():
            if hasattr(self.signals, signal_name):
                signal = getattr(self.signals, signal_name)
                signal.connect(callbacks)
    
    def __eq__(self, other: 'Player') -> bool:
        if not isinstance(other, Player):
            return NotImplemented
        return (
            self._hero == other._hero and
            self._army == other._army and
            self._gold == other._gold and
            self._income == other._income and
            len(self._hand) == len(other._hand) and
            all(c1 == c2 for c1, c2 in zip(self._hand, other._hand))
        )
    
    @property
    def gold(self):
        return self._gold
    @gold.setter
    def gold(self, new_amount):
        change_amount = new_amount - self.gold
        if change_amount >= 0: # think if = is necessary
            self.signals.on_gold_gained.emit(change_amount)
        else:
            self.signals.on_gold_spent.emit(-change_amount) # want abs amount of gold spent
        self._gold = new_amount

    @property
    def income(self):
        return self._income
    @income.setter
    def income(self, new_amount):
        change_amount = new_amount - self.income
        if change_amount >= 0: # think if = is necessary
            self.signals.on_income_gained.emit(change_amount)
        else:
            self.signals.on_income_lost.emit(change_amount)
        self._income += change_amount
    
    # Helpers: useful checks that don't affect the game state
    # Status Checks (mainly for output)
    def get_hero_status(self):
        return {
            "name": self._hero._name,
            "attack": self._hero._attack,
            "health": self._hero.health
        }
    def get_army_status(self):
        return [ { "name": ally._name, "attack": ally._attack, "health": ally.health, "cost": ally._cost } for ally in self._army.get_army() ]
    def get_hand_status(self):
        return [ { "name": card._name, "attack": card._attack, "health": card.health, "cost": card._cost } for card in self._hand ]
    # Hero Helpers
    def hero_health(self):
        return self._hero.health
    def is_dead(self):
        return self.hero_health() <= 0
    # Deck Helpers
    def out_of_cards(self):
        return self._deck.current_num_cards() <= 0
    
    # Army Helpers
    def get_army_size(self):
        return self._army.army_size()

    # IMPORTANT: Should return indicies, hero is always 0
    def available_targets(self): # attackable allies
        availableTargets = []
        availableTargets.append(0) # for hero
        for idx, ally in enumerate(self._army.get_army()):
            availableTargets.append(idx + 1) # army starts at 1
        return availableTargets

    # IMPORTANT: Should return indicies, hero is always 0
    def available_attackers(self):
        available_attackers = []
        if (self._hero.can_attack()):
            available_attackers.append(0) # for hero
        for idx, ally in enumerate(self._army.get_army()):
            if (ally.can_attack()):
                available_attackers.append(idx + 1)
        return available_attackers
    
    # This version just returns a list that can be indexed by the above
    def all_characters(self):
        return [ self._hero ] + self._army.get_army()

    def in_army(self, ally):
        return self._army.in_army(ally)
    
    # Hand Helpers
    def current_hand_size(self):
        return len(self._hand)
    
    def get_from_hand(self, position):
        return self._hand[position] # will error on out of range, think this is fine with how we're handling errors
    
    def any_cards(self):
        return len(self._hand) > 0

    def hand_is_full(self):
        return self.current_hand_size() == self.max_hand_size()

    def any_playable_cards(self): # Are there any playable cards in my hand?
        playable = False
        for i in self._hand:
            if i.cost() <= self.gold:
                playable = True
        return playable

    def playable_cards(self): # What cards are playable in your hand?
        playable = [] # indicies
        for idx, card in enumerate(self._hand):
            if card._cost <= self.gold:
                playable.append(idx)
        return playable
    
    def playable_card(self, card):
        if not isinstance(card, Card):
            raise ValueError(f"Checking non Card type. Got: {card}")
        playable = False
        if card.cost() <= self.gold():
            playable = True
        return playable

    def playable_hand(self):
        playable = []
        for i in self._hand:
            if i.cost() <= self.gold:
                playable.append(i)
        return playable

    def in_hand(self, card):
        if not isinstance(card, Card):
            raise ValueError(f"Checking non Card type. Got: {card}")
        return card in self._hand

    # Gold Helpers
    def has_enough_gold(self, index):
        if not isinstance(index, int):
            raise ValueError(f"Checking non int index. Got: {index}")
        return self._hand[index]._cost <= self.gold
    
    # Actions: exposed functions that directly affect the game state
    def ready_up(self):
        self._hero.ready_up()
        self._army.ready_up()
    
    # Deck Actions
    # Army Actions
    def call_to_arms(self, ally): # hate and love this function name, its dumb but i like it
        if not isinstance(ally, Ally):
            raise ValueError(f"Tried adding non ally to army. Got: {ally}")
        self._army.add_ally(ally)

    # TODO move outside of player, player should just do what is told and manager will control battlecries and such
    #def play_ally(self, card, opposingPlayer):
    #    if not self._army.is_full() and card._cost <= self.gold:
    #        self._army.add_ally(card)
    #        card.ready_down()
    #        self.gold -= card.cost()
    #        self.remove_from_hand(card)
    #        # handle battlecry
    #        if card._playEffect:
    #            card._playEffect(amount=card._amount[0], player=self, opposingPlayer=opposingPlayer)
    #        self._army.toll_the_dead()
    #        opposingPlayer._army.toll_the_dead()
    #    else: return None # unsuccessful
    def play_ally(self, card):
        if self._army.is_full() or card._cost > self.gold:
            raise ValueError("Card unplayable")
        self._army.add_ally(card)
        card.ready_down()
        self.gold -= card._cost
        self.remove_from_hand(card)
        self.signals.on_card_played.emit(card)
        
        # Connect all relevant subscribers to the ally's signals
        for signal_name, callbacks in self._ally_subscribers.items():
            if hasattr(card, signal_name):
                ally_signal = getattr(card, signal_name) # ally.on_death
                ally_signal.connect(callbacks)

    # Hand Actions
    def max_hand_size(self, newSize=None):
        if newSize:
            self._maxHandSize = newSize
        return self._maxHandSize

    def remove_from_hand(self, card):
        if not isinstance(card, Card):
            raise ValueError(f"Expected Card argument. Got: {card}")
        for i in self._hand:
            if i == card:
                self._hand.remove(i)
                return
        raise ValueError("Card was not in hand.")

    def draw_card(self):
        if self.out_of_cards():
            # oh no! taking fatigue damage
            fatigue_damage = self._deck.take_fatigue()
            self.damage_hero(fatigue_damage)
            self.signals.on_fatigue.emit(fatigue_damage)
            return
        card = self._deck.draw_card()
        if not self.hand_is_full():
            self._hand.append(card)

    def draw_cards(self, number):
        if not isinstance(number, int) or number < 0:
            raise ValueError(f"Number of cards to draw must be a positive integer. Got: {number}")
        for i in range(number):
            self.draw_card()

    # Battle Actions
    # TODO: Move outside of player, remember player will only do things that affect itself
    # def attack_enemy(self, enemy, attackingPlayer):
    #     if self._ready:
    #         if self.attack() >= 0:
    #             enemy.lower_health(self.attack())
    #         if enemy.attack() >= 0:
    #             self.lower_health(enemy.attack())
    #         if enemy.health() < 0:
    #             enemy.health(0)
    #             attackingPlayer.get_bounty(2)
    #         self.ready_down()
    
    def damage_hero(self, damage):
        if not isinstance(damage, int):
            raise ValueError(f"Damage must be an integer. Got: {damage}")
        self._hero.health -= damage
    
    def damage_army(self, damage):
        if not isinstance(damage, int) or damage < 0:
            raise ValueError(f"Damage must be a positive integer. Got: {damage}")
        for ally in self._army._army:
            ally.health -= damage
    
    def damage_all(self, damage): # simply additionally include hero
        if not isinstance(damage, int) or damage < 0:
            raise ValueError(f"Damage must be a positive integer. Got: {damage}")
        self.damage_hero(damage)
        self.damage_army(damage)

    def heal_hero(self, heal):
        if not isinstance(heal, int):
            raise ValueError(f"Heal amount must be an integer. Got: {heal}")
        self._hero.health += heal
    
    def heal_army(self, heal):
        if not isinstance(heal, int) or heal < 0:
            raise ValueError(f"Heal amount must be a positive integer. Got: {heal}")
        for ally in self._army.get_army():
            ally.health += heal

    def heal_all(self, heal):
        if not isinstance(heal, int) or heal < 0:
            raise ValueError(f"Heal amount must be a positive integer. Got: {heal}")
        self.heal_hero(heal)
        self.heal_army(heal)

    # Gold
    # TODO: alot of this is dependent on the overall game state, soooo move it out of player
    # def set_gold(self, roundNumber): # Players have a certain income, they earn that much gold per turn
    #     if (roundNumber % X_ROUNDS) == 0:
    #         self._income += INCOME_PER_X_ROUNDS
    #     self.gold += self._income
    #     if self.gold > self._maxGold: self.gold = self._maxGold
    # def steal_gold_from(self, opposingPlayer, amount):
    #     opposingPlayer.gold -= amount
    #     if opposingPlayer.gold < 0:
    #         stolenAmount = amount + opposingPlayer.gold # ex stealing 5, has 4 -> .gold = -1: 5 + -1 = 4 (how much was actually stolen)
    #         opposingPlayer.gold = 0 # cant go below 0
    #     else:
    #         stolenAmount = amount
    #     self.get_bounty(stolenAmount)
    # def steal_income_from(self, opposingPlayer, amount):
    #     if amount > 0 and opposingPlayer:
    #         opposingPlayer.change_income(-amount)
    #         if opposingPlayer._income < 0:
    #             stolenAmount = amount + opposingPlayer._income # ex stealing 5, has 4 -> .gold = -1: 5 + -1 = 4 (how much was actually stolen)
    #             opposingPlayer._income = 0 # cant go below 0
    #         else:
    #             stolenAmount = amount
    #         self.change_income(stolenAmount)
    #     else:
    #         raise ValueError("Using Hero.steal_income_from incorrectly")
