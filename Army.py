from Card import Ally

# The main way to organize allies in the game army
# assumes only one type of ally
class Army:
    def __init__(self):
        self._maxSlots = 7
        self._armySize = 0
        self._army = []

    def maxSlots(self, maxSlots=None):
        if maxSlots:
            self._maxSlots = maxSlots
        return self._maxSlots

    def armySize(self, armySize=None):
        if armySize:
            self._armySize = armySize
        return self._armySize

    def setArmySize(self):
        self._armySize = len(self._army)

    def getArmy(self):
        return self._army

    def addAlly(self, ally):
        if self.armySize() <= self.maxSlots():
            self._army.append(ally)
            self.setArmySize()
        else:
            print('Army is full')

    #This clears your Army of dead Allies
    def tollTheDead(self):
        for i in self._army:
            if i.health() <= 0:
                self._army.remove(i)

    # find the index of a specific ally on the army
    def findAlly(self, ally):
        if isinstance(ally, Ally):
            for i in self._army:
                if i == ally:
                    return i
            print('That ally is not in battle')
        print('That is not an ally')

    # gain access to an index on the army
    def findIndex(self, index):
        if index < 0 & index > 7:
            print('Index is out of range')
        elif self._army[index] == None:
            print('There is no ally here')
        return(self._army[index])

    def printArmy(self):
        if self.armySize() > 0:
            for i, j in enumerate(self._army):
                print(f'~_{i+1}{j}')
        else:
            print('Your army is empty!')

    def __repr__(self):
        if self._army != []:
            for c, slot_c in enumerate(self._army):
                print(f'{c}: {slot_c}', end='', flush=True)
        else:
            return 'The Army is Empty'
        return '__________________________'

def main():
    # This is to demonstrate how the army class interacts with Allies
    # Here, we create an army of size 3
    army = Army()
    caleb = Ally(name='Caleb', cost=1, attack=3, health=2)
    luka = Ally(name='Luka', cost=3, attack=3, health=3)
    nathan = Ally(name='Nathan', cost=5, attack=5, health=5)
    army.addAlly(caleb)
    army.addAlly(luka)
    army.addAlly(nathan)

    print('Printing Army...')
    print(army)
    print('Finished Printing Army...')

    # Then we simulate damage by directly setting the health of a couple allies
    print('\nSet Health')
    army.findAlly(nathan).health(1)
    army.findAlly(luka).health(0)

    # If a ally has 0 health, like luka right now, then they are removed
    print('Toll the Dead\n')
    army.tollTheDead()

    # Results showns
    print('Printing New Army...')
    print(army)
    print('Finished Printing New Army...')

    

if __name__ == "__main__":
    main()