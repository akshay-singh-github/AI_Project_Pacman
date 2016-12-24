# perceptron.py
# -------------
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


# Perceptron implementation
import util
PRINT = True

class PerceptronClassifier:
    """
    Perceptron classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    """
    def __init__( self, legalLabels, max_iterations):
        self.legalLabels = legalLabels
        self.type = "perceptron"
        self.max_iterations = max_iterations
        self.weights = {}
        for label in legalLabels:
            self.weights[label] = util.Counter() # this is the data-structure you should use

    def setWeights(self, weights):
        assert len(weights) == len(self.legalLabels);
        self.weights = weights;

    def return_vector_score(self,train_data,weights):
        totalvalue = 0
        if len(train_data) > len(weights):
            temp = train_data
            train_data = weights
            weights = temp
        for td in train_data:
            if td not in weights:
                continue
            totalvalue = totalvalue + (train_data[td] * weights[td])
        return totalvalue

    def return_new_sub_weights(self,weight_vector,training_data):
        subvector = util.Counter()
        for wv in weight_vector:
            if wv in training_data:
                subvector[wv] = weight_vector[wv] - training_data[wv]
            else:
                subvector[wv] = weight_vector[wv]

        for td in training_data:
            if td in weight_vector:
                continue
            subvector[td] = -1 * training_data[td]

        return subvector


    def train( self, trainingData, trainingLabels, validationData, validationLabels ):
        """
        The training loop for the perceptron passes through the training data several
        times and updates the weight vector for each label based on classification errors.
        See the project description for details.

        Use the provided self.weights[label] data structure so that
        the classify method works correctly. Also, recall that a
        datum is a counter from features to values for those features
        (and thus represents a vector a values).
        """

        self.features = trainingData[0].keys() # could be useful later
        # DO NOT ZERO OUT YOUR WEIGHTS BEFORE STARTING TRAINING, OR
        # THE AUTOGRADER WILL LIKELY DEDUCT POINTS.

        for iteration in range(self.max_iterations):
            print "Starting iteration ", iteration, "..."
            for i in range(len(trainingData)):
                "*** YOUR CODE HERE ***"
                allowed_labels = self.legalLabels
                current_training_label = trainingLabels[i]
                vec = util.Counter()
                for al in allowed_labels:
                    vec[al] = self.return_vector_score(trainingData[i],self.weights[al])
                if current_training_label != vec.argMax():
                    for kv in trainingData[i].items():
                        self.weights[current_training_label][kv[0]] = self.weights[current_training_label][kv[0]] + kv[1]
                    self.return_new_sub_weights(self.weights[vec.argMax()] , trainingData[i])

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


    def findHighWeightFeatures(self, label):
        """
        Returns a list of the 100 features with the greatest weight for some label
        """
        featuresWeights = []

        "*** YOUR CODE HERE ***"
        counter = 100
        #print "self.weights[label]" , self.weights[label]
        initialfeaturesandWeights = self.weights[label]
        sorted_features_and_weights = initialfeaturesandWeights.sortedKeys()
        #print "sorted_features_and_weights" , sorted_features_and_weights
        while counter>0:
            featuresWeights.append(initialfeaturesandWeights.argMax())
            del initialfeaturesandWeights[initialfeaturesandWeights.argMax()]
            counter = counter - 1
        
        #util.raiseNotDefined()

        return featuresWeights
