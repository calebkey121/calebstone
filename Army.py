from Card import Ally
from config.GameSettings import ARMY_MAX_SIZE

# The main way to organize allies in the game army
# assumes only one type of ally
class Army:
    def __init__(self):
        self._maxSize = ARMY_MAX_SIZE
        self._armySize = 0
        self._army = []

    # getter/setters
    def max_size(self, maxSize=None):
        if maxSize:
            self._maxSize = maxSize
        return self._maxSize
    
    def army_size(self, armySize=None):
        if armySize:
            self._armySize = armySize
        return self._armySize
    
    def get_army(self):
        return self._army

    def set_army_size(self):
        self._armySize = len(self._army)

    # can any allies attack?
    def available_attackers(self):
        for ally in self._army:
            if ally.is_ready():
                return True
        return False
    
    # Returns true if the army is full
    def is_full(self):
        return self.army_size() == self.max_size()

    def ready_up(self):
        for ally in self._army:
            ally.ready_up()

    def add_ally(self, ally):
        if not isinstance(ally, Ally) or self.is_full():
            raise ValueError("Must be adding an ally to a non full army")
        self._army.append(ally)
        self.set_army_size()

    #This clears your Army of dead Allies
    def toll_the_dead(self):
        for i in self._army:
            if i._health <= 0:
                self._army.remove(i)
        self.set_army_size()

    # find the index of a specific ally on the army
    def find_ally(self, ally):
        if not isinstance(ally, Ally):
            raise ValueError(f"Checking non Ally type. Got: {ally}")
        for i in self._army:
            if i == ally:
                return i
        raise ValueError("Checking Ally thats not in the army") # do we really wanna be this strict?

    def get_ally_at(self, index):
        return self._army[index] # errors on out of index, fine

    def in_army(self, ally):
        if not isinstance(ally, Ally):
            raise ValueError(f"Checking non Ally type. Got: {ally}")
        return ally in self._army
