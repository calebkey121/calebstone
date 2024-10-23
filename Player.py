from Army import Army
from Deck import Deck
from Card import Card, Ally
from Hero import Hero
from config.GameSettings import *

class Player:
    def __init__(self, heroName, deckList):
        # Private Variables start with an underscore (_hero)
        # Very important that when using the player class you use the exposed functions and do NOT directly ref private variables
        self._name = heroName
        self._hero = Hero(heroName)
        self._deck = Deck(deckList)
        self._army = Army()
        self._hand = []
        self._maxHandSize = PLAYER_MAX_HAND_SIZE
        self._gold = 0
        self._maxGold = PLAYER_MAX_GOLD
        self._income = 0
        self._maxIncome = PLAYER_MAX_INCOME
    
    # Helpers: useful checks that don't affect the game state
    # Status Checks (mainly for output)
    def get_hero_status(self):
        return {
            "name": self._hero._name,
            "attack": self._hero._attack,
            "health": self._hero._health
        }
    def get_army_status(self):
        return [ { "name": ally._name, "attack": ally._attack, "health": ally._health, "cost": ally._cost } for ally in self._army.get_army() ]
    def get_hand_status(self):
        return [ { "name": card._name, "attack": card._attack, "health": card._health, "cost": card._cost } for card in self._hand ]
    # Hero Helpers
    def hero_health(self):
        return self._hero._health
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
            if i.cost() <= self._gold:
                playable = True
        return playable

    def playable_cards(self): # What cards are playable in your hand?
        playable = [] # indicies
        for idx, card in enumerate(self._hand):
            if card._cost <= self._gold:
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
            if i.cost() <= self._gold:
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
        return self._hand[index]._cost <= self._gold
    
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
    
    def toll_the_dead(self):
        self._army.toll_the_dead()

    # TODO move outside of player, player should just do what is told and manager will control battlecries and such
    #def play_ally(self, card, opposingPlayer):
    #    if not self._army.is_full() and card._cost <= self._gold:
    #        self._army.add_ally(card)
    #        card.ready_down()
    #        self._gold -= card.cost()
    #        self.remove_from_hand(card)
    #        # handle battlecry
    #        if card._playEffect:
    #            card._playEffect(amount=card._amount[0], player=self, opposingPlayer=opposingPlayer)
    #        self._army.toll_the_dead()
    #        opposingPlayer._army.toll_the_dead()
    #    else: return None # unsuccessful
    def play_ally(self, card):
        if self._army.is_full() or card._cost > self._gold:
            raise ValueError("Card unplayable")
        self._army.add_ally(card)
        card.ready_down()
        self._gold -= card._cost
        self.remove_from_hand(card)

    # Hand Actions
    def play_card(self, index):
        if not isinstance(index, int):
            raise ValueError(f"Expected int argument. Got: {index}")
        card = self._hand[index]
        if card._cost > self._gold:
            raise ValueError("Tried playing unplayable card.")
        self.play_ally(card)

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
        self._hero.take_damage(damage)
    
    def damage_army(self, damage):
        if not isinstance(damage, int) or damage < 0:
            raise ValueError(f"Damage must be a positive integer. Got: {damage}")
        for ally in self._army:
            ally.take_damage(damage)
    
    def damage_all(self, damage): # simply additionally include hero
        if not isinstance(damage, int) or damage < 0:
            raise ValueError(f"Damage must be a positive integer. Got: {damage}")
        self._hero.take_damage(damage)
        self.damage_army(damage)

    def heal_hero(self, heal):
        if not isinstance(heal, int):
            raise ValueError(f"Heal amount must be an integer. Got: {heal}")
        self._hero.heal_damage(heal)
    
    def heal_army(self, heal):
        if not isinstance(heal, int) or heal < 0:
            raise ValueError(f"Heal amount must be a positive integer. Got: {heal}")
        for ally in self._army:
            ally.heal_damage(heal)

    def heal_all(self, heal):
        if not isinstance(heal, int) or heal < 0:
            raise ValueError(f"Heal amount must be a positive integer. Got: {heal}")
        self._hero.heal_damage(heal)
        self.heal_army(heal)

    # Gold
    # TODO: alot of this is dependent on the overall game state, soooo move it out of player
    # def set_gold(self, roundNumber): # Players have a certain income, they earn that much gold per turn
    #     if (roundNumber % X_ROUNDS) == 0:
    #         self._income += INCOME_PER_X_ROUNDS
    #     self._gold += self._income
    #     if self._gold > self._maxGold: self._gold = self._maxGold
    # def steal_gold_from(self, opposingPlayer, amount):
    #     opposingPlayer._gold -= amount
    #     if opposingPlayer._gold < 0:
    #         stolenAmount = amount + opposingPlayer._gold # ex stealing 5, has 4 -> ._gold = -1: 5 + -1 = 4 (how much was actually stolen)
    #         opposingPlayer._gold = 0 # cant go below 0
    #     else:
    #         stolenAmount = amount
    #     self.get_bounty(stolenAmount)
    # def steal_income_from(self, opposingPlayer, amount):
    #     if amount > 0 and opposingPlayer:
    #         opposingPlayer.change_income(-amount)
    #         if opposingPlayer._income < 0:
    #             stolenAmount = amount + opposingPlayer._income # ex stealing 5, has 4 -> ._gold = -1: 5 + -1 = 4 (how much was actually stolen)
    #             opposingPlayer._income = 0 # cant go below 0
    #         else:
    #             stolenAmount = amount
    #         self.change_income(stolenAmount)
    #     else:
    #         raise ValueError("Using Hero.steal_income_from incorrectly")
    def change_gold(self, amount):
        self._gold += amount
        if self._gold < 0:
            self._gold = 0
        if self._gold > self._maxGold:
            self._gold = self._maxGold

    def change_income(self, amount):
        self._income += amount
        if self._income < 0:
            self._income = 0
        if self._income > self._maxIncome:
            self._income = self._maxIncome
