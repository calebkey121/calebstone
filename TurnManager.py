import Hero as Hero
import Tools as Tools
import random

class TurnManager:
    def __init__(self, hero, enemy):
        self._hero = hero
        self._enemy = enemy
        self._endTurn = False

class HumanTurnManagaer(TurnManager):

    # Make this silent
    def start_of_game(self):
        # coin toss:
        # True -> hero first
        # False -> enemy first
        heroFirst = Tools.coin_toss()
        if heroFirst:
            print(f'{self._hero.name()} wins the coin toss.\n')
            self._hero.draw_cards(3, output=False)
            self._enemy.draw_cards(4, output=False)
            return True
        else:
            print(f'{self._enemy.name()} wins the coin toss.\n')
            self._enemy.draw_cards(3, output=False)
            self._hero.draw_cards(4, output=False)
            return False

    def full_turn(self, roundNumber):
        print('\nIt\'s ' + self._hero.name() + '\'s turn!')
        self._hero.draw_card(output=False)
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
        while self._endTurn == False:
            self.turn_choice()
        self._hero.ready_up() # readies hero and army

    # Find out want the player wants to do and call correct function based on that choice
    def turn_choice(self):
        # While the player makes a doable choice i.e. This will loop uptil the player makes
        #                                              a choice that can actually be done
        answers = ('play card', 'attack', 'something else')
        turnChoice = Tools.get_input('\n|Enter your option|', answers)
        if turnChoice == answers[0]:
            self.choice_play_card()
        elif turnChoice == answers[1]:
            self.choice_attack()
        elif turnChoice == answers[2]:
            self.choice_other()

    # Give Player other options
    def choice_other(self):
        answers = ('end your turn', 'help', 'Game State', 'Deck',  'go back') # 'check hand', 'check gold', Not very useful
        returnOther = True
        while returnOther:
            turnChoice = Tools.get_input('\n|Enter your option|', answers)
            if turnChoice == answers[0]:
                self._endTurn = True
                return
            elif turnChoice == answers[1]:
                self.get_help()
            elif turnChoice == answers[2]:
                self.print_state()
            elif turnChoice == answers[3]:
                self.check_deck()
            # elif turnChoice == answers[3]:        Not very useful :/
            #     self.check_hand()
            # elif turnChoice == answers[4]:        Not very useful :/
            #     self.print_gold()
            elif turnChoice == answers[4]:
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
            self._endTurn = True
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

    ## End the current turn
    #    def end_turn(self, boola=None):
    #        if boola:
    #            self._endTurn = boola
    #        return self._endTurn

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

    def check_deck(self):
        print(self._hero.deck_list())

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


# # Implementing Random
class RandomTurnManager(TurnManager):
    def __init__(self, hero, enemy, output_file):
        self._hero = hero
        self._enemy = enemy
        self._endTurn = False
        self._output = output_file

    #def __del__(self):
    #    self._output.close()

    # Make this silent
    def start_of_game(self):
        # coin toss:
        # True -> hero first
        # False -> enemy first
        heroFirst = Tools.coin_toss()
        if heroFirst:
            self._output.write(f'{self._hero.name()} wins the coin toss.\n')
            for i in range(3):
                self._output.write(self._hero.draw_card(output=True))
            for i in range(4):
                self._output.write(self._enemy.draw_card(output=True))
            return True
        else:
            self._output.write(f'{self._enemy.name()} wins the coin toss.\n')
            for i in range(3):
                self._output.write(self._enemy.draw_card(output=True))
            for i in range(4):
                self._output.write(self._hero.draw_card(output=True))
            return False

    def full_turn(self, roundNumber):
        self._output.write('______________________________________________________________________________________________________________\n')
        self._output.write('It\'s ' + self._hero.name() + '\'s turn!\n')
        self.output_hand()
        self._output.write(self._hero.draw_card(output=True))
        # check is fatigue killed the hero
        if self._hero.health() <= 0 or self._enemy.health() <= 0:
            self.end_turn(True)
            return

        # set hero's gold to round number
        if roundNumber < 10:
            self._hero.gold(roundNumber)
        else:
            self._hero.gold(10)
        self.output_gold()
        self.output_state()
        self._endTurn = False
        while self._endTurn == False:
            self.random_choice()
        self._hero.ready_up() # readies hero and army

    # Ouptus how much gold the hero has left
    def output_gold(self):
        self._output.write(f'You have {self._hero.gold()} gold\n')

    # Outputs the current state of the game i.e. the Heros and Armies of both sides
    def output_state(self):
        self._output.write(f'{self._hero}\t\t|\t{self._enemy}\n')

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
                enemyAlly = '\t\t\t\t\t\t\t\t'
            self._output.write(f'|{heroAlly}\t|{enemyAlly}|\n')
            heroCounter += 1
            enemyCounter += 1

    def output_hand(self):
        self._output.write('hand:\n')
        for card in self._hero._hand:
            self._output.write(card._name + '\n')

    # Randomly find out want the player wants to do and call correct function based on that choice
    def random_choice(self):
        # while you can play cards
        while self.playable_cards():
            # randomly play a card until out, no gold or board full
            while self.playable_cards():
                self.random_play_card()

            # while you can attack # are there any available attackers? return bool
            while self._hero._army.available_attackers() or self._hero._ready == True:
                self.random_attack()
            # attack
        # in case you cant play cards but can attack
        while self._hero._army.available_attackers() or self._hero._ready == True:
            self.random_attack()

        # end turn
        self._endTurn = True

    # are there any playable cards? return bool
    def playable_cards(self):
        # Does the hero have any cards
        playable = False
        if self._hero.any_cards() == True:
            # Great! We have cards - lets see if we can play any
            if self._hero.playable_cards() == True and self._hero.call_to_arms().full_army() == False:
                playable = True # you have enough gold AND space to play
        # If you are over here, then you are not able to play a Card for some reason or other
        return playable

    # play a random card in hand
    def random_play_card(self):
        playable_hand = self._hero.playable_hand()
        choice = random.randint(0, len(playable_hand) - 1)
        self._hero.play_ally(playable_hand[choice])
        self._output.write(self._hero._name + " played " + playable_hand[choice]._name + "\n")

    # randomly attack a random target
    def random_attack(self):
        availableAttackers = self._hero.available_attackers()
        availableDefenders = self._enemy.available_targets()

        attacker = availableAttackers[random.randint(0, len(availableAttackers) - 1)]
        defender = availableDefenders[random.randint(0, len(availableDefenders) - 1)]

        self._output.write('***********FIGHT***********\n')
        self.output_state()
        self._output.write('|Attacking:|' + defender.name() + '\n')
        self._output.write('|Attacking with:|' + attacker.name() + '\n')
        attacker.attack_enemy(defender)
        if self._hero.health() <= 0 or self._enemy.health() <= 0:
            self._endTurn = True
            return
        self._hero.call_to_arms().toll_the_dead()
        self._enemy.call_to_arms().toll_the_dead()
        self.output_state()
        self._output.write('***********FIGHT***********\n')

def main():
    pass

if __name__ == "__main__":
    main()
            