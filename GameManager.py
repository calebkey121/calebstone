import TurnManager as turn
import Hero as hero
import time

class GameManager:
    def __init__(self, player1, player2):
        self._player1 = player1
        self._player2 = player2
        self._player1goesFirst = False
        self._roundCounter = 0

    def round_counter(self, roundNum=None):
        if roundNum:
            self._roundCounter = roundNum
        return self._roundCounter

    def human_v_human(self):
        print('\nLet the games commence...\n')
        player1Turn = turn.HumanTurnManagaer(self._player1, self._player2)
        player2Turn = turn.HumanTurnManagaer(self._player2, self._player1)
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

    def random_v_random(self, output_file):
        player1Copy = self._player1
        player2Copy = self._player2
        player1Turn = turn.RandomTurnManager(player1Copy, player2Copy, output_file)
        player2Turn = turn.RandomTurnManager(player2Copy, player1Copy, output_file)
        self._player1goesFirst = player1Turn.start_of_game()

        # player1goesFirst = True if player1 wins coin toss
        self.round_counter(1)

        while self.check_for_winner() == False:
            if self._player1goesFirst:
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
        self.output_winner(output_file)

    def human_v_random(self, output_file):
        player1Turn = turn.HumanTurnManagaer(self._player1, self._player2)
        player2Turn = turn.RandomTurnManager(self._player2, self._player1, output_file)
        player1goesFirst = player1Turn.start_of_game()

        # player1goesFirst = True if player1 wins coin toss
        self.round_counter(1)

        while self.check_for_winner() == False:
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
        self.output_winner(output_file)

    def check_for_winner(self):
        if self._player1.health() <= 0 or self._player2.health() <= 0:
            return True
        else:
            return False

    def winner(self):
        if self._player1.health() <= 0 and self._player2.health() <= 0:
            return 3
        elif self._player1.health() <= 0:
            return 1
        elif self._player2.health() <= 0:
            return 2


    def output_winner(self, output_file):
        player1Lose = self._player1.health() <= 0
        player2Lose = self._player2.health() <= 0
        # tie
        if player1Lose and player2Lose:
            output_file.write('You both lose!')
        elif player1Lose:
            output_file.write(f'{self._player1.name()} loses!')
        elif player2Lose:
            output_file.write(f'{self._player2.name()} loses!')

def main():


    numRuns = 1000
    ties, win1, win2 = 0, 0, 0
    p1First, p2First = 0, 0

    for i in range(numRuns):
        caleb = hero.Hero(hero='Caleb', deckList="CalebDeckList")
        dio = hero.Hero(hero='Dio', deckList="DioDeckList")
        game = GameManager(caleb, dio)
        output_file = open("RandomRun/output" + str(i + 1), "w")

        print(f"start {i}")
        start = time.time()
        winner = game.random_v_random(output_file)
        end = time.time()
        print(f"end{i}\nelapsed time: {end - start}")
        
        
        output_file.close()

        winner = game.winner()
        if game._player1goesFirst:
            p1First += 1
        else:
            p2First += 1
        
        if winner == 1:
            win1 += 1
        if winner == 2:
            win2 += 1
        if winner == 3:
            ties += 1
    
    print(f"Win Rate Caleb: {(win1 / numRuns) * 100}%")
    print(f"First Rate Caleb: {(p1First / numRuns) * 100}%")
    print(f"Win Rate Dio: {(win2 / numRuns) * 100}%")
    print(f"First Rate Dio: {(p2First / numRuns) * 100}%")
    print(f"Tie Rate: {(ties / numRuns) * 100}%")

if __name__ == "__main__":
    main()