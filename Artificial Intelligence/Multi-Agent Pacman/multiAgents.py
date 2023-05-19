# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        newFoodList = newFood.asList()
        minDistance = 999999999999
        for food in newFoodList:
            distance = util.manhattanDistance(food, newPos)
            minDistance = min(minDistance, distance)
        for ghost in newGhostStates:
            ghostPosition = ghost.getPosition()
            ghostDistance = util.manhattanDistance(ghostPosition, newPos)
            if ghostDistance <= 1:
                return -minDistance

        return successorGameState.getScore() + (1/minDistance)

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        value, move = self.max_value(gameState, 0)
        return move

    def max_value(self, gameState, depth):
        legalActionsList = gameState.getLegalActions(0)
        if len(legalActionsList) == 0 or gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState), None
        v = -99999999999999
        for action in legalActionsList:
            v_two, a_two = self.min_value(gameState.generateSuccessor(0, action), depth, 1)
            if v_two > v:
                v = v_two
                move = action
        return v, move

    def min_value(self, gameState, depth, agentIndex):
        legalActionsList = gameState.getLegalActions(agentIndex)
        if len(legalActionsList) == 0 or gameState.isLose() or gameState.isWin() or depth == self.depth:
            return self.evaluationFunction(gameState), None
        v = 99999999999999
        for action in legalActionsList:
            if agentIndex == gameState.getNumAgents() - 1:
                v_two, a_two = self.max_value(gameState.generateSuccessor(agentIndex, action), depth + 1)
            else:
                v_two, a_two = self.min_value(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1)
            if v_two < v:
                v = v_two
                move = action
        return v, move


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        value, move = self.max_value(gameState, 0, -99999999999999, 99999999999999)
        return move
        #util.raiseNotDefined()

    def max_value(self, gameState, depth, alpha, beta):
        legalActionsList = gameState.getLegalActions(0)
        if len(legalActionsList) == 0 or gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState), None
        v = -99999999999999
        for action in legalActionsList:
            v_two, a_two = self.min_value(gameState.generateSuccessor(0, action), depth, 1, alpha, beta)
            if v_two > v:
                v = v_two
                move = action
                alpha = max(alpha, v)
            if v > beta:
                return v, move
        return v, move

    def min_value(self, gameState, depth, agentIndex, alpha, beta):
        legalActionsList = gameState.getLegalActions(agentIndex)
        if len(legalActionsList) == 0 or gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState), None
        v = 99999999999999
        for action in legalActionsList:
            if agentIndex == gameState.getNumAgents() - 1:
                v_two, a_two = self.max_value(gameState.generateSuccessor(agentIndex, action), depth+1, alpha, beta)
            else:
                v_two, a_two = self.min_value(gameState.generateSuccessor(agentIndex, action), depth, agentIndex+1,
                                              alpha, beta)
            if v_two < v:
                v = v_two
                move = action
                beta = min(beta, v)
            if v < alpha:
                return v, move
        return v, move



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        value, move = self.max_value(gameState, 0)
        return move
        #util.raiseNotDefined()

    def max_value(self, gameState, depth):
        legalActionsList = gameState.getLegalActions(0)
        if len(legalActionsList) == 0 or gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState), None
        v = -99999999999999
        for action in legalActionsList:
            v_two, a_two = self.expected_value(gameState.generateSuccessor(0, action), depth, 1)
            if v_two > v:
                v = v_two
                move = action
        return v, move

    def expected_value(self, gameState, depth, agentIndex):
        legalActionsList = gameState.getLegalActions(agentIndex)
        if len(legalActionsList) == 0 or gameState.isLose() or gameState.isWin() or depth == self.depth:
            return self.evaluationFunction(gameState), None
        v = 0
        count = 0
        for action in legalActionsList:
            if agentIndex == gameState.getNumAgents() - 1:
                v_two, a_two = self.max_value(gameState.generateSuccessor(agentIndex, action), depth+1)
                v += v_two
                count += 1
            else:
                v_two, a_two = self.expected_value(gameState.generateSuccessor(agentIndex, action), depth, agentIndex+1)
                v += v_two
                count += 1
        return float(v) / float(count), None


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <My evaluation function used a linear combination of four features: the pacman's distance to food,
    it's distance to a scared ghost, its distance to an active ghost and the distance towards a capsule. For each of
    the distances, I took the reciprocal. I added 0.0001 to the minDistance in the denominator in case the minDistance
    was 0, I wanted to avoid having a divide-by-zero error. For the distance to food, scared ghost and capsule, I added
    the reciprocal to the score because I wanted it to work in a way such that the lower the minDistance, the more
    points are added to the score, which would motivate the pacman to make it a higher priority to eat those items.
    When there was an active ghost, I subtracted from the score the reciprocal, which meant that the lower the distance
    between the Pacman and the active ghost the more points would be subtracted from the score and thus the Pacman
    should try to move as far as possible from the active ghosts and avoid them.>
    """
    "*** YOUR CODE HERE ***"
    global minDistance
    score = currentGameState.getScore()
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newFoodList = newFood.asList()
    newGhostStates = currentGameState.getGhostStates()
    scaredGhost = []
    activeGhost = []
    capsules = currentGameState.getCapsules()

    min_d = 99999999999
    for food in newFoodList:
        distance = util.manhattanDistance(food, newPos)
        minDistance = min(min_d, distance)
    score += (1/(minDistance+0.0001))

    for ghost in newGhostStates:
        if ghost.scaredTimer != 0:
            scaredGhost.append(ghost.getPosition())
        else:
            activeGhost.append(ghost.getPosition())

    for scGhost in scaredGhost:
        distance = util.manhattanDistance(newPos, scGhost)
        minDistance = min(min_d, distance)
    score += (1/(minDistance+0.0001))

    for acGhost in activeGhost:
        distance = util.manhattanDistance(newPos, acGhost)
        minDistance = min(min_d, distance)
    score -= (1/(minDistance+0.0001))

    for capsule in capsules:
        distance = util.manhattanDistance(capsule, newPos)
        minDistance = min(min_d, distance)
    score += (1/(minDistance+0.0001))

    return score

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
