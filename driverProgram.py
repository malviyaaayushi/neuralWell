import network
from network import Network
from network import ConvPoolLayer, FullyConnectedLayer, SoftmaxLayer
import cPickle
import gzip

# Third-party libraries
import numpy as np
import theano
import theano.tensor as T


#training_data, validation_data, test_data = network.load_data_shared()
training_data, validation_data, test_data = network.load_data_shared("data/data.pkl.gz")
mini_batch_size = 10
size_x = 100
size_y = 100
num_possible_outcomes = 3
num_pixels = size_x * size_y
net = Network([FullyConnectedLayer(n_in=num_pixels, n_out=1000), SoftmaxLayer(n_in=1000, n_out=num_possible_outcomes)], mini_batch_size) 
net.SGD(training_data, 60, mini_batch_size, 0.1, validation_data, test_data)
