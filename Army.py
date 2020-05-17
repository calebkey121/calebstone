from Card import Ally


# The main way to organize allies in the game board
# assumes only one type of ally
class Army:
    def __init__(self):
        self._maxSlots = 7
        self._boardSize = 0
        self._board = []

    def max_slots(self, max_slots=None):
        if max_slots:
            self._maxSlots = max_slots
        return self._maxSlots

    def board_size(self, board_size=None):
        if board_size:
            self._boardSize = board_size
        return self._boardSize

    def set_board_size(self):
        self._boardSize = len(self._board)

    def get_board(self):
        return self._board

    def add_ally(self, ally):
        if self.board_size() <= self.max_slots():
            self._board.append(ally)
            self.set_board_size()
        else:
            print('Board is full')

    def toll_the_dead(self):
        for i in self._board:
            if i.health() <= 0:
                self._board.remove(i)

    # find the index of a specific ally on the board
    def find_ally(self, ally):
        if isinstance(ally, Ally):
            for i in self._board:
                if i == ally:
                    return i
            print('That ally is not in battle')
        print('That is not an ally')

    # gain access to an index on the board
    def find_index(self, index):
        if index < 0 & index > 7:
            print('Index is out of range')
        elif self._board[index] == None:
            print('There is no ally here')
        return self._board[index]

    def print_army(self):
        if self.board_size() > 0:
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
    army.add_ally(caleb)
    army.add_ally(luka)
    army.add_ally(nathan)

    print('Printing Army...')
    print(army)
    print('Finished Printing Army...')

    # Then we simulate damage by directly setting the health of a couple allies
    print('\nSet Health')
    army.find_ally(nathan).health(1)
    army.find_ally(luka).health(0)

    # If a ally has 0 health, like luka right now, then they are removed
    print('Toll the Dead\n')
    army.toll_the_dead()

    # Results shown
    print('Printing New Army...')
    print(army)
    print('Finished Printing New Army...')


if __name__ == "__main__":
    main()
