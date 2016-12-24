# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        for each_iteration in range(self.iterations):
            values_for_current_iteration = self.values.copy()  
            for each_state in self.mdp.getStates():  
                if self.mdp.isTerminal(each_state):
                    continue
                allowed_actions = self.mdp.getPossibleActions(each_state)
                bestQvalue = None
                for each_action in allowed_actions:
                    Qvalue_for_this_action = self.getQValue(each_state, each_action)
                    trackbestvalue = bestQvalue
                    bestQvalue = max(Qvalue_for_this_action,bestQvalue)  
                values_for_current_iteration[each_state] = bestQvalue
            self.values = values_for_current_iteration


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        # A variable V is defined to store the value of each successive q state additively.
        # the initial value of this variable is kept 0.
        V=0
        #Let TransVariable be the variable that stores the values for nextstate and probability
        #Therefore

        for TransVariable in self.mdp.getTransitionStatesAndProbs(state, action):
            V+= TransVariable[1]*(self.mdp.getReward(state, action, TransVariable[0]) +(self.discount * self.values[TransVariable[0]])) 
        return V


    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        actions = self.mdp.getPossibleActions(state)
        bestQvalue = None
        bestAction = None
        for each_action in actions:
            currentQvalue = self.getQValue(state,each_action)
            trackbestQvalue = bestQvalue
            bestQvalue = max(bestQvalue,currentQvalue)
            if bestQvalue != trackbestQvalue:
                bestAction = each_action
        return bestAction

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
