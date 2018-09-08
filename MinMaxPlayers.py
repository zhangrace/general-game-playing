########################################
# CS63: Artificial Intelligence, Lab 3
# Spring 2018, Swarthmore College
########################################
# full name(s): Cindy Li and Grace Zhang
# username(s): cli2 and yzhang1
########################################

class MinMaxPlayer:
    """Gets moves by depth-limited min-max search."""
    def __init__(self, boardEval, depthBound):
        self.name = "MinMax"
        self.boardEval = boardEval
        self.depthBound = depthBound

    def moveHelper(self, currentDepth, depthBound, game_state):
        if currentDepth == depthBound or game_state.isTerminal:
            return None, self.boardEval(game_state)

        bestAction = None
        # initialize bestValue according to if player is a maximizer or minimizer
        if game_state.turn == 1:
            bestValue = -float('inf')
        if game_state.turn == -1:
            bestValue = float('inf')

        for move in game_state.availableMoves:
            nextState = game_state.makeMove(move)
            # ignore the action that gets returned here -- the actual move we
            # care about is the move given by the for loop
            _, val = self.moveHelper(currentDepth+1, depthBound, nextState)
            if game_state.turn == 1 and val >= bestValue:
                bestAction, bestValue = move, val
            if game_state.turn == -1 and val <= bestValue:
                bestAction, bestValue = move, val
        return bestAction, bestValue

    def getMove(self, game_state):
        return self.moveHelper(0, self.depthBound, game_state)[0]

class PruningPlayer:
    """Gets moves by depth-limited min-max search with alpha-beta pruning."""
    def __init__(self, boardEval, depthBound):
        self.name = "Pruning"
        self.boardEval = boardEval
        self.depthBound = depthBound

    def moveHelper(self, lowerBound, upperBound, currentDepth, depthBound, game_state):
        if currentDepth == depthBound or game_state.isTerminal:
            return None, self.boardEval(game_state)

        bestAction = None
        # initialize bestValue according to if player is a maximizer or minimizer
        if game_state.turn == 1:
            bestValue = -float('inf')
        if game_state.turn == -1:
            bestValue = float('inf')

        for move in game_state.availableMoves:
            nextState = game_state.makeMove(move)
            # ignore the action that gets returned here -- the actual move we
            # care about is the move given by the for loop
            _, val = self.moveHelper(lowerBound, upperBound, currentDepth+1, depthBound, nextState)
            if game_state.turn == 1:
                if val >= upperBound:
                    return move, val
                lowerBound = max(val, lowerBound)
                bestAction = move
                bestValue = max(bestValue, val)
            if game_state.turn == -1 and val < bestValue:
                if val <= lowerBound:
                    return move, val
                upperBound = min(val, upperBound)
                bestAction = move
                bestValue = min(bestValue, val)

        return bestAction, bestValue

    def getMove(self, game_state):
        return self.moveHelper(-float('inf'), float('inf'), 0, self.depthBound, game_state)[0]
