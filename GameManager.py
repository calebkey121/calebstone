from Hero import Hero
import time
import Tools
import random
import pygame
import settings
import os
import Card
import DeckLists.BearDeckList as Bear
import DeckLists.WolfDeckList as Wolf
import DeckLists.SpiderDeckList as Spider

class GameManager:

    def __init__(self, player1Name="Necromancer", player1Deck=Wolf.deck_list, player2Name="Skeleton Wizard", player2Deck=Bear.deck_list):
        self._player1 = Hero(hero=player1Name, deckList=player1Deck, side1=False) # player1 is human when possible
        self._player1._yourTurn = True
        self._player2 = Hero(hero=player2Name, deckList=player2Deck, side1=True) # player2 is random when possible
        # typegame is always human v random
        self._player1GoesFirst = False
        self._roundCounter = 0
        self._currentTurn = 1 # set back to 0 # 0 -> not in game, 1 -> player1 turn, 2 -> player2 turn
        self._endTurnButton = settings.sub_font.render(f"End Turn", 1, settings.white)
        self._endTurnRect = None
        self._selectedCard = None # a card is selected
        self._selectingHand = False # used to tell if we should highlight board or not
        self._showText = False # True when you want to show text
        self._board1 = None
        self._board2 = None

        # PYGAME Setup
        self.WIN = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT),pygame.FULLSCREEN | pygame.RESIZABLE)
        pygame.display.set_caption("Calebstone")
        self.BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("avatars", "backgrounds", "b1.jpg")), (settings.WIDTH, settings.HEIGHT))

        self.run_game()

    def run_game(self):
        print("Starting Game...")
        self.start_of_game()

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
                    
                    if self._currentTurn == 1: # must be player1's turn (human)
                        #self._player1._yourTurn = True # may need for later
                        if self._endTurnRect.collidepoint(pos):
                            self.endTurn()

                        # These check if you're clicking the respective sprite(s)
                        if self.select_enemy(pos): # check this first
                            pass
                        elif self.select_player1(pos):
                            pass
                        elif self.select_board(pos): # Are you playing a card or selecting an ally?
                            pass
                        elif self.select_card(pos): # Card in hand?
                            pass
                        else: self.unselect()
            
            if self.check_for_winner(): run = False

        print("Ending Game...", self.winner(), "won!")

# SELECTING FUNCTIONS ******************************************************************************************
    def select(self, target):
        self._selectedCard = target
        target.select()

        if type(target) == Hero:
            if target == self._player1:
                if target.is_ready():
                    self._player2.target_all()
        elif type(target) == Card.Ally:
            if self._player1.in_army(target):
                if target.is_ready():
                    self._player2.target_all()
            
    def unselect(self):
        target = self._selectedCard # Default to self._selectedCard
        if target:
            target.unselect()

            if type(target) == Hero:
                self._player2.untarget_all()
            elif type(target) == Card.Ally:
                if self._player1.in_army(target) or self._player2.in_army(target):
                    self._player2.untarget_all()
                elif self._player1.in_hand(target):
                    pass
            self._showText = False
            self._selectingHand = False
            self._selectedCard = None

    def select_player1(self, mousePos):
        if self._player1._sprite.collidepoint(mousePos):
            if self._selectedCard != self._player1:
                self.unselect()
            if self._selectedCard == self._player1: # if you are clicking a second time
                self._showText = True
            self.select(self._player1)
            return True
        return False

    def select_card(self, mousePos):
        for card in self._player1._hand:
            if card._sprite:
                if card._sprite.collidepoint(mousePos):
                    if self._selectedCard != card:
                        self.unselect()
                    elif self._selectedCard == card: # if you are clicking a second time
                        self._showText = True
                    
                    self.select(card)
                    self._selectingHand = True
                    return True
        return False

    def select_board(self, mousePos):
        if self._board1.collidepoint(mousePos):
            # if you currently are selecting your hand, then you're trying to play a card when you click the board
            # make sure its a card in your hand (could be an attacker or hero or enemy ally)
            if self._player1.in_hand(self._selectedCard):
                if not self._player1.play_ally(self._selectedCard): # play selected card
                    self.unselect() # if you cant play, unselect card
                    return False
            else: # if you are not currently selecting your hand, then try to select an ally
                return self.select_ally(mousePos) # Ally in Army on Board
        return False
   
    def select_ally(self, mousePos):
        for ally in self._player1.army():
            if ally._sprite:
                if ally._sprite.collidepoint(mousePos):
                    if self._selectedCard != ally:
                        self.unselect()
                    elif self._selectedCard == ally: # if you are clicking a second time
                        self._showText = True
                    self.select(ally)
                    return True
        return False

    def select_enemy(self, mousePos):
        if self._player2._sprite.collidepoint(mousePos):
            if self._player1.in_army(self._selectedCard) or self._selectedCard == self._player1: # if the current selected card is in the army
                self._selectedCard.attack_enemy(self._player2, attackingPlayer=self._player1)
                self._player1.call_to_arms().toll_the_dead()
                self._player2.call_to_arms().toll_the_dead()
                self.unselect()
            else: # otherwise, select just to look at card
                if self._selectedCard != self._player2:
                    self.unselect()
                if self._selectedCard == self._player2: # if you are clicking a second time
                    self._showText = True
                self.select(self._player2)
            return True
        else:
            for enemyAlly in self._player2.army():
                if enemyAlly._sprite:
                    if enemyAlly._sprite.collidepoint(mousePos):
                        if self._player1.in_army(self._selectedCard) or self._selectedCard == self._player1:
                            self._selectedCard.attack_enemy(enemyAlly, attackingPlayer=self._player1)
                            self._player1.call_to_arms().toll_the_dead()
                            self._player2.call_to_arms().toll_the_dead()
                            self.unselect()
                        else:
                            if self._selectedCard != enemyAlly:
                                self.unselect()
                            elif self._selectedCard == enemyAlly: # if you are clicking a second time
                                self._showText = True
                            self.select(enemyAlly)
                        return True
        return False
# **************************************************************************************************************
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

# **************************************************************************************************************
# HUMAN ********************************************************************************************************

# **************************************************************************************************************
# PYGAME *******************************************************************************************************
    def redraw_window(self):
        # draws background onto window at coordinate (0, 0)
        self.WIN.blit(self.BACKGROUND, (0, 0))

        #player dividing borders 
        pygame.draw.line(self.WIN, settings.white, (0, settings.HEIGHT / 2), (settings.WIDTH, settings.HEIGHT / 2), 5) # horizontak line down the middle
        pygame.draw.line(self.WIN, settings.white, (settings.endHeroZone, 0), (settings.endHeroZone, settings.HEIGHT), 5)
        # board / hand lines
        self._board1 = pygame.Rect(settings.endHeroZone, settings.HEIGHT / 2, settings.WIDTH - settings.endHeroZone, settings.HEIGHT / 4)
        self._board2 = pygame.Rect(settings.endHeroZone, settings.HEIGHT / 4, settings.WIDTH - settings.endHeroZone, settings.HEIGHT / 4)
        board1BorderColor = settings.white
        board2BorderColor = settings.white
        if self._selectingHand:
            board1BorderColor = settings.targeted_color
        pygame.draw.rect(self.WIN, board1BorderColor, self._board1, settings.card_border_size)
        pygame.draw.rect(self.WIN, board2BorderColor, self._board2, settings.card_border_size)


        # Game Stats ##########################
        # Player 1 Gold 
        gold_p1 = settings.sub_font.render(f"Gold: {self._player1.gold()}", 1, settings.gold)
        gold_p1X = 0
        gold_p1Y = settings.HEIGHT - gold_p1.get_height()
        gold_p1_rect = pygame.Rect(gold_p1X, gold_p1Y, gold_p1.get_width(), gold_p1.get_height())
        pygame.draw.rect(self.WIN, settings.dark_grey, gold_p1_rect) # BACKDROP
        self.WIN.blit(gold_p1, gold_p1_rect)
        # Player 1 Income
        income_p1 = settings.sub_font.render(f"Income: {self._player1.income()}", 1, settings.gold)
        income_p1X = 0
        income_p1Y = settings.HEIGHT - gold_p1.get_height() - income_p1.get_height()
        income_p1_rect = pygame.Rect(income_p1X, income_p1Y, income_p1.get_width(), income_p1.get_height())
        pygame.draw.rect(self.WIN, settings.dark_grey, income_p1_rect) # BACKDROP
        self.WIN.blit(income_p1, income_p1_rect)
        # Player 2 Gold 
        gold_p2 = settings.sub_font.render(f"Gold: {self._player2.gold()}", 1, settings.gold)
        gold_p2X = 0
        gold_p2Y = 0
        gold_p2_rect = pygame.Rect(gold_p2X, gold_p2Y, gold_p2.get_width(), gold_p2.get_height())
        pygame.draw.rect(self.WIN, settings.dark_grey, gold_p2_rect) # BACKDROP
        self.WIN.blit(gold_p2, gold_p2_rect)
        # Player 2 Income
        income_p2 = settings.sub_font.render(f"Income: {self._player2.income()}", 1, settings.gold)
        income_p2X = 0
        income_p2Y = gold_p2.get_height()
        income_p2_rect = pygame.Rect(income_p2X, income_p2Y, income_p2.get_width(), income_p2.get_height())
        pygame.draw.rect(self.WIN, settings.dark_grey, income_p2_rect) # BACKDROP
        self.WIN.blit(income_p2, income_p2_rect)
        # Round 
        round_label = settings.sub_font.render(f"Round: {self._roundCounter}", 1, settings.white) # better way to choose rgb? is needed??
        roundX = settings.endHeroZone - round_label.get_width()
        roundY = 0
        round_rect = pygame.Rect(roundX, roundY, round_label.get_width(), round_label.get_height())
        pygame.draw.rect(self.WIN, settings.dark_grey, round_rect) # BACKDROP
        self.WIN.blit(round_label, round_rect)
        # End Turn Button
        self._endTurnRect = pygame.Rect(settings.endHeroZone - self._endTurnButton.get_width(), settings.HEIGHT - self._endTurnButton.get_height(), self._endTurnButton.get_width(), self._endTurnButton.get_height())
        self.WIN.blit(self._endTurnButton, self._endTurnRect)
        pygame.draw.rect(self.WIN, settings.white, self._endTurnRect, 5)
        ###########################################

        self._player1.draw(self.WIN)
        self._player1.draw_army(self.WIN) # side 1 = true
        self._player1.draw_deck(self.WIN)
        self._player1.draw_hand(self.WIN)

        self._player2.draw(self.WIN)
        self._player2.draw_army(self.WIN) # side 1 = false ie side 2
        self._player2.draw_deck(self.WIN)
        self._player2.draw_hand(self.WIN, hidden=True) # typically say hidden=True

        # Show text box if you have a selected card
        if self._selectedCard:
            if self._showText:
                if self._selectedCard._text:
                    self._selectedCard.draw_text_window(self.WIN)

        pygame.display.update()
# **************************************************************************************************************
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
        self._player2.play_ally(playable_hand[choice])

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
