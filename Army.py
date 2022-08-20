from Card import Ally

# The main way to organize allies in the game army
# assumes only one type of ally
class Army:
    def __init__(self):
        self._maxSlots = 7
        self._armySize = 0
        self._army = []

    # can any allies attack?
    def available_attackers(self):
        for ally in self._army:
            if ally.is_ready():
                return True
        return False

    # getter/setter for maxSlots
    def max_slots(self, maxSlots=None):
        if maxSlots:
            self._maxSlots = maxSlots
        return self._maxSlots

    # getter/setter for maxSlots
    def army_size(self, armySize=None):
        self.set_army_size()
        if armySize:
            self._armySize = armySize
        return self._armySize

    
    def set_army_size(self):
        self._armySize = len(self._army)

    
    # Returns true if the army is full
    def is_full(self):
        self.set_army_size()
        returnVal = False
        if self.army_size() == self.max_slots():
            returnVal = True
        return returnVal

    def get_army(self):
        return self._army

    def add_ally(self, ally):
        if self.army_size() <= self.max_slots():
            self._army.append(ally)
            self.set_army_size()
        else:
            print('Army is full')

    #This clears your Army of dead Allies
    def toll_the_dead(self):
        for i in self._army:
            if i.health() <= 0:
                self._army.remove(i)

    # find the index of a specific ally on the army
    def find_ally(self, ally):
        if isinstance(ally, Ally):
            for i in self._army:
                if i == ally:
                    return i
            print('That ally is not in battle')
        print('That is not an ally')

    def print_army(self):
        if self.army_size() > 0:
            for i, j in enumerate(self._army):
                print(f'{i+1}: {j}')
        else:
            print('Your army is empty!')

    def get_ally_at(self, index):
        try:
            return self._army[index]
        except IndexError:
            return None


    def __repr__(self):
        if self._army != []:
            for c, slot_c in enumerate(self._army):
                print(f'{c}: {slot_c}', end='', flush=True)
        else:
            return 'The Army is Empty'
        return '__________________________'

def main():
    pass  

if __name__ == "__main__":
    main()