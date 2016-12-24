# mira.py
# -------
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


# Mira implementation
import util
PRINT = True

class MiraClassifier:
    """
    Mira classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    """
    def __init__( self, legalLabels, max_iterations):
        self.legalLabels = legalLabels
        self.type = "mira"
        self.automaticTuning = False
        self.C = 0.001
        self.legalLabels = legalLabels
        self.max_iterations = max_iterations
        self.initializeWeightsToZero()

    def initializeWeightsToZero(self):
        "Resets the weights of each label to zero vectors"
        self.weights = {}
        for label in self.legalLabels:
            self.weights[label] = util.Counter() # this is the data-structure you should use

    def train(self, trainingData, trainingLabels, validationData, validationLabels):
        "Outside shell to call your method. Do not modify this method."

        self.features = trainingData[0].keys() # this could be useful for your code later...

        if (self.automaticTuning):
            Cgrid = [0.002, 0.004, 0.008]
        else:
            Cgrid = [self.C]

        return self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, Cgrid)


    def multiplyTwoVectors(self,a,b):
        s=0
        if (len(a) > len(b)):
            a,b = b,a
        for k in a:
            if k not in b:
                continue
            s = s + (a[k]*b[k])
        return s

    def subtractTwoVectors(self, a, b):
        tracker = util.Counter()
        for k in a:
            if k in b:
                tracker[k] = a[k] - b[k]
            else:
                tracker[k] = a[k]

        for k in b:
            if k in a:
                continue
            tracker[k] = -1 * b[k]
        return tracker

    def addTwoVectors(self, a, b):
        for k ,v in b.items():
            a[k] = a[k] + v

    def calculateTau(self , weightVectorMistake , weightVectorTarget, featureVector ,C):
        part1 =   self.multiplyTwoVectors((self.subtractTwoVectors(weightVectorMistake, weightVectorTarget)),featureVector)
        part2 = 2*self.multiplyTwoVectors(featureVector , featureVector)
        value = (part1 + 1.0)/part2

        return min(C,value)

    def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, Cgrid):
        """
        This method sets self.weights using MIRA.  Train the classifier for each value of C in Cgrid,
        then store the weights that give the best accuracy on the validationData.

        Use the provided self.weights[label] data structure so that
        the classify method works correctly. Also, recall that a
        datum is a counter from features to values for those features
        representing a vector of values.
        """
        "*** YOUR CODE HERE ***"
        size_training_data=0.0
        size_validation_data=0.0
        UpdatedweightsforCurrentC = util.Counter()
        LabelweightVectors = util.Counter()
        validationLableweightVector = util.Counter()
        counter = 0
        countTracker = util.Counter()
        for C in Cgrid:
            for iteration in range(self.max_iterations):
                size_training_data = len(trainingData)
                for td in range(size_training_data):
                    allowed_labels = self.legalLabels
                    for al in allowed_labels:
                        LabelweightVectors[al] = self.multiplyTwoVectors(self.weights[al],trainingData[td])
                    outputLabel = LabelweightVectors.argMax()
                    if outputLabel != trainingLabels[td]:
                        tau = self.calculateTau(self.weights[outputLabel],self.weights[trainingLabels[td]],trainingData[td] , C )
                        changetracker = util.Counter()
                        for n in trainingData[td].keys():
                            changetracker[n] = (trainingData[td][n]*tau)
                        self.addTwoVectors(self.weights[trainingLabels[td]],changetracker)
                        self.weights[outputLabel] = self.subtractTwoVectors(self.weights[outputLabel], changetracker)

                  
            size_validation_data = len(validationData)
            validation_guesses = self.classify(validationData)
            UpdatedweightsforCurrentC[C] =  self.weights
            for vd in range(len(validation_guesses)):
                if (validation_guesses[vd] == validationLabels[vd]):
                    counter = counter+1
                     
            countTracker[C] = counter
        self.weights = UpdatedweightsforCurrentC[countTracker.argMax()]

        #util.raiseNotDefined()

    def classify(self, data ):
        """
        Classifies each datum as the label that most closely matches the prototype vector
        for that label.  See the project description for details.

        Recall that a datum is a util.counter...
        """
        guesses = []
        for datum in data:
            vectors = util.Counter()
            for l in self.legalLabels:
                vectors[l] = self.weights[l] * datum
            guesses.append(vectors.argMax())
        return guesses


