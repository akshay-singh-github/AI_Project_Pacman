# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
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

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    import Queue
    startingState = problem.getStartState()
    listExplored = []
    queue_Frontier = Queue.LifoQueue()
    move_sequence  = []
    queue_Frontier.put((startingState,move_sequence))

    while not queue_Frontier.empty():
        state, move_sequence = queue_Frontier.get()
        if not state in listExplored:
            listExplored.append(state)
            if problem.isGoalState(state):
                #move_sequence.reverse()
                return move_sequence
                 
            children = problem.getSuccessors(state)
            for eachchild in children:
                updated_move_sequence = move_sequence+[eachchild[1]]
                queue_Frontier.put((eachchild[0],updated_move_sequence))
    
    #util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    import Queue
    startingState = problem.getStartState()
    listExplored = []
    queue_Frontier = Queue.Queue()
    move_sequence  = []
    queue_Frontier.put((startingState,move_sequence))

    while not queue_Frontier.empty():
        state, move_sequence = queue_Frontier.get()
        if not state in listExplored:
            listExplored.append(state)
            if problem.isGoalState(state):
                #move_sequence.reverse()
                return move_sequence
                 
            children = problem.getSuccessors(state)
            for eachchild in children:
                updated_move_sequence = move_sequence + [eachchild[1]]
                queue_Frontier.put((eachchild[0],updated_move_sequence))
    
    #util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    import util
    startingState = problem.getStartState()
    listExplored = []
    queue_Frontier = util.PriorityQueue()
    h = {}  #heuristic
    g = {}  #node cost
    f = {}  # total cost
    
    g[startingState] = 0
    move_sequence  = []
    queue_Frontier.push((startingState,move_sequence),g[startingState])

    while not queue_Frontier.isEmpty():
        state, move_sequence = queue_Frontier.pop()
        if not state in listExplored:
            listExplored.append(state)
            if problem.isGoalState(state):
                #move_sequence.reverse()
                return move_sequence
            children = problem.getSuccessors(state)
            for eachchild in children:
                childstate, childmove, cost = eachchild
                updated_moves = move_sequence + [eachchild[1]]
                g[childstate] = problem.getCostOfActions(updated_moves)
                queue_Frontier.push((childstate,updated_moves),g[childstate])

    
    #util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    import util
    startingState = problem.getStartState()
    listExplored = []
    queue_Frontier = util.PriorityQueue()
    g = 0
    h = heuristic(startingState,problem)
    f = g+h  #here is the total cost
    move_sequence  = []
    queue_Frontier.push((startingState,move_sequence),f)

    while not queue_Frontier.isEmpty():
        state, move_sequence = queue_Frontier.pop()
        if not state in listExplored:
            listExplored.append(state)
            if problem.isGoalState(state):
                #move_sequence.reverse()
                return move_sequence
            children = problem.getSuccessors(state)
            for eachchild in children:
                childstate, childmove, cost = eachchild
                updated_moves = move_sequence + [eachchild[1]]
                g_new = problem.getCostOfActions(updated_moves)
                h_new = heuristic(childstate,problem)
                f_new = g_new + h_new
                queue_Frontier.push((childstate,updated_moves),f_new)

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
