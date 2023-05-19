# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print ("Start:", problem.getStartState())
    print ("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print ("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    frontier = util.Stack()
    explored = set()
    frontier.push((start, []))
    while not frontier.isEmpty():
        curr_cell = frontier.pop()
        coordinates = curr_cell[0]
        actions = curr_cell[1]
        if problem.isGoalState(coordinates):
            return actions
        if coordinates not in explored:
            explored.add(coordinates)
            for successor in problem.getSuccessors(coordinates):
                if successor[0] not in explored:
                    new_node = successor[0]
                    new_action = actions + [successor[1]]
                    frontier.push((new_node, new_action))

    util.raiseNotDefined()
    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    frontier = util.Queue()
    explored = set()
    frontier.push((start, []))
    while not frontier.isEmpty():
        node = frontier.pop()
        coordinates = node[0]
        actions = node[1]
        if problem.isGoalState(coordinates):
            return actions
        if coordinates not in explored:
            explored.add(coordinates)
            for successor in problem.getSuccessors(coordinates):
                if successor[0] not in explored:
                    new_node = successor[0]
                    new_action = actions + [successor[1]]
                    frontier.push((new_node, new_action))

    util.raiseNotDefined()
    return []


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    frontier = util.PriorityQueue()
    explored = set()
    frontier.push((start, []), 0)
    while not frontier.isEmpty():
        node = frontier.pop()
        coordinates = node[0]
        actions = node[1]
        if problem.isGoalState(coordinates):
            return actions
        if coordinates not in explored:
            explored.add(coordinates)
            for successor in problem.getSuccessors(coordinates):
                if successor[0] not in explored:
                    new_node = successor[0]
                    new_action = actions + [successor[1]]
                    new_cost = problem.getCostOfActions(new_action)
                    frontier.push((new_node, new_action), new_cost)

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    frontier = util.PriorityQueue()
    explored = set()
    frontier.push((start, []), 0)
    while not frontier.isEmpty():
        node = frontier.pop()
        coordinates = node[0]
        actions = node[1]
        if problem.isGoalState(coordinates):
            return actions
        if coordinates not in explored:
            explored.add(coordinates)
            for successor in problem.getSuccessors(coordinates):
                if successor[0] not in explored:
                    new_node = successor[0]
                    new_action = actions + [successor[1]]
                    new_cost = problem.getCostOfActions(new_action)
                    new_heuristic = heuristic(new_node, problem)
                    total_cost = new_cost + new_heuristic
                    frontier.push((new_node, new_action), total_cost)

    util.raiseNotDefined()

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
