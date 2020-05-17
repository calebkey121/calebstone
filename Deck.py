from Card import Ally
import random


class Deck:
    def __init__(self):
        self._deckList = []
        self._startingNumCards = 30
        self._currentNumCards = 0

    # Reading cards from a text file ***ALLIES ONLY***
    # In text file, use '#' for comment 
    # Format: NAME, COST, ATTACK, HEALTH
    def import_txt(self, file):
        with open(file) as f:
            for line in f:
                # Each line of the incoming txt file should be an ALLY formatted as:
                # NAME, ATTACK, HEALTH
                
                # Using '#' is considered a comment
                if line[0] == '#':
                    continue

                # This line is a list of [NAME, ATTACK, HEALTH]
                input_card = line.strip().split(',')

                # I want to put some check here to make sure the values that I get
                # are good to create a card with - to throw error if some garbage 
                # txt file is read

                new_ally = Ally(name=input_card[0],
                                cost=int(input_card[1]),
                                attack=int(input_card[2]),
                                health=int(input_card[3]))
                self.add_card(new_ally)
                
    # adds card to deck
    def add_card(self, card):
        self._deckList.append(card)
        self.set_num_cards()

    # remove card from deck
    def remove_card(self, card):
        self._deckList.remove(card)
        self.set_num_cards()

    # Sets deck list
    # could simply add 1, but to be safe set to len(deck_list)
    def set_num_cards(self):
        self._currentNumCards = len(self._deckList)

    def get_current_num_cards(self):
        return self._currentNumCards

    # Picks random card from deck and appends to hand - returns that card
    def draw_card(self, hand):
        if len(self._deckList) <= 0:
            print('Your Deck is empty!!!')
        else:
            draw = random.choice(self._deckList)
            hand.append(draw)
            self.remove_card(draw)
            return draw

    def burn_card(self):
        draw = random.choice(self._deckList)
        self.remove_card(draw)
        return draw

    def __repr__(self):
        print('____________________')
        print(f'Current Deck Size: {self.get_current_num_cards()}')
        for i in self._deckList:
            print(i)
        return '____________________'


def main():
    # This is to demonstrate how this deck class interacts with 
    # an input txt file, class cards and ally, and how it presents its data

    # Create empty deck
    caleb_deck = Deck()
    # Read any txt file that complies with the given format
    caleb_deck.import_txt('Decklist.txt')

    # In game player will have a hand and draw 5 cards at the start of the game
    # Here I show the deck in full, the 5 drawn cards now appended to hand, and
    # the deck after the cards were drawn
    # *** DECK IS 30 CARDS LONG - EXPECT A LOT OF OUTPUT***
    hand = []

    print('Printing Deck...')
    print(caleb_deck)
    print('Finished Printing Deck...')

    print('Draw 5 Cards')
    for i in range(5):
        caleb_deck.draw_card(hand)
    print(hand)

    print('Printing New Deck...')
    print(caleb_deck)
    print('Finished Printing New Deck...')


if __name__ == "__main__":
    main()
