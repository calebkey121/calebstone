import GameManager
import Hero as hero

class simulator:
    def __init__(self, player1Name, player1Deck, player2Name, player2Deck, numRuns, typeRuns):
        self._player1Name = player1Name
        self._player1Deck = player1Deck
        self._player2Name = player2Name
        self._player2Deck = player2Deck
        self._numRuns = numRuns
        self._typeRuns = typeRuns

        self._player1 = hero.Hero(hero=player1Name, deckList=player2Name)
        self._player2 = hero.Hero(hero=player1Name, deckList=player2Name)

        if self._typeRuns == "Random":




