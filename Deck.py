from Card import Ally
import os
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
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        rel_path = "DeckLists/" + file
        abs_file_path = os.path.join(script_dir, rel_path)
        with open(abs_file_path) as f:
            for line in f:
                # Each line of the incoming txt file should be an ALLY formatted as:
                # NAME, ATTACK, HEALTH
                
                # Using '#' is considered a comment
                if line[0] == '#':
                    continue

                # This line is a list of [NAME, ATTACK, HEALTH]
                inputCard = line.strip().split(',')

                # I want to put some check here to make sure the values that I get
                # are good to create a card with - to throw error if some garbage 
                # txt file is read

                newAlly = Ally(name=inputCard[0], cost=int(inputCard[1]), attack=int(inputCard[2]), health=int(inputCard[3]))
                self.add_card(newAlly)
                
    # adds card to deck
    def add_card(self, card):
        self._deckList.append(card)
        self.set_num_cards()

    # remove card from deck
    def remove_card(self, card):
        self._deckList.remove(card)
        self.set_num_cards()

    # Sets deck list
    # could simply add 1, but to be safe set to len(decklist)
    def set_num_cards(self):
        self._currentNumCards = len(self._deckList)

    def get_current_num_cards(self):
        return self._currentNumCards

    # Picks random card from deck and appends to hand - returns that card
    def draw_card(self, hand):
        if self.get_current_num_cards() <= 0:
            print('Your Deck is empty!!!')
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
        return draw


    def __repr__(self):
        print('____________________')
        print(f'Current Deck Size: {self.get_current_num_cards()}')
        for i in self._deckList:
            print(i)
        return('____________________')
        
    
    
    
    
def main():
    pass
    
if __name__ == "__main__":
    main()