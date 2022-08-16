import Hero
import time
import Tools
import random
import pygame
import settings
import os
import Card



class GameManager:

    def __init__(self, player1Name="Wolf", player1Deck="CalebDeckList", player2Name="Bear", player2Deck="DioDeckList"):
        self._player1 = Hero.Hero(hero=player1Name, deckList=player1Deck, leftSide=True) # player1 is human when possible
        self._player2 = Hero.Hero(hero=player2Name, deckList=player2Deck, leftSide=False) # player2 is random when possible
        # typegame is always human v random
        self._player1GoesFirst = False
        self._roundCounter = 0
        self._currentTurn = 1 # 0 -> not in game, 1 -> player1 turn, 2 -> player2 turn

        # remove later newAlly = Ally(name=inputCard[0], cost=int(inputCard[1]), attack=int(inputCard[2]), health=int(inputCard[3]))
        card = Card.Ally(name="test name1", cost=2, attack=22, health=22)
        self._player1._army.add_ally(card)
        card.ready_up()

        card = Card.Ally(name="test name2", cost=3, attack=33, health=33)
        self._player1._army.add_ally(card)
        card.ready_up()

        card = Card.Ally(name="test name3", cost=5, attack=55, health=55)
        self._player2._army.add_ally(card)
        card.ready_up()

        # remove later

        # PYGAME
        self.WIN = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT),pygame.FULLSCREEN, pygame.RESIZABLE)
        pygame.display.set_caption("Calebstone")
        self.BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("avatars", "backgrounds", "b1.jpg")), (settings.WIDTH, settings.HEIGHT))

    def run_game(self):
        print("Starting Game...")
        #self.start_of_game()

        run = True
        FPS = 60
        clock = pygame.time.Clock()

        while run:
            clock.tick(FPS)
            self.redraw_window()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    
                    if self._currentTurn == 1:
                        if self._player1._sprite.collidepoint(pos):
                            self._player1.select()
                        else:
                            self._player1.unselect()
                        if self._player2._sprite.collidepoint(pos):
                            self._player2.select()
                        else:
                            self._player2.unselect()
                        for ally in self._player1._army.get_army():
                            if ally._sprite.collidepoint(pos):
                                ally.select()
                            else:
                                ally.unselect()
                        for ally in self._player2._army.get_army():
                            if ally._sprite.collidepoint(pos):
                                ally.select()
                            else:
                                ally.unselect()
                    else: 
                        # continue cpu's turn
                        pass

        print("Ending Game...")

    def run_turns(self):
        if self._currentTurn == 1:
            # player 1 turn
            self.human_turn()
        else:
            # computer turn
            self.random_turn
        self._roundCounter += 1

# GAME FUNCS ********************************************************************************************
    def start_of_game(self):
        # coin toss:
        # True -> hero first
        # False -> enemy first
        self._player1GoesFirst = Tools.coin_toss()
        if self._player1GoesFirst:
            self._currentTurn = 1
            self._player1.draw_cards(3)
            self._player2.draw_cards(4)
        else:
            self._currentTurn = 2
            self._player2.draw_cards(3)
            self._player1.draw_cards(4)
        self.round_counter(1)

    def round_counter(self, roundNum=None):
        if roundNum:
            self._roundCounter = roundNum
        return self._roundCounter

    def check_for_winner(self):
        if self._player1.health() <= 0 or self._player2.health() <= 0:
            # output winner and close everything
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
# GAME FUNCS ********************************************************************************************
# HUMAN ********************************************************************************************
    # this is full turn for human player 
    def human_turn(self):
        self._player1.draw_card()
        # check if fatigue killed the hero
        if self._player1.health() <= 0:
            self.end_turn(True)
            return
        # set player's gold to round number
        self._player1.set_gold(self._roundCounter)
        endTurn = False
        while endTurn == False:
            endTurn = self.turn_choice() # returns true when turn is over
        self._player1.ready_up() # readies hero and army

    # Find out want the player wants to do and call correct function based on that choice
    def turn_choice(self):
        # While the player makes a doable choice i.e. This will loop uptil the player makes
        #                                              a choice that can actually be done
        answers = ('play card', 'attack', 'something else')
        turnChoice = Tools.get_input('\n|Enter your option|', answers)
        if turnChoice == answers[0]:
            return self.choice_play_card()
        elif turnChoice == answers[1]:
            return self.choice_attack()
        elif turnChoice == answers[2]:
            return self.choice_other()

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

# HUMAN ********************************************************************************************
# PYGAME ********************************************************************************************
    def redraw_window(self):
        # draws background onto window at coordinate (0, 0)
        self.WIN.blit(self.BACKGROUND, (0, 0))

        #player dividing borders 
        pygame.draw.line(self.WIN, (255,255,255), (settings.WIDTH / 2, 0), ((settings.WIDTH / 2, settings.HEIGHT)), 5)
        #pygame.draw.line(WIN, (255,255,255), (0, settings.HEIGHT * 2 / 3), ((settings.WIDTH, settings.HEIGHT * 2 / 3)), 5)

        self._player1.draw(self.WIN)
        self._player1.draw_army(self.WIN) # side 1 = true

        self._player2.draw(self.WIN)
        self._player2.draw_army(self.WIN) # side 1 = false ie side 2

        pygame.display.update()


# PYGAME ********************************************************************************************
# RANDOM ********************************************************************************************
# Random player is always self._player2, human is always self._player1
    # player, opposingPlayer, round
    def random_turn(self):
        self._player2.draw_card()
        # check is fatigue killed the hero
        if self._player2.health() <= 0:
            self.end_turn(True)
            return

        # set player's gold to round number
        self._player2.set_gold(self._roundCounter)

        endTurn = False
        while endTurn == False:
            endTurn = self.random_choice() # returns true when turn is over
        self._player2.ready_up() # readies hero and army
        
    # Randomly find out want the player wants to do and call correct function based on that choice
    def random_choice(self):
        # while you can play cards
        while self._player2.playable_cards():
            # randomly play a card until out, no gold or board full
            while self._player2.playable_cards():
                self.random_play_card()

            # while you can attack # are there any available attackers? return bool
            while self._player2._army.available_attackers() or self._player2._ready == True:
                self.random_attack()
            # attack
        # in case you cant play cards but can attack
        while self._player2._army.available_attackers() or self._player2._ready == True:
            self.random_attack()

        # end turn
        return True # endTurn = True

    # play a random card in hand
    def random_play_card(self):
        playable_hand = self._player2.playable_hand()
        choice = random.randint(0, len(playable_hand) - 1)
        self._player2.play_ally(playable_hand[choice])

    # randomly attack a random target
    def random_attack(self):
        availableAttackers = self._player2.available_attackers()
        availableDefenders = self._player1.available_targets()

        attacker = availableAttackers[random.randint(0, len(availableAttackers) - 1)]
        defender = availableDefenders[random.randint(0, len(availableDefenders) - 1)]

        attacker.attack_enemy(defender)
        if self._player2.health() <= 0 or self._player1.health() <= 0:
            return True # stops the turn
        self._player2.call_to_arms().toll_the_dead()
        self._player1.call_to_arms().toll_the_dead()
# RANDOM ********************************************************************************************

def main():
    game = GameManager()
    game.run_game()

if __name__ == "__main__":
    main()