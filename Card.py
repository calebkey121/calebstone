
class Card:
    def __init__(self, **kwargs):
        self._cost = kwargs['cost'] if 'cost' in kwargs else -1
        self._name = kwargs['name'] if 'name' in kwargs else 'No Name'
        self._ready = False

    def name(self, name=None):
        if name:
            self._name = name
        return self._name

    def cost(self, cost=None):
        if cost:
            self._cost = cost
        return self._cost

    # def __repr__(self):
    #     return f'
    #     Card: {self.name()}
    #     Cost: {self.cost()}
    #     '
        

class Ally(Card):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._attack = kwargs['attack'] if 'attack' in kwargs else 0
        self._health = kwargs['health'] if 'health' in kwargs else 0
        self._ready = False

    def attack(self, a=None):
        if a:
            self._attack = a
        return self._attack

    def health(self, h=None):
        if isinstance(h, int):
            self._health = h
        return self._health

    def lowerHealth(self, attackVal):
        self._health -= attackVal

    def readyUp(self):
        self._ready = True

    def readyDown(self):
        self._ready = False

    def isReady(self):
        return self._ready

    def attackEnemy(self, enemy):
        if self._ready:
            if self.attack() >= 0:
                enemy.lowerHealth(self.attack())
            if enemy.attack() >= 0:
                self.lowerHealth(enemy.attack())
            self.readyDown()
        else:
            print(f'{self.name()} is not ready!')

    # Representation - Weird String is me trying to make the output look cool
    def __repr__(self):
        return f'~__{self.name()}__~ \tCost: {self.cost()} \tAttack: {self.attack()} \tHealth: {self.health()}'

def main():
    pass

if __name__ == '__main__':
    main()
