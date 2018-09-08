########################################
# CS63: Artificial Intelligence, Lab 4
# Spring 2018, Swarthmore College
########################################
# NOTE: you should not need to modify this file.
########################################

from random import choice
from sys import stdin


class HumanPlayer:
    """Player that gets moves from command line input."""
    def __init__(self, *args):
        self.name = "Human"

    def getMove(self, game):
        move = None
        while move not in game.availableMoves:
            if all(isinstance(move, int) for move in game.availableMoves):
                print("select a move from", game.availableMoves)
                try:
                    move = int(stdin.readline())
                except ValueError:
                    print("invalid move")
                if move not in game.availableMoves:
                    print("invalid move")
            else:
                print("select a move from:")
                for i,move in enumerate(game.availableMoves):
                    print(i, ":", move)
                try:
                    move = game.availableMoves[int(stdin.readline())]
                except (ValueError, IndexError):
                    print("invalid move")
        return move


class RandomPlayer:
    """Player that selects a random legal move."""
    def __init__(self, *args):
        self.name = "Random"

    def getMove(self, game):
        return choice(game.availableMoves)
