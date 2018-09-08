########################################
# CS63: Artificial Intelligence, Lab 4
# Spring 2018, Swarthmore College
########################################
# full name(s): Cindy Li, Grace Zhang
# username(s): cli2, yzhang1
########################################

#NOTE: You will probably want to make use of these imports.
#      Feel free to add more.
from math import log, sqrt
from numpy.random import choice

class Node(object):
    """Node used in MCTS"""
    def __init__(self, state):
        self.state = state
        self.children = {} # maps moves to Nodes
        self.visits = 0
        self.value = 0
        #NOTE: you may add additional fields if needed

    def updateValue(self, outcome):
        """Updates the value estimate for the node's state.
        outcome: a game object, where the winner field will store +1 for a
                1st player win, -1 for a 2nd player win, or 0 for a draw."""
        self.value *= self.visits
        self.value += outcome.winner
        self.visits += 1
        self.value /= self.visits

    def UCBWeight(self, UCB_const, parent_visits, player):
        """Weight from the UCB formula used by parent to select a child.
        This node will be selected by the parent with probability
        proportional to its weight."""
        if player == 1:
            value = self.value
        else:
            value = -self.value

        weight = value + (UCB_const * sqrt(log(parent_visits/self.visits)))
        # add 1 to weight to shift distribution from [-1.1] to [0,2], keeping
        # all values positive
        return weight + 1

    def UCBSample(self, UCB_const):
        weights = []
        for child in self.children.values():
            weights.append(child.UCBWeight(UCB_const, self.visits, self.state.turn))
        weightSum = 0
        for i in weights:
            weightSum += i
        distribution = [weight/weightSum for weight in weights]
        moveIndex = choice(len(self.state.availableMoves), p=distribution )
        move = self.state.availableMoves[moveIndex]
        return self.children[move]

class MCTSPlayer(object):
    """Selects moves using Monte Carlo tree search."""
    def __init__(self, rollouts=1000, UCB_const=1.0):
        self.name = "MCTS"
        self.rollouts = rollouts
        self.UCB_const = UCB_const
        self.nodes = {} #maps states to their nodes
        self.path = []

    def getMove(self, game):
        # find node for game if it exists, otherwise create one
        if game not in self.nodes.keys():
            # (state, Node)
            node = Node(game)
        else:
            node = self.nodes[game]

        # call MCTS to perform rollouts
        self.MCTS(node)

        # return the best move
        allChildren = node.children
        bestChild = None
        bestMove = None

        if game.turn == 1:
            maxVal = -float('inf')
            for move, child in allChildren.items():
                if child.value > maxVal:
                    maxVal = child.value
                    bestChild = child
                    bestMove = move
        elif game.turn == -1:
            minVal = float('inf')
            for move, child in allChildren.items():
                if child.value < minVal:
                    minVal = child.value
                    bestChild = child
                    bestMove = move
        return bestMove

    def randomPlayout(self, state):
        while not state.isTerminal:
            nextMoveIndex = choice(len(state.availableMoves))
            nextMove = state.availableMoves[nextMoveIndex]

            # nextMove = state.availableMoves[0]
            state = state.makeMove(nextMove)
        return state

    def MCTS(self, root_node):
        """Plays random games from the root node to a terminal state.
        Each rollout consists of four phases:
            Selection: nodes are selected according to UCB as long as all
                    children have been expanded.
            Expansion: a new node is created for a random unexpanded child.
            Simulation: uniform random moves are played until the end of
                    the game.
            Backpropagation: values and visits are updated for each node
                    visited during selection and expansion."""

        for i in range(0, self.rollouts):
            node = root_node
            self.path = []
            self.path.append(root_node)

            # selection
            while len(node.children) == len(node.state.availableMoves) and not node.state.isTerminal:
                if len(node.children) == 1:
                    node = node.children[node.state.availableMoves[0]]
                    self.path.append(node)
                else:
                    node = node.UCBSample(self.UCB_const)
                    self.path.append(node)

            # expansion
            if not node.state.isTerminal:
                unexpandedNodes = set(node.state.availableMoves).difference(node.children.keys())
                nodesList = list(unexpandedNodes)
                nextMoveIndex = choice(len(nodesList))
                nextMove = nodesList[nextMoveIndex]

                # create new node from resulting state after move has been made
                moveState = node.state.makeMove(nextMove)
                nextNode = Node(moveState)

                # append new node to node's children and path
                node.children[nextMove] = nextNode
                self.path.append(nextNode)

                # simulation
                outcome = self.randomPlayout(moveState)

            else:
                outcome = node.state
            # backpropagation
            for node in self.path:
                node.updateValue(outcome)
