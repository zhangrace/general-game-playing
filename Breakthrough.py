########################################
# CS63: Artificial Intelligence, Lab 4
# Spring 2018, Swarthmore College
########################################
# NOTE: you should not need to modify this file.
########################################

import numpy as np

from BoardGames import _base_game

RED   = u"\033[1;31m"
BLUE  = u"\033[1;34m"
RESET = u"\033[0;0m"
CIRCLE = u"\u25CF"

RED_DISK = RED + CIRCLE + RESET
BLUE_DISK = BLUE + CIRCLE + RESET

class Breakthrough(_base_game):
    """Implements the board game Breakthrough.
    See en.wikipedia.org/wiki/breakthrough_(board_game) for rules.

    There are two ways to construct a Breakthrough instance:
    1. Initialize a new game by passing the board's height and width.
    2. Copy an existing game by specifying the game keyword.

    Attributes:
    board: An array in which +1 represents a blue piece, -1 represents a red
           piece, and 0 represents an empty space.
    turn:  Indicates which player will move next. +1 for the blue (downward-
           moving) player. -1 for the red (upward-moving) player."""
    def __init__(self, height=7, width=5, game=None):
        if game is None: # create new game
            assert width > 1
            self.board = np.zeros([height, width], dtype=int)
            self.board[:2] = 1
            self.board[-2:] = -1
            self.turn = 1
        else: # copy existing game
            self.board = game.board.copy()
            self.turn = game.turn

        self._moves = None
        self._terminal = None
        self._winner = None
        self._repr = None
        self._hash = None

    def makeMove(self, move):
        """Returns a new Breakthrough instance in which move has been played.

        A valid move is a triple (row, col, dir), where row and col indicate
        the position of the piece that is moving, and dir can be -1, 0, or +1,
        indicating which of the (up to) three possible columns the piece moves
        to. For example if it is the +1 player's turn, (2,1,-1) would mean that
        the piece in row 2, column 1 moves to row 3 column 0. On player -1's
        turn, the same move would mean moving to row 1, column 0 (because
        player +1's pieces move down, while player -1's pieces move up)."""
        row, col, delta = move
        new_game = Breakthrough(game=self)
        new_game.board[row, col] = 0
        new_game.board[row + self.turn, col + delta] = self.turn
        new_game.turn *= -1
        return new_game

#The @property decorator makes it so that you can access self.availableMoves
#as a field instead of calling self.availableMoves() as a function.
    @property
    def availableMoves(self):
        """List of legal moves for the current player."""
        if self._moves is None:
            self._moves = []
            for row,col in zip(*np.where(self.board == self.turn)):
                r = row + self.turn
                if (r < 0) or (r >= self.board.shape[0]):
                    continue
                if self.board[r, col] == 0:
                    self._moves.append((row, col, 0))
                for delta in [-1,1]:
                    c = col + delta
                    if (c < 0) or (c >= self.board.shape[1]):
                        continue
                    if self.board[r,c] != self.turn:
                        self._moves.append((row, col, delta))
        return self._moves

    @property
    def isTerminal(self):
        """Boolean indicating whether the game has ended."""
        if self._terminal is None:
            if (1 in self.board[-1]) or (-1 in self.board[0]):
                self._terminal = True
            elif (1 not in self.board) or (-1 not in self.board):
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
        if self._winner is None:
            if -1 in self.board[0]:
                self._winner = -1
            elif 1 in self.board[-1]:
                self._winner = 1
            elif 1 not in self.board:
                self._winner = -1
            elif -1 not in self.board:
                self._winner = 1
        return self._winner
