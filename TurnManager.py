import Hero as Hero
import Tools as Tools


class TurnManager:
    def __init__(self, hero, enemy):
        self._hero = hero
        self._enemy = enemy
        self._return = True
        self._endTurn = False

    def start_of_game(self):
        # coin toss:
        # True -> hero first
        # False -> enemy first
        hero_first = Tools.coin_toss()
        if hero_first:
            self._hero.draw_cards(4)
            self._enemy.draw_cards(5)
            return True
        else:
            self._enemy.draw_cards(4)
            self._hero.draw_cards(5)
            return False

    def full_turn(self, gold):
        # set hero's gold to round number
        self._hero.gold(gold)
        self._endTurn = False
        self._hero.draw_card()
        while not self.end_turn():
            self.turn_choice()

    # Find out want the player wants to do and call correct function based on that choice
    # ********************TO IMPLEMENT*************************ADD H OPTION - HAND INFORMATION***************
    # ********************TO IMPLEMENT*************************ADD B OPTION - BOARD INFORMATION***************
    # ********************TO IMPLEMENT*************************ADD E OPTION - ENEMY INFORMATION***************
    # ********************TO IMPLEMENT*************************ADD H OPTION - HERO INFORMATION***************
    def turn_choice(self):
        print('\nIt\'s ' + self._hero.hero_name() + '\'s turn!\n')
        # While the player makes a doable choice i.e. This will loop uptil the player makes
        #                                              a choice that can actually be done
        self._return = True
        while self._return:
            answers = ('attack', 'play card', 'something else')
            turn_choice = Tools.get_input('|Enter your option|', answers)
            if turn_choice == answers[0]:
                self.choice_attack()
            elif turn_choice == answers[1]:
                self.choice_play_card()
            elif turn_choice == answers[2]:
                self.choice_other()

    # Player wants to Attack with a friendly ally
    def choice_attack(self):
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
    def choice_play_card(self):
        # Does the player have enough Gold to play any of their cards
        if self._hero.any_cards():
            # Does the hero have any cards
            if self._hero.playable_cards():
                
                # Great! Now we can play a card
                # I want to play this card! Retrieve it from you hand
                play_this_card = Tools.get_input('Play which card:', self._hero._hand)
                # Is this chosen card playable?
                if not self._hero.playable_card(play_this_card):
                    print('That card costs too much gold\n')
                    return
                self._hero.play_ally(play_this_card)
                print(play_this_card.name(), 'Get out there!\n')
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

    def choice_other(self):
        while self._return:
            answers = ('end your turn', 'help', 'board info', 'go back')
            turn_choice = Tools.get_input('|Enter your option|', answers)
            if turn_choice == answers[0]:
                self.end_turn(True)
                self._return = False
                return
            elif turn_choice == answers[1]:
                self.get_help()
                return
            elif turn_choice == answers[2]:
                self.print_state()
                return
            elif turn_choice == answers[3]:
                return
            # elif turn_choice == 'a':
            #     self.choiceAttack()
            # elif turn_choice == 'p':
            #     self.choicePlayCard()
            # else:
            #     print('What?\n')
            #     return2

    def end_turn(self, boola=None):
        if boola:
            self._endTurn = boola
        return self._endTurn

    # To be implemented later
    @staticmethod
    def get_help():
        print('Never give up!\n')

    def print_state(self):
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
    turn.full_turn(10)


if __name__ == "__main__":
    main()
