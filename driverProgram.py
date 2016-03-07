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
mini_batch_size = 1000
net = Network([FullyConnectedLayer(n_in=784, n_out=100), SoftmaxLayer(n_in=100, n_out=10)], mini_batch_size) 
net.SGD(training_data, 60, mini_batch_size, 0.1, validation_data, test_data)
