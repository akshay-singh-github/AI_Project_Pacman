# multiAgents.py
# --------------
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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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
        #print "Sucessor game state is :",successorGameState
        newPos = successorGameState.getPacmanPosition()
        #print "Pacman position after moving (newPos) :",newPos
        newFood = successorGameState.getFood().asList()
        currentFood = currentGameState.getFood().asList()
        #print "remaining food value :",newFood
        newGhostStates = successorGameState.getGhostStates()
        #print "These are the new ghost states :",newGhostStates
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        #print "newScaredTimes holds the number of moves that each ghost will remain scared :",newScaredTimes
        
        "*** YOUR CODE HERE ***"
        
        optimum_heuristic_value=0.0
        for foodItem in currentFood:
            foodDistance=manhattanDistance(foodItem,newPos)
            #print "the food distance is",foodDistance
            if(foodDistance==0):
                optimum_heuristic_value+=400
            else:
                optimum_heuristic_value+=10/(foodDistance*foodDistance)
        for ghostItem in newGhostStates:
            #print "ghost is here",ghost.getPosition()
            ghostDistance=manhattanDistance(ghostItem.getPosition(),newPos)
            print "ghost distance is here",ghostDistance
            if(ghostDistance<=1):
                if(ghostItem.scaredTimer!=0):
                    optimum_heuristic_value+=4000
                else:
                    optimum_heuristic_value-=600
        for capsulePellet in currentGameState.getCapsules():
          capsulePelletDistance=manhattanDistance(capsulePellet,newPos)
          if(capsulePelletDistance==0):
            optimum_heuristic_value+=400
          else:
            optimum_heuristic_value+=50/capsulePelletDistance


        print "optimum_heuristic_value",optimum_heuristic_value       
        return optimum_heuristic_value

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
        """
        "*** YOUR CODE HERE ***"
        return self.maxValueFunction(gameState,self.depth)[1]

    def maxValueFunction(self,gameState,depth):
        if gameState.isLose() or gameState.isWin() or (depth == 0):
            return self.evaluationFunction(gameState)

        value = -(float("inf"))
        allowedActions = gameState.getLegalActions()
        values = []
        
        values = [self.minValueFunction(gameState.generateSuccessor(self.index, each_action),1 ,depth) for each_action in allowedActions]
        value=max(values)
        for position in range(len(values)):
            if(values[position]==value):
                related_number = position
        related_action = allowedActions[related_number]
        return value, related_action



    def minValueFunction(self,gameState,agentIndex,depth):
        if gameState.isLose() or gameState.isWin() or (depth == 0):
            return self.evaluationFunction(gameState)
        
        value = float("inf")
        allowedActions = gameState.getLegalActions(agentIndex)
        values = []
        if (agentIndex != gameState.getNumAgents()-1):
            values = [self.minValueFunction(gameState.generateSuccessor(agentIndex, each_action),agentIndex + 1,depth) for each_action in allowedActions]
        else:
            values = [self.maxValueFunction(gameState.generateSuccessor(agentIndex, each_action),depth - 1) for each_action in allowedActions]
        value = min(values)

        for position in range(len(values)):
            if(values[position]==value):
                related_number = position
                
        related_action = allowedActions[related_number]     
        return value, related_action




class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        final_value_and_action = self.finalCalculatedValue(gameState, 0, -float("inf"), float("inf"))
        return final_value_and_action[1]

    def maxValueFunction(self,gameState,depth,alphaValue,betaValue):
        value=-(float("inf"))
        outputValueandAction=(value,None)
        allowedActions=gameState.getLegalActions()
        if len(allowedActions) == 0:
            return (self.evaluationFunction(gameState),None)

        for each_action in allowedActions:
            successor_after_each_action = gameState.generateSuccessor(0,each_action)
            old_value=value
            value=max(value,self.finalCalculatedValue(successor_after_each_action,depth+1,alphaValue,betaValue)[0])
            if old_value!=value:
                outputValueandAction=(value,each_action)
            if value>betaValue:
                return outputValueandAction
            alphaValue = max(alphaValue,value)
        return outputValueandAction
    
    def minValueFunction(self,gameState,depth,alphaValue,betaValue):
        value=float("inf")
        outputValueandAction=(value,None)
        allowedActions=gameState.getLegalActions(depth % gameState.getNumAgents())
        
        if len(allowedActions) == 0:
            return (self.evaluationFunction(gameState),None)
        
        for each_action in allowedActions:
            successor_after_each_action = gameState.generateSuccessor(depth % gameState.getNumAgents(),each_action)
            old_value=value
            value=min(value,self.finalCalculatedValue(successor_after_each_action,depth+1,alphaValue,betaValue)[0])
            if old_value!=value:
                outputValueandAction=(value,each_action)
            if value<alphaValue:
                return outputValueandAction
            betaValue = min(betaValue,value)
        return outputValueandAction
        
            
    def finalCalculatedValue(self,gameState,depth,alphaValue,betaValue):
        if depth == self.depth*gameState.getNumAgents() or gameState.isLose() or gameState.isWin():
            return (self.evaluationFunction(gameState),None)
        if depth % gameState.getNumAgents() != 0:
            return self.minValueFunction(gameState,depth,alphaValue,betaValue)
        else:
            return self.maxValueFunction(gameState,depth,alphaValue,betaValue)



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
        final_value_and_action = self.finalCalculatedValue(gameState, 0)
        return final_value_and_action[1]


        
    def finalCalculatedValue(self,gameState,depth):
        if depth == self.depth*gameState.getNumAgents() or gameState.isLose() or gameState.isWin():
            return (self.evaluationFunction(gameState),None)
        if depth % gameState.getNumAgents() != 0:
            return self.expValueFunction(gameState,depth)
        else:
            return self.maxValueFunction(gameState,depth)
        
    
    def expValueFunction(self, gameState, depth):
        value=0
        outputValueandAction=(value,None)
        allowedActions=gameState.getLegalActions(depth % gameState.getNumAgents())
        if len(allowedActions) == 0:
            return (self.evaluationFunction(gameState),None)
        prob = float(1./len(allowedActions))
        optimumValue=0
        for each_action in allowedActions:
            successor_after_each_action = gameState.generateSuccessor(depth % gameState.getNumAgents(),each_action)
    
            value=self.finalCalculatedValue(successor_after_each_action,depth+1)[0]
            optimumValue=optimumValue+(value*prob)
            outputValueandAction=(optimumValue,None)
        return outputValueandAction
           
    def maxValueFunction(self,gameState,depth):
        value=-(float("inf"))
        outputValueandAction=(value,None)
        allowedActions=gameState.getLegalActions()
        if len(allowedActions) == 0:
            return (self.evaluationFunction(gameState),None)
        for each_action in allowedActions:
            successor_after_each_action = gameState.generateSuccessor(0,each_action)
            old_value=value
            value=max(value,self.finalCalculatedValue(successor_after_each_action,depth+1)[0])
            if old_value!=value:
                outputValueandAction=(value,each_action)
        return outputValueandAction


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    value = 0
    currentPosition = currentGameState.getPacmanPosition()
    posFood = currentGameState.getFood().asList()
    initialDistanceValue = 1000000
    changeinitialDistanceValue = False
    for pof in posFood:
        distFood = util.manhattanDistance(currentPosition, pof)
        oldinitialDistanceValue = initialDistanceValue
        initialDistanceValue = min(initialDistanceValue,distFood)
        if oldinitialDistanceValue!=initialDistanceValue:
            changeinitialDistanceValue = True
    if changeinitialDistanceValue:
        value += initialDistanceValue
    value += 1000*currentGameState.getNumFood()
    value += 10*len(currentGameState.getCapsules())
    posGhost = currentGameState.getGhostPositions()
    for pog in posGhost:
        distGhost = util.manhattanDistance(currentPosition, pog)
        if distGhost < 2:
            value = 999999
    value -= 10*currentGameState.getScore()
    return value*(-1)

# Abbreviation
better = betterEvaluationFunction

