from Army import Army
from Deck import Deck
from Card import Ally

# This represents the player - Human or AI
class Hero:
    def __init__(self, **kwargs):
        # Heros are the player and hold all the variables that the player will have in game
        # In the future, I want the heros to be unique, here the just have the following:
        # :: Name, Health, Gold, Deck(of cards), Hand(of cards), and related variables
        self._name = kwargs['hero'] if 'hero' in kwargs else 'Finn'
        self._deckList = kwargs['deckList'] if 'deckList' in kwargs else Deck()
        self._army = kwargs['army'] if 'army' in kwargs else Army()
        self._health = 30
        self._attack = 0
        self._ready = True
        self._gold = 0
        self._hand = []
        self._maxHandSize = 10

    # Hero's Army Functions
    def call_to_arms(self, ally=None):
        if ally:
            self._army.add_ally(ally)
        return self._army

    def attack(self, attack=None):
        if attack:
            self._attack = attack
        return self._attack

    def get_army_size(self):
        return self.call_to_arms().army_size()

    # Hand Functions
    def max_hand_size(self, newSize=None):
        if newSize:
            self._maxHandSize = newSize
        return self._maxHandSize

    def current_hand_size(self):
        return len(self._hand)

    def print_hand(self):
        for i, j in enumerate(self._hand):
            print(f'{i+1}: {j}')

    def remove_from_hand(self, card):
        for i in self._hand:
            if i == card:
                self._hand.remove(i)

    def attack_enemy(self, enemy):
        if self._ready:
            if self.attack() >= 0:
                enemy.lower_health(self.attack())
            if enemy.attack() >= 0:
                self.lower_health(enemy.attack())
            self.ready_down()
        else:
            print(f'{self.name()} is not ready!')

    def get_from_hand(self, position):
        return self._hand[position]

    def any_cards(self):
        if len(self._hand) > 0:
            return True
        else:
            return False

    # Variable Changing
    def deck_list(self, deckList=None):
        if deckList:
            self._deckList.import_txt(deckList)
        return self._deckList

    def gold(self, income=None):
        if income:
            self._gold = income
        return self._gold

    def name(self, name=None):
        if name:
            self._name = name
        return self._name
    
    def health(self, health=None):
        if health:
            self._health = health
        return self._health

    def lower_health(self, attackVal):
        self._health -= attackVal

    # Card Draw
    def draw_card(self):
        if len(self._hand) < self.max_hand_size():
            # CASE: Out of Cards!! Take damage equal to the amount of cards that you have overdrawn
            if self.deck_list().get_current_num_cards() <= 0:
                damage = self._deckList.draw_card(self._hand)
                print(f'Fatigue: {-damage} damage delt to your hero')
                self._health += damage
            else:
                draw = self._deckList.draw_card(self._hand)
                print(self.name() + ' drew ' + draw.name() + '\n')
        else:
            if self.deck_list().get_current_num_cards() > 0:
                print('Your hand is too full!')
                print(self._name + ' burned:', self._deckList.burn_card())
            else:
                damage = self._deckList.draw_card(self._hand)
                print(f'Fatigue: {-damage} damage delt to your hero')
                self._health += damage

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
        availableTargets = []
        availableTargets.append(self)
        for i in self.call_to_arms()._army:
            availableTargets.append(i)
        return availableTargets

    def ready_up(self):
        self._ready = True

    def ready_down(self):
        self._ready = False

    def is_ready(self):
        return self._ready

    def __repr__(self):
        return f'~__{self.name()}__~ \tAttack: {self.attack()} \tHealth: {self.health()}'

def main():
    pass


if __name__ == "__main__":
    main()