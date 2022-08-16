import Hero
import time
import Tools
import random
import pygame
import settings
import os


#WIN = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT),pygame.FULLSCREEN, pygame.RESIZABLE)
#pygame.display.set_caption("Calebstone")
## below puts ricardo on full scale of the scren
#BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("avatars", "backgrounds", "ricardo.png")), (settings.WIDTH, settings.HEIGHT))

class GameManager:

    def __init__(self, player1Name="Caleb", player1Deck="CalebDeckList", player2Name="Dio", player2Deck="DioDeckList", typeGame="RandomvRandom"):
        self._player1 = Hero.Hero(hero=player1Name, deckList=player1Deck, leftSide=True) # player1 is human when possible
        self._player2 = Hero.Hero(hero=player2Name, deckList=player2Deck, leftSide=False) # player2 is random when possible
        self._typeGame = typeGame # RandomvRandom, HumanvRandom, RandomvRandom
        if typeGame == "RandomvRandom":
            self._output = open("Runs/output.txt", 'w+')
        else:
            self._output = print
        self._player1GoesFirst = False
        self._roundCounter = 0

        #def run(self):
        
        start = time.time()
        print("Starting Game...")
        if self._typeGame == "RandomvRandom":
            self.random_v_random()
        elif self._typeGame == "HumanvRandom":
            self.human_v_random()
        else:
            print("Incorrect game type given")
            return
        end = time.time()
        print("Ending Game...")
        #print(f"end run {i}\nelapsed time: {end - start}")

    def __del__(self) -> None:
        if self._output != print:
            self._output.close()

    def round_counter(self, roundNum=None):
        if roundNum:
            self._roundCounter = roundNum
        return self._roundCounter

    def start_of_game(self):
        # coin toss:
        # True -> hero first
        # False -> enemy first
        self._player1GoesFirst = Tools.coin_toss()
        if self._player1GoesFirst:
            lst1 = self._player1.draw_cards(3)
            lst2 = self._player2.draw_cards(4)
            self.output(f'{self._player1.name()} wins the coin toss.\n')
        else:
            lst1 = self._player2.draw_cards(3)
            lst2 = self._player1.draw_cards(4)
            self.output(f'{self._player2.name()} wins the coin toss.\n')
        for i in lst1:
            self.output(i)
        for j in lst2:
            self.output(j)

    def check_for_winner(self):
        if self._player1.health() <= 0 or self._player2.health() <= 0:
            return True
        else:
            return False

    def winner(self): # returns 3 with tie, 1 for player 1 win, 2 for player 2 win
        if self._player1.health() <= 0 and self._player2.health() <= 0:
            return 3
        elif self._player1.health() <= 0:
            return 1
        elif self._player2.health() <= 0:
            return 2

    def human_v_human(self):
        print('\nLet the games commence...\n')
        player1Turn = turn.HumanTurnManagaer(self._player1, self._player2)
        player2Turn = turn.HumanTurnManagaer(self._player2, self._player1)
        self._player1GoesFirst = self.start_of_game()

        # player1goesFirst = True if player1 wins coin toss
        self.round_counter(1)

        while self.check_for_winner() == False:
            print(f'Round {self.round_counter()}:')
            if self._player1GoesFirst:
                # Take your turns - player 1 then player 2
                # pass in round number to set gold for that turn
                player1Turn.full_turn(self.round_counter())
                if self.check_for_winner():
                    break
                player2Turn.full_turn(self.round_counter())
                if self.check_for_winner():
                    break
            else:
                # Take your turns - player 2 then player 1
                player2Turn.full_turn(self.round_counter())
                if self.check_for_winner():
                    break
                player1Turn.full_turn(self.round_counter())
                if self.check_for_winner():
                    break
            self._roundCounter += 1
        self.print_winner()

    def human_v_random(self):
        self.start_of_game()

        # player1goesFirst = True if player1 wins coin toss
        self.round_counter(1)

        while self.check_for_winner() == False:
            if self._player1GoesFirst:
                # Take your turns - player 1 then player 2
                # REMEMBER player1 is human when possible, p2 is random when possible
                # pass in round number to set gold for that turn
                self.full_turn(self._player1, self._player2, self.round_counter())
                if self.check_for_winner():
                    break
                self.random_full_turn(self._player2, self._player1, self.round_counter())
                if self.check_for_winner():
                    break
            else:
                # Take your turns - player 2 then player 1
                self.random_full_turn(self._player2, self._player1, self.round_counter())
                if self.check_for_winner():
                    break
                self.full_turn(self._player1, self._player2, self.round_counter())
                if self.check_for_winner():
                    break
            self._roundCounter += 1
        self.output_winner()

    def random_v_random(self): # must have file output
        self.start_of_game()

        # player1goesFirst = True if player1 wins coin toss
        self.round_counter(1)

        while self.check_for_winner() == False:
            if self._player1GoesFirst:
                # Take your turns - player 1 then player 2
                # pass in round number to set gold for that turn
                self.random_full_turn(self._player1, self._player2, self.round_counter())
                if self.check_for_winner():
                    break
                self.random_full_turn(self._player2, self._player1, self.round_counter())
                if self.check_for_winner():
                    break
            else:
                # Take your turns - player 2 then player 1
                self.random_full_turn(self._player2, self._player1, self.round_counter())
                if self.check_for_winner():
                    break
                self.random_full_turn(self._player1, self._player2, self.round_counter())
                if self.check_for_winner():
                    break
            self._roundCounter += 1
        self.output_winner()

# HUMAN ********************************************************************************************
# ALWAYS PRINT
    # this is full turn for human player 
    def full_turn(self, player, opposingPlayer, roundNumber):
        self.output('______________________________________________________________________________________________________________\n')
        self.output('It\'s ' + player.name() + '\'s turn!\n')
        self.output_hand(player)
        self.output(player.draw_card())
        # check if fatigue killed the hero
        if player.health() <= 0 or opposingPlayer.health() <= 0:
            self.end_turn(True)
            return

        # set player's gold to round number
        player.set_gold(roundNumber)
            
        self.output_gold(player)
        self.output_state(player, opposingPlayer)
        endTurn = False
        while endTurn == False:
            endTurn = self.turn_choice(player, opposingPlayer) # returns true when turn is over
        player.ready_up() # readies hero and army

    # Find out want the player wants to do and call correct function based on that choice
    def turn_choice(self, player, opposingPlayer):
        # While the player makes a doable choice i.e. This will loop uptil the player makes
        #                                              a choice that can actually be done
        answers = ('play card', 'attack', 'something else')
        turnChoice = Tools.get_input('\n|Enter your option|', answers)
        if turnChoice == answers[0]:
            return self.choice_play_card(player, opposingPlayer)
        elif turnChoice == answers[1]:
            return self.choice_attack(player, opposingPlayer)
        elif turnChoice == answers[2]:
            return self.choice_other(player, opposingPlayer)

        return True # shouldnt reach here

    # Give Player other options
    def choice_other(self, player, opposingPlayer):
        answers = ('end your turn', 'help', 'Game State', 'Deck',  'go back') # 'check hand', 'check gold', Not very useful
        while True:
            turnChoice = Tools.get_input('\n|Enter your option|', answers)
            if turnChoice == answers[0]:
                return True # ends turn
            elif turnChoice == answers[1]:
                self.get_help()
            elif turnChoice == answers[2]:
                self.output_state(player, opposingPlayer)
            elif turnChoice == answers[3]:
                self.check_deck(player)
            # elif turnChoice == answers[3]:        Not very useful :/
            #     self.check_hand()
            # elif turnChoice == answers[4]:        Not very useful :/
            #     self.print_gold()
            elif turnChoice == answers[4]:
                return False

    # Player wants to Attack with a friendly ally
    def choice_attack(self, player, opposingPlayer):
        tryAgain = True
        availableAttackers = []
        availableDefenders = []
        availableAttackers.append('Go Back')
        availableDefenders.append('Go Back')
        for i in player.available_targets():
            availableAttackers.append(i)
        for i in opposingPlayer.available_targets():
            availableDefenders.append(i)
        while tryAgain:
            attacker = Tools.get_input('|Attack with|', availableAttackers)
            if attacker == 'Go Back':
                return False
            elif attacker.is_ready():
                tryAgain = False
            else:
                print(f'{attacker.name()} is not ready!')
        defender = Tools.get_input('|Attack who|', availableDefenders)
        if defender == 'Go Back':
                return False
        print('|Attacking:|', defender.name(), '\n')
        print('|Attacking with:|', attacker.name(), '\n')
        attacker.attack_enemy(defender)
        if player.health() <= 0 or opposingPlayer.health() <= 0:
            return True 
        player.call_to_arms().toll_the_dead()
        opposingPlayer.call_to_arms().toll_the_dead()
        self.output_state(player, opposingPlayer)
        return False

    # Player wants to play a card
    def choice_play_card(self, player, opposingPlayer):
        # Does the hero have any cards
        if player.any_cards() == True:
            # Great! Now we can play a card
            # I want to play this card! Retrieve it from you hand
            hand = []
            hand.append('Go Back')
            for i in player._hand:
                hand.append(i)
            self.output_gold(player)
            playThisCard = Tools.get_input('Play which card:', hand)
            if playThisCard == 'Go Back':
                return False
            # Is this chosen card playable?
            elif player.playable_card(playThisCard) == False:
                print('That card costs too much gold')
                return False
            elif player.call_to_arms().full_army() == True:
                print('Your Army is Full!')
                return False
            else:
                player.play_ally(playThisCard)
                playThisCard.ready_down()
                print(playThisCard.name(), 'Get out there!\n')
                self.output_state(player, opposingPlayer)
                print('')
                return False
        # If you are over here, then you are not able to play a Card for some reason or other
        else:
            print('Your Hand is empty! Choose something else..\n')
            return False

    # To be implemented later
    def get_help(self):
        self.output('Never give up!\n')
        return False

    def check_deck(self, player):
        print(player.deck_list())
        return False

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

# HUMAN ********************************************************************************************
# OUTPUT ********************************************************************************************
    def output(self, text):
        if self._output == print:
            self._output(text)
        else: # fileOutput
            self._output.write(text)

    # Outputs who wins
    def output_winner(self):
        player1Lose = self._player1.health() <= 0
        player2Lose = self._player2.health() <= 0
        # tie
        if player1Lose and player2Lose:
            self.output('You both lose!')
        elif player1Lose:
            self.output(f'{self._player1.name()} loses!')
        elif player2Lose:
            self.output(f'{self._player2.name()} loses!')

    # Ouptus how much gold the hero has left
    def output_gold(self, player):
        self.output(f'You have {player.gold()} gold\n')

    # Outputs the current state of the game i.e. the Heros and Armies of both sides
    def output_state(self, player, opposingPlayer):
        self.output(f'{player}\t\t|\t{opposingPlayer}\n')

        # This gets the armies together to output in an intelligible way
        # I am least proud of these lines of code but hey they work
        heroCounter = 0
        enemyCounter = 0
        heroArmySize = player.call_to_arms().army_size()
        enemyArmySize = opposingPlayer.call_to_arms().army_size()
        largestArmy = max(heroArmySize, enemyArmySize)
        while heroCounter < largestArmy and enemyCounter < largestArmy:
            heroAlly = player.call_to_arms().get_ally_at(heroCounter)
            enemyAlly = opposingPlayer.call_to_arms().get_ally_at(enemyCounter)
            if heroAlly == None:
                #This mess of a string gets the spacing right
                heroAlly = '\t\t\t\t\t\t\t\t'
            
            if enemyAlly == None:
                #Same with this string
                enemyAlly = '\t\t\t\t\t\t\t\t'
            self.output(f'|{heroAlly}\t|{enemyAlly}|\n')
            heroCounter += 1
            enemyCounter += 1

    # Outputs current hand
    def output_hand(self, player):
        self.output('hand:\n')
        for card in player._hand:
            self.output(card._name + '\n')
# OUTPUT ********************************************************************************************
    def redraw_window(self):
        # draws background onto window at coordinate (0, 0)
        WIN.blit(BACKGROUND, (0, 0))

        #player dividing borders 
        pygame.draw.line(WIN, (255,255,255), (settings.WIDTH / 2, 0), ((settings.WIDTH / 2, settings.HEIGHT)), 5)
        #pygame.draw.line(WIN, (255,255,255), (0, settings.HEIGHT * 2 / 3), ((settings.WIDTH, settings.HEIGHT * 2 / 3)), 5)

        self._player1.draw(WIN)
        self._player1.draw_army(WIN) # side 1 = true

        self._player2.draw(WIN)
        self._player2.draw_army(WIN) # side 1 = false ie side 2

        pygame.display.update()
# RANDOM ********************************************************************************************
    # player, opposingPlayer, round
    def random_full_turn(self, player, opposingPlayer, roundNumber):
        self.output('______________________________________________________________________________________________________________\n')
        self.output('It\'s ' + player.name() + '\'s turn!\n')
        self.output_hand(player)
        self.output(player.draw_card())
        # check is fatigue killed the hero
        if player.health() <= 0 or opposingPlayer.health() <= 0:
            self.end_turn(True)
            return

        # set player's gold to round number
        player.set_gold(roundNumber)
            
        self.output_gold(player)
        self.output_state(player, opposingPlayer)
        endTurn = False
        while endTurn == False:
            endTurn = self.random_choice(player, opposingPlayer) # returns true when turn is over
        player.ready_up() # readies hero and army
        
    # Randomly find out want the player wants to do and call correct function based on that choice
    def random_choice(self, player, opposingPlayer):
        # while you can play cards
        while player.playable_cards():
            # randomly play a card until out, no gold or board full
            while player.playable_cards():
                self.random_play_card(player)

            # while you can attack # are there any available attackers? return bool
            while player._army.available_attackers() or player._ready == True:
                self.random_attack(player, opposingPlayer)
            # attack
        # in case you cant play cards but can attack
        while player._army.available_attackers() or player._ready == True:
            self.random_attack(player, opposingPlayer)

        # end turn
        return True # endTurn = True

    # play a random card in hand
    def random_play_card(self, player):
        playable_hand = player.playable_hand()
        choice = random.randint(0, len(playable_hand) - 1)
        player.play_ally(playable_hand[choice])
        self.output(player._name + " played " + playable_hand[choice]._name + "\n")

    # randomly attack a random target
    def random_attack(self, player, opposingPlayer):
        availableAttackers = player.available_attackers()
        availableDefenders = opposingPlayer.available_targets()

        attacker = availableAttackers[random.randint(0, len(availableAttackers) - 1)]
        defender = availableDefenders[random.randint(0, len(availableDefenders) - 1)]

        self.output('***********FIGHT***********\n')
        self.output_state(player, opposingPlayer)
        self.output('|Attacking:|' + defender.name() + '\n')
        self.output('|Attacking with:|' + attacker.name() + '\n')
        attacker.attack_enemy(defender)
        if player.health() <= 0 or opposingPlayer.health() <= 0:
            return True # stops the turn
        player.call_to_arms().toll_the_dead()
        opposingPlayer.call_to_arms().toll_the_dead()
        self.output_state(player, opposingPlayer)
        self.output('***********FIGHT***********\n')
# RANDOM ********************************************************************************************

def main():
    GameManager()

if __name__ == "__main__":
    main()