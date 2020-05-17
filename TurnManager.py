import Hero as hero
import Tools as tools

class TurnManager:
    def __init__(self, hero, enemy):
        self._hero = hero
        self._enemy = enemy
        self._endTurn = False

    def startOfGame(self):
        # coin toss:
        # True -> hero first
        # False -> enemy first
        heroFirst = tools.coinToss()
        if heroFirst:
            self._hero.drawCards(4)
            self._enemy.drawCards(5)
            return True
        else:
            self._enemy.drawCards(4)
            self._hero.drawCards(5)
            return False

    def fullTurn(self, roundNumber):
        print('\nIt\'s ' + self._hero.name() + '\'s turn!')
        self.printState()

        # set hero's gold to round number
        if roundNumber < 10:
            self._hero.gold(roundNumber)
        else:
            self._hero.gold(10)
        self.print_gold()

        self._endTurn = False
        self._hero.drawCard()
        while self.endTurn() == False:
            self.turnChoice()
        for i in self._hero.availableTargets():
            i.readyUp()

    # Find out want the player wants to do and call correct function based on that choice
    # ********************TO IMPLEMENT*************************ADD H OPTION - HAND INFORMATION***************
    # ********************TO IMPLEMENT*************************ADD B OPTION - Army INFORMATION***************
    # ********************TO IMPLEMENT*************************ADD E OPTION - ENEMY INFORMATION***************
    # ********************TO IMPLEMENT*************************ADD H OPTION - HERO INFORMATION***************
    def turnChoice(self):
        # While the player makes a doable choice i.e. This will loop uptil the player makes
        #                                              a choice that can actually be done
        answers = ('attack', 'play card', 'something else')
        turnChoice = tools.get_input('|Enter your option|', answers)
        if turnChoice == answers[0]:
            self.choiceAttack()
        elif turnChoice == answers[1]:
            self.choicePlayCard()
        elif turnChoice == answers[2]:
            self.choiceOther()

    # Player wants to Attack with a friendly ally
    def choiceAttack(self):
        tryAgain = True
        availableAttackers = self._hero.availableTargets()
        availableDefenders = self._enemy.availableTargets()
        availableAttackers.append('Go Back')
        availableDefenders.append('Go Back')
        while tryAgain:
            attacker = tools.get_input('|Attack with|', availableAttackers)
            if attacker == 'Go Back':
                return
            elif attacker.isReady():
                tryAgain = False
            else:
                print(f'{attacker.name()} is not ready!')
        defender = tools.get_input('|Attack who|', availableDefenders)
        if defender == 'Go Back':
                return
        print('|Attacking:|', defender.name(), '\n')
        print('|Attacking with:|', attacker.name(), '\n')
        attacker.attackEnemy(defender)
        self.printState()

    # Player wants to play a card
    def choicePlayCard(self):
        # Does the player have enough Gold to play any of their cards
        if self._hero.anyCards() == True:
            # Does the hero have any cards
            if self._hero.playableCards() == True:
                
                # Great! Now we can play a card
                # I want to play this card! Retrieve it from you hand
                playThisCard = tools.get_input('Play which card:', self._hero._hand)
                # Is this chosen card playable?
                if self._hero.playableCard(playThisCard) == False:
                    print('That card costs too much gold\n')
                    return
                self._hero.playAlly(playThisCard)
                playThisCard.readyDown()
                print(playThisCard.name(), 'Get out there!\n')
                print('This is your army looks like now:')
                self._hero.printArmy()
                print('')
            # If you are over here, then you are not able to play a Card for some reason or other
            else:
                print('You don\'t have enough gold to play any of your cards! Choose something else..\n')
        else:
            print('Your Hand is empty! Choose something else..\n')

    def choiceOther(self):
        answers = ('end your turn', 'help', 'Game State', 'go back')
        turnChoice = tools.get_input('|Enter your option|', answers)
        if turnChoice == answers[0]:
            self.endTurn(True)
            return
        elif turnChoice == answers[1]:
            self.getHelp()
            return
        elif turnChoice == answers[2]:
            self.printState()
            return
        elif turnChoice == answers[3]:
            return


    def endTurn(self, boola=None):
        if boola:
            self._endTurn = boola
        return self._endTurn

    # To be implemented later
    def getHelp(self):
        print('Never give up!\n')

    def print_gold(self):
        print(f'You have {self._hero.gold()} gold')

    def printState(self):
        print(f'\t{self._hero}       |\t{self._enemy}\n')
        for i, j in zip(self._hero.callToArms().getArmy(), self._enemy.callToArms().getArmy()):
            print(f'{i}|{j}\n')

        # print(f'|{self._hero.name()}\'s Army|')
        # for i in self._hero.callToArms().getArmy():
        #     print(i)
        # print(f'|{self._hero.name()}\'s Army|')
        # print(f'|{self._enemy.name()}\'s Army|')
        # for i in self._enemy.callToArms().getArmy():
        #     print(i)
        # print(f'|{self._enemy.name()}\'s Army|\n')


def main():
    pass

if __name__ == "__main__":
    main()
            