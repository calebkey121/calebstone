from tkinter import X
from .Hero import Hero
import time
import archive.Tools as Tools
import random
import pygame
import settings
import os
import Card
import DeckLists.PlayerOneList as p1
import DeckLists.PlayerTwoList as p2
#import DeckLists.SpiderDeckList as Spider

class GameManager:

    def __init__(self, player1Name="Plague Doctor", player1Deck=p1.deck_list, player2Name="Black Knight", player2Deck=p2.deck_list):
        self._player1 = Hero(hero=player1Name, deckList=player1Deck, side1=False) # player1 is human when possible
        self._player1._yourTurn = True
        self._player2 = Hero(hero=player2Name, deckList=player2Deck, side1=True) # player2 is random when possible
        self._player1GoesFirst = False
        self._roundCounter = 0
        self._currentTurn = 1 # set back to 0 # 0 -> not in game, 1 -> player1 turn, 2 -> player2 turn
        self.run_game()

    def run_game(self):
        print("Starting Game...")
        self.start_of_game()

        run = True
        while run:
            
            if self.check_for_winner():
                run = False

        print("Ending Game...", self.winner(), "won!")

# GAME FUNCS ***************************************************************************************************
    def start_of_game(self):
        # coin toss:
        # True -> hero first
        # False -> enemy first
        self._player1GoesFirst = Tools.coin_toss()
        if self._player1GoesFirst:
            #self._currentTurn = 1
            self._player1.draw_cards(3)
            self._player2.draw_cards(4)
        else:
            #self._currentTurn = 2
            self._player2.draw_cards(3)
            self._player1.draw_cards(4)
        self.round_counter(1)
        self._player1.set_gold(1)
        self._player2.set_gold(1)

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
            return self._player2._name
        elif self._player2.health() <= 0:
            return self._player1._name

    def endTurn(self): # function that is called when end turn is clicked
        if not self._player1GoesFirst: # if you went first, then the next player is in the same round (dont increment)
            self._roundCounter += 1

        # enemy takes their turn
        self._currentTurn = 2
        self.random_turn()
        self._currentTurn = 1

        # start your next turn
        if self._player1GoesFirst:
            self._roundCounter += 1
        self._player1.set_gold(self._roundCounter)
        self._player1.ready_up()
        self._player1.draw_card()

# RANDOM *******************************************************************************************************
# Random player is always self._player2, human is always self._player1
    # player, opposingPlayer, round
    def random_turn(self):
        self._player2.draw_card()
        # check is fatigue killed the hero
        # if self._player2.health() <= 0:
        #     self.end_turn(True)
        #     return

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
        self._player2.play_ally(playable_hand[choice], opposingPlayer=self._player1)

    # attack a random target
    def random_attack(self):
        availableAttackers = self._player2.available_attackers()
        availableDefenders = self._player1.available_targets()

        attacker = availableAttackers[random.randint(0, len(availableAttackers) - 1)]
        defender = availableDefenders[random.randint(0, len(availableDefenders) - 1)]

        attacker.attack_enemy(defender, attackingPlayer=self._player2)
        if self._player2.health() <= 0 or self._player1.health() <= 0:
            return True # stops the turn
        self._player2.call_to_arms().toll_the_dead()
        self._player1.call_to_arms().toll_the_dead()
# **************************************************************************************************************

def main():
    game = GameManager()

if __name__ == "__main__":
    main()
