import random
from config.GameSettings import DECK_STARTING_NUM_CARDS

class Deck:
    def __init__(self, deckList):
        self._deckList = deckList
        self.set_num_cards()
        self._startingNumCards = DECK_STARTING_NUM_CARDS
        self._fatigueCounter = 0
                
    # adds card to deck
    def add_card(self, card):
        self._deckList.append(card)
        self.set_num_cards()

    # remove card from deck
    def remove_card(self, card):
        self._deckList.remove(card)
        self.set_num_cards()

    # Sets deck list length or size
    def set_num_cards(self):
        self._currentNumCards = len(self._deckList)

    def current_num_cards(self):
        return self._currentNumCards
    
    def out_of_cards(self):
        return self._currentNumCards <= 0

    # Picks random card from deck and returns that card
    def draw_card(self):
        if self.out_of_cards():
            raise ValueError("Tried drawing a card when out of cards")
        draw = random.choice(self._deckList)
        self.remove_card(draw)
        return draw
    
    def take_fatigue(self):
        # Should we only increment this when out of cards?
        self._fatigueCounter += 1
        return self._fatigueCounter
