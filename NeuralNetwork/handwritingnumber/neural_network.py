import numpy as np
import os

BASE_DIR = os.path.dirname(__file__)

def sigmoid(X):
    return 1./(1. + np.exp(-X))

def transfer(weight, input, threshold_method = sigmoid):
    X = np.dot(weight, input)
    output = threshold_method(X)
    return output

class NeuralNetwork(object):

    def __init__(self, learning_rate = 0.5, input_size = 1, hidden_size = 3, output_size = 1):
        self.alpha = learning_rate
        self.size = (input_size, hidden_size, output_size)
        self.weight_ih = np.random.rand(hidden_size, input_size) - 0.5
        self.weight_ho = np.random.rand(output_size, hidden_size) - 0.5
        # Options: more complexed initial weight
        # self.weight_ih = np.random.normal(0.0, pow(hidden_size, -0.5), (hidden_size, input_size))
        # self.weight_ho = np.random.normal(0.0, pow(output_size, -0.5), (output_size, hidden_size))

    def train(self, input, output):
        input_data = np.array(input, ndmin = 2).T
        output_target = np.array(output, ndmin = 2).T
        # transfer
        hidden_data = transfer(self.weight_ih, input_data)
        output_data = transfer(self.weight_ho, hidden_data)
        # errors
        output_errors = output_target - output_data
        hidden_errors = np.dot(self.weight_ho.T, output_errors)
        # feedback
        self.weight_ho += self.alpha * np.dot((output_errors * output_data * (1. - output_data)), hidden_data.T)
        self.weight_ih += self.alpha * np.dot((hidden_errors * hidden_data * (1. - hidden_data)), input_data.T)


    def query(self, input):
        input_data = np.array(input, ndmin = 2).T
        hidden_data = transfer(self.weight_ih, input_data)
        output_data = transfer(self.weight_ho, hidden_data)
        return output_data

