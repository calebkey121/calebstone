import pygame
import os
import settings
from Army import Army
from Deck import Deck
import Card
from Card import Card

# This represents the player - Human or AI
class Hero:
    def __init__(self, **kwargs): # must
        # Heros are the player and hold all the variables that the player will have in game
        # In the future, I want the heros to be unique, here the just have the following:
        # :: Name, Health, Gold, Deck(of cards), Hand(of cards), and related variables
        self._name = kwargs['hero']
        self._deck = Deck(kwargs['deckList'])
        self._army = Army()
        self._avatar = pygame.transform.scale(pygame.image.load(os.path.join("avatars", "heros", self._name + ".png")), (settings.hero_size[0], settings.hero_size[1] - settings.main_font.get_height() * 2))
        self._health = 30
        self._attack = 0
        self._gold = 0
        self._hand = []
        self._maxHandSize = 7
        self._side1 = kwargs['side1'] # says if the hero is on the left or right side
        self._sprite = None

        self._ready = False
        self._targeted = False
        self._selected = False
        self._yourTurn = False # is it your turn

    # Hero's Army Functions
    def call_to_arms(self, ally=None):
        if ally:
            self._army.add_ally(ally)
        return self._army

    def attack(self, attack=None):
        if attack:
            self._attack = attack
        return self._attack

    def get_army_size(self):
        return self.call_to_arms().army_size()

    # Hand Functions
    def max_hand_size(self, newSize=None):
        if newSize:
            self._maxHandSize = newSize
        return self._maxHandSize

    def current_hand_size(self):
        return len(self._hand)

    def print_hand(self):
        for i, j in enumerate(self._hand):
            print(f'{i+1}: {j}')

    def remove_from_hand(self, card):
        for i in self._hand:
            if i == card:
                self._hand.remove(i)

    def attack_enemy(self, enemy):
        if self._ready:
            if self.attack() >= 0:
                enemy.lower_health(self.attack())
            if enemy.attack() >= 0:
                self.lower_health(enemy.attack())
            self.ready_down()
        else:
            print(f'{self.name()} is not ready!')

    def get_from_hand(self, position):
        return self._hand[position]

    def any_cards(self):
        if len(self._hand) > 0:
            return True
        else:
            return False

    # Variable Changing
    def deck_list(self, deckList=None):
        if deckList:
            self._deck.import_txt(deckList)
        return self._deck

    def gold(self, income=None):
        if income:
            self._gold = income
        return self._gold

    def name(self, name=None):
        if name:
            self._name = name
        return self._name
    
    def health(self, health=None):
        if health:
            self._health = health
        return self._health

    def lower_health(self, attackVal):
        self._health -= attackVal

    # Card Draw
    def draw_card(self):
        # CASE: Your hand is NOT FULL
        if len(self._hand) < self.max_hand_size():
            # CASE: Out of Cards!! Take damage equal to the amount of cards that you have overdrawn
            if self.deck_list().get_current_num_cards() <= 0:
                damage = self._deck.draw_card(self._hand)
                self._health += damage
                return (f'Fatigue: {-damage} damage delt to {self.name()}')
            else:
                draw = self._deck.draw_card(self._hand)
                return (self.name() + ' drew ' + draw.name() + '\n')
        # CASE: Your hand is FULL
        else:
            if self.deck_list().get_current_num_cards() > 0:
                return (self._name + '\'s hand is too full!\n' + self._name + ' burned:' + self._deck.burn_card())
            else:
                damage = self._deck.draw_card(self._hand)
                self._health += damage
                return (f'Fatigue: {-damage} damage delt to {self.name()}')

    def draw_cards(self, number):
        drawnCards = []
        for i in range(number):
            drawnCards.append(self.draw_card())
        return drawnCards

    # Playing Cards!!!
    def play_ally(self, card):
        if not self._army.is_full() and card._cost <= self._gold:
            self._army.add_ally(card)
            card.ready_down()
            self._gold -= card.cost()
            self.remove_from_hand(card)
        else: return None # unsuccessful

    # Gold Management
    def set_gold(self, roundNumber):
        if roundNumber < 10:
            self.gold(roundNumber)
        else:
            self.gold(10)

    # Are there any playable cards in my hand?
    def playable_cards(self):
        playable = False
        for i in self._hand:
            if i.cost() <= self._gold:
                playable = True
        return playable

    # Is this card playable?
    def playable_card(self, card):
        playable = False
        if card.cost() <= self.gold():
            playable = True
        return playable

    def playable_hand(self):
        playable = []
        for i in self._hand:
            if i.cost() <= self._gold:
                playable.append(i)
        return playable

    def available_targets(self):
        availableTargets = []
        availableTargets.append(self)
        for i in self._army._army:
            availableTargets.append(i)
        return availableTargets

    def available_attackers(self):
        available_attackers = []
        if (self._ready and (self._attack >= 0)):
            available_attackers.append(self)
        for i in self._army._army:
            if (i._ready and (i._attack > 0)):
                available_attackers.append(i)
        return available_attackers

    def ready_up(self):
        if self._attack >= 0:
            self._ready = True
        for card in self._army._army:
            card.ready_up()

    def ready_down(self):
        self._ready = False

    def is_ready(self):
        return self._ready

    def select(self):
        self._selected = True
    
    def unselect(self):
        self._selected = False

    def target_all(self):
        self._targeted = True
        for ally in self._army.get_army():
            ally._targeted = True
            
    def untarget_all(self):
        self._targeted = False
        for ally in self._army.get_army():
            ally._targeted = False

# PYGAME DRAW FUNCTIONS ********************************************************************************************
    def draw(self, WIN):

        # Players Avatar
        x = settings.hero_zone_buffer
        if self._side1:
            y = settings.HEIGHT / 2 - settings.hero_zone_buffer - settings.hero_size[1]
        else:
            y = settings.HEIGHT / 2 + settings.hero_zone_buffer
        WIN.blit(self._avatar, (x, y + settings.main_font.get_height()))

        # Stat Area
        # Player Health
        health_label = settings.main_font.render(f"{self._health}", 1, settings.health_color) 
        health_rect = pygame.Rect(x, y + settings.hero_size[1] - health_label.get_height(), settings.hero_size[0] / 2, health_label.get_height())
        pygame.draw.rect(WIN, settings.dark_grey, health_rect) # Backdrop
        pygame.draw.rect(WIN, settings.light_grey, health_rect, 5) # Border
        WIN.blit(health_label, (x + self._avatar.get_width() / 4 - health_label.get_width() / 2, y + settings.hero_size[1] - settings.main_font.get_height()))

        # Player Attack
        attack_label = settings.main_font.render(f"{self._attack}", 1, settings.attack_color)
        attack_rect = pygame.Rect(x + settings.hero_size[0] / 2, y + settings.hero_size[1] - health_label.get_height(), settings.hero_size[0] / 2, health_label.get_height())
        pygame.draw.rect(WIN, settings.dark_grey, attack_rect) # Backdrop
        pygame.draw.rect(WIN, settings.light_grey, attack_rect, settings.card_border_size) # Border
        WIN.blit(attack_label, (x + self._avatar.get_width() * 3 / 4 - attack_label.get_width() / 2, y + settings.hero_size[1] - settings.main_font.get_height()))
        
        # Player Name
        name_label = settings.main_font.render(f"{self._name}", 1, settings.white)
        name_rect = pygame.Rect(x, y, settings.hero_size[0], name_label.get_height())
        pygame.draw.rect(WIN, settings.dark_grey, name_rect) # BACKDROP
        pygame.draw.rect(WIN, settings.light_grey, name_rect, settings.card_border_size) # BORDER
        WIN.blit(name_label, (x + settings.hero_size[0] / 2 - name_label.get_width() / 2, y))
        
        # Final Border
        finalBorderColor = settings.light_grey
        if self._ready and self._yourTurn:
            finalBorderColor = settings.ready_color
        if self._selected and self._yourTurn:
            finalBorderColor = settings.selected_color
        if self._targeted:
            finalBorderColor = settings.targeted_color
        if self._side1:
            self._sprite = pygame.Rect(x, y, settings.hero_size[0], settings.hero_size[1])
        else:
            self._sprite = pygame.Rect(x, y, settings.hero_size[0], settings.hero_size[1])
        pygame.draw.rect(WIN, finalBorderColor, self._sprite, 5)

    def draw_army(self, WIN):
        # example to get the size of card and label
        if (self._side1):
            y = settings.HEIGHT / 2 - (settings.card_zone_buffer + settings.card_size[1])
        else: y = (settings.HEIGHT / 2) + settings.card_zone_buffer

        armySize = self.get_army_size()
        # left side is cut off, lets get that starting point
        starting_point = 2 * settings.hero_zone_buffer + self._avatar.get_width()
        middle = (settings.WIDTH + starting_point) / 2
        settings.card_buffer = 5

        x = middle - (settings.card_size[0] / 2) * armySize
        x -= settings.card_buffer * (armySize - 1)
        for card in self._army.get_army():
            card.draw(WIN, x, y, self._yourTurn)
            x += card._avatar.get_width()
            x += settings.card_buffer * 2

    def draw_deck(self, WIN):

        if self._deck._deckList == []:
            pass 
            # deck is empty, display something saying that
        else: # deck is not empty
            x = settings.WIDTH - settings.card_zone_buffer - settings.card_size[0]
            y = settings.card_zone_buffer
            if not self._side1:
                y = settings.HEIGHT - settings.card_zone_buffer - settings.card_size[1]
            Card.draw_card_back(WIN, x, y)
        remaining_cards = settings.small_font.render(f"Remaining Cards:{self._deck.get_current_num_cards()}", 1, settings.white)
        WIN.blit(remaining_cards, (x + settings.card_size[0] / 2 - remaining_cards.get_width() / 2, y + settings.card_buffer))

    def draw_hand(self, WIN, hidden=False):
        if self._hand == []:
            pass 
            # hand is empty, display something saying that
        else: # hand is not empty
            x = settings.endHeroZone + settings.card_zone_buffer
            y = settings.card_zone_buffer
            if not self._side1:
                y = settings.HEIGHT - settings.card_zone_buffer - settings.card_size[1]
            for card in self._hand:
                if hidden:
                    Card.draw_card_back(WIN, x, y)
                else: card.draw(WIN, x, y, self._yourTurn)
                x += settings.card_size[0] + settings.card_buffer
