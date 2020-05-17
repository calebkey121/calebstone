import TurnManager as Turn
import Hero as Hero


class GameManager:
    def __init__(self, player1, player2):
        self._player1 = player1
        self._player2 = player2
        self._roundCounter = 0

    def round_counter(self, round_num=None):
        if round_num:
            self._roundCounter = round_num
        return self._roundCounter

    def game(self):
        player_1_turn = Turn.TurnManager(self._player1, self._player2)
        player_2_turn = Turn.TurnManager(self._player2, self._player1)

        # player_1_goes_first = True if player1 wins coin toss
        player_1_goes_first = player_1_turn.startOfGame()
        self.round_counter(1)

        while self._player1.heroHealth() > 0 and self._player2.heroHealth() > 0:
            if player_1_goes_first:
                # Take your turns - player 1 then player 2
                # pass in round number to set gold for that turn
                player_1_turn.fullTurn(self.round_counter())
                player_2_turn.fullTurn(self.round_counter())
            else:
                # Take your turns - player 2 then player 1
                player_2_turn.fullTurn(self.round_counter())
                player_1_turn.fullTurn(self.round_counter())
            self._roundCounter += 1


def main():
    caleb = Hero.Hero(hero='caleb')
    caleb.deckList('DeckLists/CalebDeckList.txt')
    dio = Hero.Hero(hero='dio')
    dio.deckList('DeckLists/DioDeckList.txt')
    
    game = GameManager(caleb, dio)
    game.game()


if __name__ == "__main__":
    main()
