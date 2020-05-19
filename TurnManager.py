import Hero as Hero
import Tools as Tools

class TurnManager:
    def __init__(self, hero, enemy):
        self._hero = hero
        self._enemy = enemy
        self._endTurn = False

    def start_of_game(self):
        # coin toss:
        # True -> hero first
        # False -> enemy first
        heroFirst = Tools.coin_toss()
        if heroFirst:
            self._hero.draw_cards(3)
            self._enemy.draw_cards(4)
            return True
        else:
            self._enemy.draw_cards(3)
            self._hero.draw_cards(4)
            return False

    def full_turn(self, roundNumber):
        print('\nIt\'s ' + self._hero.name() + '\'s turn!')
        self._hero.draw_card()
        # check is fatigue killed the hero
        if self._hero.health() <= 0 or self._enemy.health() <= 0:
            self.end_turn(True)
            return

        # set hero's gold to round number
        if roundNumber < 10:
            self._hero.gold(roundNumber)
        else:
            self._hero.gold(10)
        self.print_gold()
        self.print_state()
        self._endTurn = False
        while self.end_turn() == False:
            self.turn_choice()
        for i in self._hero.available_targets():
            i.ready_up()

    # Find out want the player wants to do and call correct function based on that choice
    def turn_choice(self):
        # While the player makes a doable choice i.e. This will loop uptil the player makes
        #                                              a choice that can actually be done
        answers = ('attack', 'play card', 'something else')
        turnChoice = Tools.get_input('\n|Enter your option|', answers)
        if turnChoice == answers[0]:
            self.choice_attack()
        elif turnChoice == answers[1]:
            self.choice_play_card()
        elif turnChoice == answers[2]:
            self.choice_other()

    # Give Player other options
    def choice_other(self):
        answers = ('end your turn', 'help', 'Game State',  'check hand', 'check gold', 'go back')
        returnOther = True
        while returnOther:
            turnChoice = Tools.get_input('\n|Enter your option|', answers)
            if turnChoice == answers[0]:
                self.end_turn(True)
                return
            elif turnChoice == answers[1]:
                self.get_help()
            elif turnChoice == answers[2]:
                self.print_state()
            elif turnChoice == answers[3]:
                self.check_hand()
            elif turnChoice == answers[4]:
                self.print_gold()
            elif turnChoice == answers[5]:
                return

    # Player wants to Attack with a friendly ally
    def choice_attack(self):
        tryAgain = True
        availableAttackers = []
        availableDefenders = []
        availableAttackers.append('Go Back')
        availableDefenders.append('Go Back')
        for i in self._hero.available_targets():
            availableAttackers.append(i)
        for i in self._enemy.available_targets():
            availableDefenders.append(i)
        while tryAgain:
            attacker = Tools.get_input('|Attack with|', availableAttackers)
            if attacker == 'Go Back':
                return
            elif attacker.is_ready():
                tryAgain = False
            else:
                print(f'{attacker.name()} is not ready!')
        defender = Tools.get_input('|Attack who|', availableDefenders)
        if defender == 'Go Back':
                return
        print('|Attacking:|', defender.name(), '\n')
        print('|Attacking with:|', attacker.name(), '\n')
        attacker.attack_enemy(defender)
        if self._hero.health() <= 0 or self._enemy.health() <= 0:
            self.end_turn(True)
            return
        self._hero.call_to_arms().toll_the_dead()
        self._enemy.call_to_arms().toll_the_dead()
        self.print_state()

    # Player wants to play a card
    def choice_play_card(self):
        # Does the hero have any cards
        if self._hero.any_cards() == True:
            # Great! Now we can play a card
            # I want to play this card! Retrieve it from you hand
            hand = []
            hand.append('Go Back')
            for i in self._hero._hand:
                hand.append(i)
            self.print_gold()
            playThisCard = Tools.get_input('Play which card:', hand)
            if playThisCard == 'Go Back':
                return
            # Is this chosen card playable?
            elif self._hero.playable_card(playThisCard) == False:
                print('That card costs too much gold')
                return
            elif self._hero.call_to_arms().full_army() == True:
                print('Your Army is Full!')
                return
            else:
                self._hero.play_ally(playThisCard)
                playThisCard.ready_down()
                print(playThisCard.name(), 'Get out there!\n')
                self.print_state()
                print('')
        # If you are over here, then you are not able to play a Card for some reason or other
        else:
            print('Your Hand is empty! Choose something else..\n')

    # End the current turn
    def end_turn(self, boola=None):
        if boola:
            self._endTurn = boola
        return self._endTurn

    # To be implemented later
    def get_help(self):
        print('Never give up!\n')

    # Prints how much gold the hero has left
    def print_gold(self):
        print(f'You have {self._hero.gold()} gold')

    # Gives the cards currently in the heros hand
    def check_hand(self):
        self.print_gold()
        self._hero.print_hand()
        print('')

    # Prints the current state of the game i.e. the Heros and Armies of both sides
    def print_state(self):
        print(f'\t\t{self._hero}\t\t|\t{self._enemy}\n')

        # This gets the armies together to output in an intelligible way
        # I am least proud of these lines of code but hey they work
        heroCounter = 0
        enemyCounter = 0
        heroArmySize = self._hero.call_to_arms().army_size()
        enemyArmySize = self._enemy.call_to_arms().army_size()
        largestArmy = max(heroArmySize, enemyArmySize)
        while heroCounter < largestArmy and enemyCounter < largestArmy:
            heroAlly = self._hero.call_to_arms().get_ally_at(heroCounter)
            enemyAlly = self._enemy.call_to_arms().get_ally_at(enemyCounter)
            if heroAlly == None:
                #This mess of a string gets the spacing right
                heroAlly = '\t\t\t\t\t\t\t\t'
            
            if enemyAlly == None:
                #Same with this string
                enemyAlly = '\t\t\t\t\t\t\t\t  '
            print(f'|{heroAlly}\t|{enemyAlly}|')
            heroCounter += 1
            enemyCounter += 1
        print('___________________________________________________________________________________________________________________________________________')


def main():
    pass

if __name__ == "__main__":
    main()
            