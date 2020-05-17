import Hero as Hero
import Tools as Tools


class TurnManager:
    def __init__(self, hero, enemy):
        self._hero = hero
        self._enemy = enemy
        self._return = True
        self._endTurn = False

    def startOfGame(self):
        # coin toss:
        # True -> hero first
        # False -> enemy first
        heroFirst = Tools.coinToss()
        if heroFirst:
            self._hero.draw_cards(4)
            self._enemy.draw_cards(5)
            return True
        else:
            self._enemy.draw_cards(4)
            self._hero.draw_cards(5)
            return False

    def fullTurn(self, gold):
        # set hero's gold to round number
        self._hero.gold(gold)
        self._endTurn = False
        self._hero.draw_card()
        while self.endTurn() == False:
            self.turnChoice()

    # Find out want the player wants to do and call correct function based on that choice
    # ********************TO IMPLEMENT*************************ADD H OPTION - HAND INFORMATION***************
    # ********************TO IMPLEMENT*************************ADD B OPTION - BOARD INFORMATION***************
    # ********************TO IMPLEMENT*************************ADD E OPTION - ENEMY INFORMATION***************
    # ********************TO IMPLEMENT*************************ADD H OPTION - HERO INFORMATION***************
    def turnChoice(self):
        print('\nIt\'s ' + self._hero.hero_name() + '\'s turn!\n')
        # While the player makes a doable choice i.e. This will loop uptil the player makes
        #                                              a choice that can actually be done
        self._return = True
        while self._return:
            answers = ('attack', 'play card', 'something else')
            turnChoice = Tools.get_input('|Enter your option|', answers)
            if turnChoice == answers[0]:
                self.choiceAttack()
            elif turnChoice == answers[1]:
                self.choicePlayCard()
            elif turnChoice == answers[2]:
                self.choiceOther()

    # Player wants to Attack with a friendly ally
    def choiceAttack(self):
        if self._hero.get_board_size() != 0:
            attacker = Tools.get_input('|Attack with|', self._hero.available_targets())
            print('|Attacking with:|\n', '~_', attacker)
            defender = Tools.get_input('|Attack who|', self._enemy.available_targets())
            print('|Attacking:|\n~_', defender)

            self._return = False
        else:
            print('Your Board is empty! Choose something else..\n')
            self._return = True

    # Player wants to play a card
    def choicePlayCard(self):
        # Does the player have enough Gold to play any of their cards
        if self._hero.any_cards() == True:
            # Does the hero have any cards
            if self._hero.playable_cards() == True:
                
                # Great! Now we can play a card
                # I want to play this card! Retrieve it from you hand
                playThisCard = Tools.get_input('Play which card:', self._hero._hand)
                # Is this chosen card playable?
                if self._hero.playable_card(playThisCard) == False:
                    print('That card costs too much gold\n')
                    return
                self._hero.play_ally(playThisCard)
                print(playThisCard.name(), 'Get out there!\n')
                print('This is your army looks like now:')
                self._hero.print_army()
                self._return = False
            # If you are over here, then you are not able to play a Card for some reason or other
            else:
                print('You don\'t have enough gold to play any of your cards! Choose something else..\n')
                self._return = True
        else:
            print('Your Hand is empty! Choose something else..\n')
            self._return = True

    def choiceOther(self):
        while self._return:
            answers = ('end your turn', 'help', 'board info', 'go back')
            turnChoice = Tools.get_input('|Enter your option|', answers)
            if turnChoice == answers[0]:
                self.endTurn(True)
                self._return = False
                return
            elif turnChoice == answers[1]:
                self.getHelp()
                return
            elif turnChoice == answers[2]:
                self.printState()
                return
            elif turnChoice == answers[3]:
                return
            # elif turnChoice == 'a':
            #     self.choiceAttack()
            # elif turnChoice == 'p':
            #     self.choicePlayCard()
            # else:
            #     print('What?\n')
            #     return2

    def endTurn(self, boola=None):
        if boola:
            self._endTurn = boola
        return self._endTurn

    # To be implemented later
    def getHelp(self):
        print('Never give up!\n')

    def printState(self):
        print(f'''
~__{self._hero}
~__{self._enemy}
''')
        print(f'|{self._hero.hero_name()}\'s board|')
        for i in self._hero.call_to_arms().get_board():
            print(i)
        print(f'|{self._hero.hero_name()}\'s board|')
        print(f'|{self._enemy.hero_name()}\'s board|')
        for i in self._enemy.call_to_arms().get_board():
            print(i)
        print(f'|{self._enemy.hero_name()}\'s board|')


def main():
    caleb = Hero.Hero(hero='caleb')
    caleb.gold(10)
    caleb.deck_list('DeckLists/CalebDeckList.txt')
    caleb.draw_cards(5)
    dio = Hero.Hero(hero='dio')
    dio.gold(10)
    dio.deck_list('DeckLists/DioDeckList.txt')

    turn = TurnManager(caleb, dio)
    turn.fullTurn(10)


if __name__ == "__main__":
    main()
