import random

class Deck:
    def __init__(self, deckList):
        self._deckList = deckList
        self.set_num_cards()
        self._startingNumCards = 45
                
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

    def get_current_num_cards(self):
        return self._currentNumCards

    # Picks random card from deck and appends to hand - returns that card
    def draw_card(self, hand):
        if self.get_current_num_cards() <= 0:
            self._currentNumCards -= 1
            return self.get_current_num_cards()
        else:
            draw = random.choice(self._deckList)
            hand.append(draw)
            self.remove_card(draw)
            return draw

    def burn_card(self):
        draw = random.choice(self._deckList)
        self.remove_card(draw)
        return draw._name
