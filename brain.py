from keras.models import Sequential
from keras.layers import Dense, Activation
import numpy as np
from random import randrange
import pygame

from neuralnetwork import NeuralNetwork
from formulae import calculate_average_error, seed_random_number_generator
import parameters

class TrainingExample():
    def __init__(self, inputs, output):
        self.inputs = inputs
        self.output = output

class Brain:

    def __init__(self):
        self.mapShots = {}
        self.mapHits  = {}
        self.trained = False

        self.id = randrange(0,100)
        # create model
        self.model = NeuralNetwork([4, 6, 4, 4, 1])

        # create model
        self.keras = Sequential()

        # From what I could gather from the docs, columns came first in the input shape
        self.keras.add(Dense(4, input_shape=(4,), activation='relu'))
        self.keras.add(Dense(6, activation='relu'))
        self.keras.add(Dense(4, activation='relu'))
        self.keras.add(Dense(4, activation='relu'))
        self.keras.add(Dense(1, activation='sigmoid'))
        self.keras.compile(loss='mean_squared_error', optimizer='sgd', metrics=['accuracy'])        
        
 
    def train(self):
        # Builds the model based on the dataset to this point
        # Create a n * 4 matrix for the input data
        #[list(item) for item in self.mapShots.it]
        x = []
        #y = np.empty((0))
        y = []
        #Step 1, build Numpy Arrays for complete data points
        for k,v in self.mapShots.items():
            # Convert our tuple to a numpy array
            if k in self.mapHits:
                a = list(v)
                x.append(a)
                #y = np.append(y,self.mapHits[k])
                y.append(self.mapHits[k])
        
        #print x
        #print y
        # Fit the data to the model        
        self.keras.fit(x,y,nb_epoch=150,batch_size=10)
        scores = self.keras.evaluate(x, y)
        print("\n%s: %.2f%%" % (self.keras.metrics_names[1], scores[1]*100))


    def learn(self):
        # Builds the model based on the dataset to this point
        # Create a n * 4 matrix for the input data
        #[list(item) for item in self.mapShots.it]
        x = []
        #y = np.empty((0))
        y = []
        #Step 1, build Numpy Arrays for complete data points
        cumulative_error = 0
        for k,v in self.mapShots.items():
            # Convert our tuple to a numpy array
            if k in self.mapHits:
                a = list(v)
                cumulative_error += self.model.train(TrainingExample(a,self.mapHits[k]))
        
        #print x
        #print y
        #print "Finished training, cumulative error was "+str(cumulative_error)
        # Fit the data to the model        
        self.trained = True
        

    def add_shot(self, bullet, dx, dy, du, dv):
        self.mapShots[bullet] = (dx, dy, du, dv)

    def record_hit(self, bullet):
        self.mapHits[bullet] = 1
        #self.learn()

    def record_miss(self, bullet):
        self.mapHits[bullet] = 0
        #self.learn()

    def draw(self,screen):
        #from keras.utils.layer_utils import print_summary
        #print_summary(self.model)
        self.model.draw(screen)