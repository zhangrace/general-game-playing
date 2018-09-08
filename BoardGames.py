########################################
# CS63: Artificial Intelligence, Lab 4
# Spring 2018, Swarthmore College
########################################
# NOTE: you should not need to modify this file.
########################################

RED   = u"\033[1;31m"
BLUE  = u"\033[1;34m"
RESET = u"\033[0;0m"
CIRCLE = u"\u25CF"

RED_DISK = RED + CIRCLE + RESET
BLUE_DISK = BLUE + CIRCLE + RESET

class _base_game:

    def __repr__(self):
        if self._repr is None:
            self._repr = "\n".join(" ".join(map(self._print_char, row)) for row in self.board)
            self._repr += "   " + self._print_char(self.turn) + " to move\n"
        return self._repr

    def __hash__(self):
        if self._hash is None:
            self._hash = hash(repr(self))
        return self._hash

    def __eq__(self, other):
        return repr(self) == repr(other)

    def _print_char(self, i):
        if i > 0:
            return BLUE_DISK
        if i < 0:
            return RED_DISK
        return u'\u00B7' # empty cell
