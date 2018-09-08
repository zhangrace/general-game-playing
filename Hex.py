########################################
# CS63: Artificial Intelligence, Lab 4
# Spring 2018, Swarthmore College
########################################
# NOTE: you should not need to modify this file.
########################################

import numpy as np
from scipy.ndimage import label

from BoardGames import _base_game

_adj = np.ones([3,3], int)
_adj[0,0] = 0
_adj[2,2] = 0

RED   = u"\033[1;31m"
BLUE  = u"\033[1;34m"
RESET = u"\033[0;0m"
SQUARE = u"\u2588"

RED_BORDER = RED + "-" + RESET
BLUE_BORDER = BLUE + "\\" + RESET



class HexGame(_base_game):
    def __init__(self, size=8):
        self.size = size
        self.turn = 1
        self.board = np.zeros([size, size], int)

        self._moves = None
        self._terminal = None
        self._winner = None
        self._repr = None
        self._hash = None

    def __repr__(self):
        if self._repr is None:
            self._repr = u"\n" + (" " + RED_BORDER)*self.size +"\n"
            for i in range(self.size):
                self._repr += " " * i + BLUE_BORDER + " "
                for j in range(self.size):
                    self._repr += self._print_char(self.board[i,j]) + " "
                self._repr += BLUE_BORDER + "\n"
            self._repr += " "*(self.size) + " " + (" " + RED_BORDER) * self.size
        return self._repr

    def makeMove(self, move):
        """Returns a new ConnectionGame in which move has been played.
        A move is a column into which a piece is dropped."""
        hg = HexGame(self.size)
        hg.board = np.array(self.board)
        hg.board[move[0], move[1]] = self.turn
        hg.turn = -self.turn
        return hg

    @property
    def availableMoves(self):
        if self._moves is None:
            self._moves = list(zip(*np.nonzero(np.logical_not(self.board))))
        return self._moves

    @property
    def isTerminal(self):
        if self._terminal is not None:
            return self._terminal
        if self.turn == 1:
            clumps = label(self.board < 0, _adj)[0]
        else:
            clumps = label(self.board.T > 0, _adj)[0]
        spanning_clumps = np.intersect1d(clumps[0], clumps[-1])
        self._terminal = np.count_nonzero(spanning_clumps)
        return self._terminal

    @property
    def winner(self):
        if self.isTerminal:
            return -self.turn
        return 0
