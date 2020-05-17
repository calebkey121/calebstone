import TurnManager as Turn
import Hero as Hero


class GameManager:
    def __init__(self, player1, player2):
        self._player1 = player1
        self._player2 = player2
        self._roundCounter = 0

    def roundCounter(self, roundNum=None):
        if roundNum:
            self._roundCounter = roundNum
        return self._roundCounter

    def game(self):
        player1Turn = Turn.TurnManager(self._player1, self._player2)
        player2Turn = Turn.TurnManager(self._player2, self._player1)

        # player1goesFirst = True if player1 wins coin toss
        player1goesFirst = player1Turn.startOfGame()
        self.roundCounter(1)

        while self._player1.heroHealth() > 0 and self._player2.heroHealth() > 0:
            if player1goesFirst:
                # Take your turns - player 1 then player 2
                # pass in round number to set gold for that turn
                player1Turn.fullTurn(self.roundCounter())
                player2Turn.fullTurn(self.roundCounter())
            else:
                # Take your turns - player 2 then player 1
                player2Turn.fullTurn(self.roundCounter())
                player1Turn.fullTurn(self.roundCounter())
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
