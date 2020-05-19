import TurnManager as turn
import Hero as hero

class GameManager:
    def __init__(self, player1, player2):
        self._player1 = player1
        self._player2 = player2
        self._roundCounter = 0

    def round_counter(self, roundNum=None):
        if roundNum:
            self._roundCounter = roundNum
        return self._roundCounter

    def game(self):
        print('\nLet the games commence...\n')
        player1Turn = turn.TurnManager(self._player1, self._player2)
        player2Turn = turn.TurnManager(self._player2, self._player1)
        player1goesFirst = player1Turn.start_of_game()

        # player1goesFirst = True if player1 wins coin toss
        self.round_counter(1)

        while self.check_for_winner() == False:
            print(f'Round {self.round_counter()}:')
            if player1goesFirst:
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

    def check_for_winner(self):
        if self._player1.health() <= 0 or self._player2.health() <= 0:
            return True
        else:
            return False

    def print_winner(self):
        player1Lose = self._player1.health() <= 0
        player2Lose = self._player2.health() <= 0
        # tie
        if player1Lose and player2Lose:
            print('You both lose!')
        elif player1Lose:
            print(f'{self._player1.name()} loses!')
        elif player2Lose:
            print(f'{self._player2.name()} loses!')

def main():
    caleb = hero.Hero(hero='caleb')
    caleb.deck_list('CalebDeckList.txt')
    dio = hero.Hero(hero='dio')
    dio.deck_list('DioDeckList.txt')
    
    game = GameManager(caleb, dio)
    game.game()

if __name__ == "__main__":
    main()