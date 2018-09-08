########################################
# CS63: Artificial Intelligence, Lab 3
# Spring 2018, Swarthmore College
########################################
# full name(s): Cindy Li and Grace Zhang
# username(s): cli2 and yzhang1
########################################

import numpy as np

def mancalaBasicEval(mancala_game):
    """Difference between the scores for each player.
    Returns +(max possible score) if player +1 has won.
    Returns -(max possible score) if player -1 has won.

    Otherwise returns (player +1's score) - (player -1's score).

    Remember that the number of houses and seeds may vary."""

    if mancala_game.isTerminal:
        totalSum = np.sum(mancala_game.scores) + np.sum(mancala_game.houses)
        if mancala_game.winner == 1:
            return totalSum
        elif mancala_game.winner == -1:
            return -totalSum
        else:
            return 0
    else:
        return mancala_game.scores[0]-mancala_game.scores[1]


def breakthroughBasicEval(breakthrough_game):
    """Measures how far each player's pieces have advanced
    and returns the difference.

    Returns +(max possible advancement) if player +1 has won.
    Returns -(max possible advancement) if player -1 has won.

    Otherwise finds the rank of each piece (number of rows onto the board it
    has advanced), sums these ranks for each player, and
    returns (player +1's sum of ranks) - (player -1's sum of ranks).

    An example on a 5x3 board:
    ------------
    |  0  1  1 |  <-- player +1 has two pieces on rank 1
    |  1 -1  1 |  <-- +1 has two pieces on rank 2; -1 has one piece on rank 4
    |  0  1 -1 |  <-- +1 has (1 piece * rank 3); -1 has (1 piece * rank 3)
    | -1  0  0 |  <-- -1 has (1*2)
    | -1 -1 -1 |  <-- -1 has (3*1)
    ------------
    sum of +1's piece ranks = 1 + 1 + 2 + 2 + 3 = 9
    sum of -1's piece ranks = 1 + 1 + 1 + 2 + 3 + 4 = 12
    state value = 9 - 12 = -3

    Remember that the height and width of the board may vary."""
    height = len(breakthrough_game.board[0])
    width = len(breakthrough_game.board[1])
    if breakthrough_game.isTerminal:
        if breakthrough_game.winner == 1:
            return height*width
        elif breakthrough_game.winner == -1:
            return -height*width
    else:
        p1total = 0
        p2total = 0
        p1rank = 1
        p2rank = height
        for row in breakthrough_game.board:
            for item in row:
                if item == 1:
                    p1total += p1rank
                elif item == -1:
                    p2total += p2rank
            p1rank += 1
            p2rank -= 1
        return p1total-p2total

def mancalaBetterEval(mancala_game):
    """A heuristic that generally wins agains mancalaBasicEval.
    This must be a static evaluation function (no search allowed).

    This heuristic sums the total number of houses with the exact
    numer of seeds to land in that player's goal, ensuring that they
    can make subsequent moves during their turn."""

    if mancala_game.isTerminal:
        totalSum = np.sum(mancala_game.scores) + np.sum(mancala_game.houses)
        if mancala_game.winner == 1:
            return totalSum*20
        elif mancala_game.winner == -1:
            return -totalSum*20
        else:
            return 0
    else:
        house1Dist = 1
        house2Dist = len(mancala_game.houses[0])
        house1Sum = mancala_game.scores[0]
        house2Sum = mancala_game.scores[1]

        if mancala_game.turn == 1:
            for house in mancala_game.houses[0]:
                if house == house1Dist:
                    house1Sum += 1
                house1Dist += 1
        elif mancala_game.turn == -1:
            for house in mancala_game.houses[1]:
                if house == house2Dist:
                    house2Sum +=1
                house2Dist -= 1

        for house in mancala_game.houses[0]:
            if house == 0:
                house1Sum += 1
        for house in mancala_game.houses[1]:
            if house == 0:
                house2Sum +=1

    return house1Sum - house2Sum

def breakthroughBetterEval(breakthrough_game):
    """A heuristic that generally wins agains breakthroughBasicEval.
    This must be a static evaluation function (no searchin allowed).

    The better eval will view with higher priority pieces that are closer to
    the goal side. It will do this by assigning higher values (on a -- scale)
    to boards with more pieces closer to the goal. """
    height = len(breakthrough_game.board[0])
    width = len(breakthrough_game.board[1])
    if breakthrough_game.isTerminal:
        if breakthrough_game.winner == 1:
            return (height*width)**1.1
        elif breakthrough_game.winner == -1:
            return -(height*width)**1.1
    else:
        p1total = 0
        p2total = 0
        p1rank = 1
        p2rank = height + 1
        for row in breakthrough_game.board:
            for item in row:
                if item == 1:
                    p1total += p1rank**3
                elif item == -1:
                    p2total += p2rank**3
            p1rank += 1
            p2rank -= 1
        return p1total-p2total
