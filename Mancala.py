########################################
# CS63: Artificial Intelligence, Lab 4
# Spring 2018, Swarthmore College
########################################
# NOTE: you should not need to modify this file.
########################################

import numpy as np

from BoardGames import _base_game

class Mancala(_base_game):
    """Implements Kalah, a common variant of Mancala.
    See en.wikipedia.org/wiki/Kalah for rules.

    There are two ways to construct a Mancala instance:
    1. Initialize a new game by passing houses_per_player and seeds_per_house.
    2. Copy an existing game by specifying the game keyword.

    Attributes:
    houses: A (2 x houses_per_player) array that tracks the number of seeds in
            each non-scoring space on the board.
    scores: A 2-element array that tracks each player's score (end houses).
    turn:   Indicates which player will move next. +1 for the first (top row)
            player. -1 for the second (bottom row) player."""
    def __init__(self, houses_per_player=6, seeds_per_house=4, game=None):
        if game is None: # create new game
            self.houses = np.empty([2, houses_per_player], dtype=int)
            self.houses.fill(seeds_per_house)
            self.scores = np.zeros(2, dtype=int)
            self.turn = 1
        else: # copy existing game
            self.houses = game.houses.copy()
            self.scores = game.scores.copy()
            self.turn = game.turn
        self._moves = None
        self._terminal = None
        self._repr = None
        self._hash = None

    def _print_char(self, i):
        return i

    def __repr__(self):
        """An ascii representation of the board state."""
        if self._repr is None:
            # Player 0 scoring area
            if self.turn == 1:
                rows = [" --", ">| ", " | ", " | ", " --"]
            else:
                rows = [" --", " | ", " | ", ">| ", " --"]
            rows[2] += str(self.scores[0]) + " |"
            for r in [0,4]:
                rows[r] += "-"*(len(str(self.scores[0])) + 2)
            for r in [1,3]:
                rows[r] += " "*len(str(self.scores[0])) + " |"
            # houses
            for h in range(self.houses.shape[1]):
                width = len(str(self.houses[:,h].max()))
                for r in [1,3]:
                    rows[r] += " " + str(self.houses[r//2,h])
                    rows[r] += " "*(width - len(str(self.houses[r//2,h]))) +" |"
                for r in [0,2,4]:
                    rows[r] += "-"*(width + 3)
            rows[2] = rows[2][:-1] + "|"
            # player 1 scoring area
            rows[2] += " " + str(self.scores[1]) + " |\n"
            for r in [0,4]:
                rows[r] += "-"*(len(str(self.scores[1])) + 2) + "\n"
            for r in [1,3]:
                rows[r] += " "*len(str(self.scores[1])) + "  |"
            if self.turn == 1:
                rows[1] += "<\n"
                rows[3] += "\n"
            else:
                rows[1] += "\n"
                rows[3] += "<\n"
            self._repr = "".join(rows)
        return self._repr

    def makeMove(self, move):
        """Returns a new Mancala instance in which move has been played.

        A valid move is the index (column) of a house in which the current
        player has seeds. Seeds in that house are sown counter-clockwise
        until they run out, at which point a capture may occur."""
        new_game = Mancala(game=self)
        new_game.houses = self.houses.copy()
        side = 0 if self.turn == 1 else 1 # start sowing in row 0 or row 1
        start_side = side
        house = move

        # grab seeds
        seeds = self.houses[side, move]
        size = self.houses.shape[1]
        new_game.houses[side, move] = 0

        while seeds > 0: # sow
            if side == 0:
                house -= 1
            else:
                house += 1
            if (house == -1) or (house == size): # reached end of side
                if side == start_side: # sow in the scoring pile
                    new_game.scores[side] += 1
                    seeds -= 1
                    if seeds == 0:
                        break
                side = (side + 1) % 2
                if side == 1:
                    house += 1
                else:
                    house -= 1
            new_game.houses[(side, house)] += 1
            seeds -= 1

        if (house == -1) or (house == size):
            new_game.turn = self.turn # take another turn
        else:
            new_game.turn = -self.turn
            # check for capture
            if side == start_side and new_game.houses[(side, house)] == 1:
                captured_house = ((side + 1) % 2, house)
                if new_game.houses[captured_house] != 0:
                    new_game.scores[side] += new_game.houses[captured_house] + 1
                    new_game.houses[(side, house)] = 0
                    new_game.houses[captured_house] = 0

        # check for empty sides
        if new_game.houses[0].sum() == 0:
            new_game.scores[1] += new_game.houses[1].sum()
            new_game.houses[1] = 0
            new_game._terminal = True
        elif new_game.houses[1].sum() == 0:
            new_game.scores[0] += new_game.houses[0].sum()
            new_game.houses[0] = 0
            new_game._terminal = True

        return new_game

#The @property decorator makes it so that you can access self.availableMoves
#as a field instead of calling self.availableMoves() as a function.
    @property
    def availableMoves(self):
        """List of legal moves for the current player."""
        if self._moves is None:
            side = 0 if self.turn == 1 else 1
            self._moves = [int(m) for m in np.nonzero(self.houses[side])[0]]
        return self._moves

    @property
    def isTerminal(self):
        """Boolean indicating whether the game has ended."""
        if self._terminal is None:
            if self.scores.max() > (self.houses.sum() + self.scores.sum()) // 2:
                self._terminal = True
            elif self.houses.sum() == 0:
                self._terminal = True
            else:
                self._terminal = False
        return self._terminal

    @property
    def winner(self):
        """+1 if the first player (maximizer) has won. -1 if the second player
        (minimizer) has won. 0 if the game is a draw. Raises an AttributeError
        if accessed on a non-terminal state."""
        if not self.isTerminal:
            raise AttributeError("Non-terminal states have no winner.")
        if self.scores[0] > self.scores[1]:
            return 1
        elif self.scores[1] > self.scores[0]:
            return -1
        return 0
