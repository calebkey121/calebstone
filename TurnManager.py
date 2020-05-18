import Hero as hero
import Tools as tools

class TurnManager:
    def __init__(self, hero, enemy):
        self._hero = hero
        self._enemy = enemy
        self._endTurn = False

    def start_of_game(self):
        # coin toss:
        # True -> hero first
        # False -> enemy first
        heroFirst = tools.coin_toss()
        if heroFirst:
            self._hero.draw_cards(4)
            self._enemy.draw_cards(5)
            return True
        else:
            self._enemy.draw_cards(4)
            self._hero.draw_cards(5)
            return False

    def full_turn(self, roundNumber):
        print('\nIt\'s ' + self._hero.name() + '\'s turn!')
        self.print_state()

        # set hero's gold to round number
        if roundNumber < 10:
            self._hero.gold(roundNumber)
        else:
            self._hero.gold(10)
        self.print_gold()

        self._endTurn = False
        self._hero.draw_card()
        while self.end_turn() == False:
            self.turn_choice()
        for i in self._hero.available_targets():
            i.ready_up()

    # Find out want the player wants to do and call correct function based on that choice
    # ********************TO IMPLEMENT*************************ADD H OPTION - HAND INFORMATION***************
    # ********************TO IMPLEMENT*************************ADD B OPTION - Army INFORMATION***************
    # ********************TO IMPLEMENT*************************ADD E OPTION - ENEMY INFORMATION***************
    # ********************TO IMPLEMENT*************************ADD H OPTION - HERO INFORMATION***************
    def turn_choice(self):
        # While the player makes a doable choice i.e. This will loop uptil the player makes
        #                                              a choice that can actually be done
        answers = ('attack', 'play card', 'something else')
        turnChoice = tools.get_input('|Enter your option|', answers)
        if turnChoice == answers[0]:
            self.choice_attack()
        elif turnChoice == answers[1]:
            self.choice_play_card()
        elif turnChoice == answers[2]:
            self.choice_other()

    # Player wants to Attack with a friendly ally
    def choice_attack(self):
        tryAgain = True
        availableAttackers = self._hero.available_targets()
        availableDefenders = self._enemy.available_targets()
        availableAttackers.append('Go Back')
        availableDefenders.append('Go Back')
        while tryAgain:
            attacker = tools.get_input('|Attack with|', availableAttackers)
            if attacker == 'Go Back':
                return
            elif attacker.is_ready():
                tryAgain = False
            else:
                print(f'{attacker.name()} is not ready!')
        defender = tools.get_input('|Attack who|', availableDefenders)
        if defender == 'Go Back':
                return
        print('|Attacking:|', defender.name(), '\n')
        print('|Attacking with:|', attacker.name(), '\n')
        attacker.attack_enemy(defender)
        self.print_state()

    # Player wants to play a card
    def choice_play_card(self):
        # Does the player have enough Gold to play any of their cards
        if self._hero.any_cards() == True:
            # Does the hero have any cards
            if self._hero.playable_cards() == True:
                
                # Great! Now we can play a card
                # I want to play this card! Retrieve it from you hand
                playThisCard = tools.get_input('Play which card:', self._hero._hand)
                # Is this chosen card playable?
                if self._hero.playable_card(playThisCard) == False:
                    print('That card costs too much gold\n')
                    return
                self._hero.play_ally(playThisCard)
                playThisCard.ready_down()
                print(playThisCard.name(), 'Get out there!\n')
                print('This is your army looks like now:')
                self._hero.print_army()
                print('')
            # If you are over here, then you are not able to play a Card for some reason or other
            else:
                print('You don\'t have enough gold to play any of your cards! Choose something else..\n')
        else:
            print('Your Hand is empty! Choose something else..\n')

    def choice_other(self):
        answers = ('end your turn', 'help', 'Game State', 'go back')
        turnChoice = tools.get_input('|Enter your option|', answers)
        if turnChoice == answers[0]:
            self.end_turn(True)
            return
        elif turnChoice == answers[1]:
            self.get_help()
            return
        elif turnChoice == answers[2]:
            self.print_state()
            return
        elif turnChoice == answers[3]:
            return


    def end_turn(self, boola=None):
        if boola:
            self._endTurn = boola
        return self._endTurn

    # To be implemented later
    def get_help(self):
        print('Never give up!\n')

    def print_gold(self):
        print(f'You have {self._hero.gold()} gold')

    def print_state(self):
        print(f'\t{self._hero}       |\t{self._enemy}\n')
        for i, j in zip(self._hero.call_to_arms().get_army(), self._enemy.call_to_arms().get_army()):
            print(f'{i}|{j}\n')

        # print(f'|{self._hero.name()}\'s Army|')
        # for i in self._hero.call_to_arms().getArmy():
        #     print(i)
        # print(f'|{self._hero.name()}\'s Army|')
        # print(f'|{self._enemy.name()}\'s Army|')
        # for i in self._enemy.call_to_arms().getArmy():
        #     print(i)
        # print(f'|{self._enemy.name()}\'s Army|\n')


def main():
    pass

if __name__ == "__main__":
    main()
            