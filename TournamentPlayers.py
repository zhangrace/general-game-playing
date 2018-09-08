########################################
# CS63: Artificial Intelligence, Lab 4
# Spring 2018, Swarthmore College
########################################
# NOTE: You should replace this with your TournamentPlayers.py
########################################

from Heuristics import breakthroughBetterEval, mancalaBetterEval, breakthroughBasicEval, mancalaBasicEval
from MinMaxPlayers import PruningPlayer

class BreakthroughTournamentPlayer:
    """Default implementation for the Breakthrough tournament."""

    def __init__(self):
        self.name = "cli2-yzhang1"
        self.player = PruningPlayer(breakthroughBasicEval, 1)

    def getMove(self, game):
        return self.player.getMove(game)


class MancalaTournamentPlayer:
    """Default implementation for the Mancala tournament."""
    def __init__(self):
        self.name = "cli2-yzhang1"
        self.player = PruningPlayer(mancalaBasicEval, 1)

    def getMove(self, game):
        return self.player.getMove(game)
