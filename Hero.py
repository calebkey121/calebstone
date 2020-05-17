from Army import Army
from Deck import Deck
from Card import Ally

# This represents the player - Human or AI


class Hero:
    def __init__(self, **kwargs):
        # Heros are the player and hold all the variables that the player will have in game
        # In the future, I want the heros to be unique, here the just have the following:
        # :: Name, Health, Gold, Deck(of cards), Hand(of cards), and related variables
        self._heroName = kwargs['hero'] if 'hero' in kwargs else 'Finn'
        self._deckList = kwargs['deckList'] if 'deckList' in kwargs else Deck()
        self._army = kwargs['army'] if 'army' in kwargs else Army()
        self._heroHealth = 30
        self._gold = 0
        self._hand = []
        self._maxHandSize = 10
        self._heroAttack = 0

    # Hero's Army Functions
    def call_to_arms(self, ally=None):
        if ally:
            self._army.add_ally(ally)
        return self._army

    def hero_attack(self, attack=None):
        if attack:
            self._heroAttack = attack
        return self._heroAttack

    def get_board_size(self):
        return self.call_to_arms().board_size()

    def print_army(self):
        self.call_to_arms().print_army()

    # Hand Functions
    def max_hand_size(self, new_size=None):
        if new_size:
            self._maxHandSize = new_size
        return self._maxHandSize

    def current_hand_size(self):
        return len(self._hand)

    def print_hand(self):
        for i, j in enumerate(self._hand):
            print(f'~_{i}{j}')

    def remove_from_hand(self, card):
        for i in self._hand:
            if i == card:
                self._hand.remove(i)

    def get_from_hand(self, position):
        return self._hand[position]

    def any_cards(self):
        if len(self._hand) > 0:
            return True
        else:
            return False

    # Variable Changing
    def deck_list(self, deck_list=None):
        if deck_list:
            self._deckList.import_txt(deck_list)
        return self._deckList

    def gold(self, income=None):
        if income:
            self._gold = income
        return self._gold

    def hero_name(self, name=None):
        if name:
            self._heroName = name
        return self._heroName
    
    def hero_health(self, hero_health=None):
        if hero_health:
            self._heroHealth = hero_health
        return self._heroHealth

    def lower_health(self, attack_val):
        self._heroHealth -= attack_val

    # Card Draw
    def draw_card(self):
        if len(self._hand) < self.max_hand_size():
            draw = self._deckList.draw_card(self._hand)
            print(self.hero_name() + ' drew ' + draw.name())
        else:
            print('Your hand is too full!')
            print(self._heroName + ' burned:\n~_', self._deckList.burn_card())

    def draw_cards(self, number):
        for i in range(number):
            self.draw_card()

    # Playing Cards!!!
    def play_ally(self, card):
        self.call_to_arms().add_ally(card)
        self._gold -= card.cost()
        self.remove_from_hand(card)

    # Gold Management
    # Are there any playable cards in my hand?
    def playable_cards(self):
        playable = False
        for i in self._hand:
            if i.cost() <= self._gold:
                playable = True
        return playable

    # Is this card playable?
    def playable_card(self, card):
        playable = False
        if card.cost() <= self.gold():
            playable = True
        return playable

    # Representation - Weird String is me trying to make the output look cool
    def available_targets(self):
        available_targets = []
        for i in self.call_to_arms()._board:
            available_targets.append(i)
        available_targets.append(self)
        return available_targets

    def __repr__(self):
        return f'''_{self.hero_name()}___~
Attack: {self.hero_attack()}
Health: {self.hero_health()}
~___________~
'''


def main():
    pass


if __name__ == "__main__":
    main()
