from Card import Ally


# The main way to organize allies in the game board
# assumes only one type of ally
class Army:
    def __init__(self):
        self._maxSlots = 7
        self._boardSize = 0
        self._board = []

    def maxSlots(self, maxSlots=None):
        if maxSlots:
            self._maxSlots = maxSlots
        return self._maxSlots

    def boardSize(self, boardSize=None):
        if boardSize:
            self._boardSize = boardSize
        return self._boardSize

    def setBoardSize(self):
        self._boardSize = len(self._board)

    def getBoard(self):
        return self._board

    def addAlly(self, ally):
        if self.boardSize() <= self.maxSlots():
            self._board.append(ally)
            self.setBoardSize()
        else:
            print('Board is full')

    def tollTheDead(self):
        for i in self._board:
            if i.health() <= 0:
                self._board.remove(i)

    # find the index of a specific ally on the board
    def findAlly(self, ally):
        if isinstance(ally, Ally):
            for i in self._board:
                if i == ally:
                    return i
            print('That ally is not in battle')
        print('That is not an ally')

    # gain access to an index on the board
    def findIndex(self, index):
        if index < 0 & index > 7:
            print('Index is out of range')
        elif self._board[index] == None:
            print('There is no ally here')
        return(self._board[index])

    def printArmy(self):
        if self.boardSize() > 0:
            for i, j in enumerate(self._board):
                print(f'~_{i+1}{j}')
        else:
            print('Your board is empty!')

    def __repr__(self):
        if self._board != []:
            for c, slot_c in enumerate(self._board):
                print(f'{c}: {slot_c}', end='', flush=True)
        else:
            return 'The Board is Empty'
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
