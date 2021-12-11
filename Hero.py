import pygame
import os
import settings
from Army import Army
from Deck import Deck
from Card import Ally

# This represents the player - Human or AI
class Hero:
    def __init__(self, **kwargs):
        # Heros are the player and hold all the variables that the player will have in game
        # In the future, I want the heros to be unique, here the just have the following:
        # :: Name, Health, Gold, Deck(of cards), Hand(of cards), and related variables
        self._name = kwargs['hero']
        self._deckList = Deck(kwargs['deckList'])
        self._army = Army()
        self._avatar = pygame.transform.scale(pygame.image.load(os.path.join("avatars", "heros", self._name + ".png")), (settings.WIDTH / 5, settings.HEIGHT / 5))
        self._health = 30
        self._attack = 0
        self._ready = False
        self._gold = 0
        self._hand = []
        self._maxHandSize = 10

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
            self._deckList.import_txt(deckList)
        return self._deckList

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
    def draw_card(self, output = False):
        if len(self._hand) < self.max_hand_size():
            # CASE: Out of Cards!! Take damage equal to the amount of cards that you have overdrawn
            if self.deck_list().get_current_num_cards() <= 0:
                damage = self._deckList.draw_card(self._hand)
                if not output:
                    print(f'Fatigue: {-damage} damage delt to {self.name()}')
                else: 
                    return (f'Fatigue: {-damage} damage delt to {self.name()}')
                self._health += damage
            else:
                draw = self._deckList.draw_card(self._hand)
                if not output:
                    print(self.name() + ' drew ' + draw.name() + '\n')
                else:
                    return (self.name() + ' drew ' + draw.name() + '\n')
        else:
            if self.deck_list().get_current_num_cards() > 0:
                if not output:
                    print(self._name + '\'s hand is too full!')
                    print(self._name + ' burned:', self._deckList.burn_card())
                else:
                    return (self._name + '\'s hand is too full!\n' + self._name + ' burned:' + self._deckList.burn_card())
            else:
                damage = self._deckList.draw_card(self._hand)
                if not output:
                    print(f'Fatigue: {-damage} damage delt to {self.name()}')
                else:
                    return (f'Fatigue: {-damage} damage delt to {self.name()}')
                self._health += damage

    def draw_cards(self, number, output = False):
        for i in range(number):
            self.draw_card(output)

    # Playing Cards!!!
    def play_ally(self, card):
        self._army.add_ally(card)
        card.ready_down()
        self._gold -= card.cost()
        self.remove_from_hand(card)

    # Gold Management
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
        if (self._ready and (self._attack > 0)):
            available_attackers.append(self)
        for i in self._army._army:
            if (i._ready and (i._attack > 0)):
                available_attackers.append(i)
        return available_attackers

    def ready_up(self):
        if self._attack > 0:
            self._ready = True
        for card in self._army._army:
            card.ready_up()


    def ready_down(self):
        self._ready = False

    def is_ready(self):
        return self._ready

    # Representation - Weird String is me trying to make the output look cool
    def __repr__(self):
        return f'~__{self.name()}__~ \tAttack: {self.attack():2d} \tHealth: {self.health():2d}'

class player1(Hero):
    def draw(self, WIN):
        # Players Avatar
        defaultX = 10
        defaultY = (settings.HEIGHT / 2) - (self._avatar.get_height() / 2)
        WIN.blit(self._avatar, (10, defaultY))

        # Stat Labels
        health_label = settings.main_font.render(f"{self._health}", 1, (255,0,0)) # better way to choose rgb? is needed??
        gold_label = settings.main_font.render(f"{self._gold}", 1, (255,188,0)) # better way to choose rgb? is needed??
        name_label = settings.main_font.render(f"{self._name}", 1, (255,255,255)) # better way to choose rgb? is needed??

        # Stat Area
        pygame.draw.rect(WIN, (30, 30, 30), (defaultX, defaultY + self._avatar.get_height(), self._avatar.get_width(), health_label.get_height())) # BACKDROP
        pygame.draw.rect(WIN, (200, 200, 200), (defaultX, defaultY + self._avatar.get_height(), self._avatar.get_width(), health_label.get_height()), 5) # BORDER
        pygame.draw.line(WIN, (200, 200, 200), (defaultX + self._avatar.get_width() / 2, defaultY + self._avatar.get_height()), (defaultX + self._avatar.get_width() / 2, defaultY + self._avatar.get_height() + health_label.get_height()), 5) # HEALTH / GOLD
        # Player Health
        WIN.blit(health_label, (defaultX + self._avatar.get_width() / 4 - health_label.get_width() / 2, defaultY + self._avatar.get_height()))
        WIN.blit(gold_label, (defaultX + self._avatar.get_width() * 3 / 4 - gold_label.get_width() / 2, defaultY + self._avatar.get_height()))
       
        # Name Area
        pygame.draw.rect(WIN, (30, 30, 30), (defaultX, defaultY - name_label.get_height(), self._avatar.get_width(), name_label.get_height())) # BACKDROP
        pygame.draw.rect(WIN, (200, 200, 200), (defaultX, defaultY - name_label.get_height(), self._avatar.get_width(), name_label.get_height()), 5) # BORDER
        WIN.blit(name_label, (defaultX + self._avatar.get_width() / 2 - name_label.get_width() / 2, defaultY - name_label.get_height()))

        # Final Border
        pygame.draw.rect(WIN, (255,255,255), (10, defaultY, self._avatar.get_width(), self._avatar.get_height()), 5)

    def draw_army(self, WIN, side1):

        example = self._deckList._deckList[0]
        x = settings.WIDTH / 2 - (settings.WIDTH / 2 - (10 + self._avatar.get_width())) / 2
        temp = 1 # replace temp with self._army.army_size()
        y = settings.HEIGHT / 2 - example._avatar.get_height() * temp / 2


        """ if temp == 0:
            pass
        elif temp == 1:
            y = settings.HEIGHT / 2 - example._avatar.get_height() / 2
        elif temp == 2:
            y = settings.HEIGHT / 2 - example._avatar.get_height()
        elif temp == 3:
            pass
        elif temp == 4:
            pass
        elif temp == 5:
            pass
        elif temp == 6:
            pass """

        for idx in range(temp):
            played_card = self._deckList._deckList[idx]
            played_card.draw(WIN, x - played_card._avatar.get_width() / 2, y, side1)
            y += played_card._avatar.get_height()

class player2(Hero):
    def draw(self, WIN):
        # Players Avatar
        defaultX = settings.WIDTH - 10 - self._avatar.get_width()
        defaultY = (settings.HEIGHT / 2) - (self._avatar.get_height() / 2)
        WIN.blit(self._avatar, (settings.WIDTH - self._avatar.get_width() - 10, defaultY))

        # Stat Labels
        health_label = settings.main_font.render(f"{self._health}", 1, (255,0,0)) # better way to choose rgb? is needed??
        gold_label = settings.main_font.render(f"{self._gold}", 1, (255,188,0)) # better way to choose rgb? is needed??
        name_label = settings.main_font.render(f"{self._name}", 1, (255,255,255)) # better way to choose rgb? is needed??
        
        # Stat Area
        pygame.draw.rect(WIN, (30, 30, 30), (defaultX, defaultY + self._avatar.get_height(), self._avatar.get_width(), health_label.get_height())) # BACKDROP
        pygame.draw.rect(WIN, (200, 200, 200), (defaultX, defaultY + self._avatar.get_height(), self._avatar.get_width(), health_label.get_height()), 5) # BORDER
        pygame.draw.line(WIN, (200, 200, 200), (defaultX + self._avatar.get_width() / 2, defaultY + self._avatar.get_height()), (defaultX + self._avatar.get_width() / 2, defaultY + self._avatar.get_height() + health_label.get_height()), 5) # HEALTH / GOLD
        WIN.blit(health_label, (defaultX + self._avatar.get_width() / 4 - health_label.get_width() / 2, defaultY + self._avatar.get_height()))
        WIN.blit(gold_label, (defaultX + self._avatar.get_width() * 3 / 4 - gold_label.get_width() / 2, defaultY + self._avatar.get_height()))
        
        # Name Area
        pygame.draw.rect(WIN, (30, 30, 30), (defaultX, defaultY - name_label.get_height(), self._avatar.get_width(), name_label.get_height())) # BACKDROP
        pygame.draw.rect(WIN, (200, 200, 200), (defaultX, defaultY - name_label.get_height(), self._avatar.get_width(), name_label.get_height()), 5) # BORDER
        WIN.blit(name_label, (defaultX + self._avatar.get_width() / 2 - name_label.get_width() / 2, defaultY - name_label.get_height()))
        
        # Final Border
        pygame.draw.rect(WIN, (255,255,255), (settings.WIDTH - 10 - self._avatar.get_width(), defaultY, self._avatar.get_width(), self._avatar.get_height()), 5)

    def draw_army(self, WIN, side1):
        example = self._deckList._deckList[0]
        x = settings.WIDTH / 2 + (settings.WIDTH / 2 - (10 + self._avatar.get_width())) / 2
        temp = 3 # replace temp with self._army.army_size()
        y = settings.HEIGHT / 2 - example._avatar.get_height() * temp / 2


        """ if temp == 0:
            pass
        elif temp == 1:
            y = settings.HEIGHT / 2 - example._avatar.get_height() / 2
        elif temp == 2:
            y = settings.HEIGHT / 2 - example._avatar.get_height()
        elif temp == 3:
            pass
        elif temp == 4:
            pass
        elif temp == 5:
            pass
        elif temp == 6:
            pass """

        for idx in range(temp):
            played_card = self._deckList._deckList[idx]
            played_card.draw(WIN, x - played_card._avatar.get_width() / 2, y, side1)
            y += played_card._avatar.get_height()