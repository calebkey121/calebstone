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
    def importTxt(self, file):
        with open(file) as f:
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
                self.addCard(newAlly)
                
    # adds card to deck
    def addCard(self, card):
        self._deckList.append(card)
        self.setNumCards()

    # remove card from deck
    def removeCard(self, card):
        self._deckList.remove(card)
        self.setNumCards()

    # Sets deck list
    # could simply add 1, but to be safe set to len(decklist)
    def setNumCards(self):
        self._currentNumCards = len(self._deckList)

    def getCurrentNumCards(self):
        return self._currentNumCards

    # Picks random card from deck and appends to hand - returns that card
    def drawCard(self, hand):
        if len(self._deckList) <= 0:
            print('Your Deck is empty!!!')
        else:
            draw = random.choice(self._deckList)
            hand.append(draw)
            self.removeCard(draw)
            return draw

    def burnCard(self):
        draw = random.choice(self._deckList)
        self.removeCard(draw)
        return draw


    def __repr__(self):
        print('____________________')
        print(f'Current Deck Size: {self.getCurrentNumCards()}')
        for i in self._deckList:
            print(i)
        return('____________________')
        
    
    
    
    
def main():
    pass
    
if __name__ == "__main__":
    main()