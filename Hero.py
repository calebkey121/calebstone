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
    def callToArms(self, ally=None):
        if ally:
            self._army.addAlly(ally)
        return self._army

    def heroAttack(self, attack=None):
        if attack:
            self._heroAttack = attack
        return self._heroAttack

    def getBoardSize(self):
        return self.callToArms().boardSize()

    def printArmy(self):
        self.callToArms().printArmy()

    # Hand Functions
    def maxHandSize(self, newSize=None):
        if newSize:
            self._maxHandSize = newSize
        return self._maxHandSize

    def currentHandSize(self):
        return len(self._hand)

    def printHand(self):
        for i, j in enumerate(self._hand):
            print(f'~_{i}{j}')

    def removeFromHand(self, card):
        for i in self._hand:
            if i == card:
                self._hand.remove(i)

    def getFromHand(self, position):
        return self._hand[position]

    def anyCards(self):
        if len(self._hand) > 0:
            return True
        else:
            return False

    # Variable Changing
    def deckList(self, deckList=None):
        if deckList:
            self._deckList.importTxt(deckList)
        return self._deckList

    def gold(self, income=None):
        if income:
            self._gold = income
        return self._gold

    def heroName(self, name=None):
        if name:
            self._heroName = name
        return self._heroName
    
    def heroHealth(self, heroHealth=None):
        if heroHealth:
            self._heroHealth = heroHealth
        return self._heroHealth

    def lowerHealth(self, attackVal):
        self._heroHealth -= attackVal

    # Card Draw
    def drawCard(self):
        if len(self._hand) <  self.maxHandSize():
            draw = self._deckList.drawCard(self._hand)
            print(self.heroName() + ' drew ' + draw.name())
        else:
            print('Your hand is too full!')
            print(self._heroName + ' burned:\n~_', self._deckList.burnCard())

    def drawCards(self, number):
        for i in range(number):
            self.drawCard()

    # Playing Cards!!!
    def playAlly(self, card):
        self.callToArms().addAlly(card)
        self._gold -= card.cost()
        self.removeFromHand(card)

    # Gold Management
    # Are there any playable cards in my hand?
    def playableCards(self):
        playable = False
        for i in self._hand:
            if i.cost() <= self._gold:
                playable = True
        return playable

    # Is this card playable?
    def playableCard(self, card):
        playable = False
        if card.cost() <= self.gold():
            playable = True
        return playable

    # Representation - Weird String is me trying to make the output look cool
    def availableTargets(self):
        availableTargets = []
        for i in self.callToArms()._board:
            availableTargets.append(i)
        availableTargets.append(self)
        return availableTargets



    def __repr__(self):
        return f'''_{self.heroName()}___~
Attack: {self.heroAttack()}
Health: {self.heroHealth()}
~___________~
'''

def main():
    pass


if __name__ == "__main__":
    main()