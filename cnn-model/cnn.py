# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 11:03:17 2017

@author: Kristoffer
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.cross_validation import train_test_split
from tensorflow.contrib import learn
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Embedding
from keras.layers import Conv1D, Flatten, Dropout, Dense, MaxPooling1D, Activation

import tflearn
import tensorflow as tf
from tflearn.data_utils import VocabularyProcessor
from tflearn.data_utils import pad_sequences
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_1d, global_max_pool
from tflearn.layers.merge_ops import merge
from tflearn.layers.estimator import regression


# Import dataset from csv file and drop unecessary field
dataset = pd.read_csv('datasetFullList')
dataset.drop('index', axis=1, inplace=True)

# Count max words from the longest sentence
max_words = max([len(x.split()) for x in dataset['text']])

# Get vocabulare size from longest sentence
vocab = VocabularyProcessor(max_words)

# Encode pos, neu and neg to numbers
labelEncoder = LabelEncoder()
labelEncoder.fit(dataset['rating'])
dataset['rating'] = labelEncoder.transform(dataset['rating'])

# Split dataset to 2 lists
X = dataset['text']
Y = dataset['rating']

# Change the list of sentences to a list of sequence of words
X = np.array(list(vocab.fit_transform(X)))

# Split the datasets to training set and test test
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.20, random_state = 1)

# Pad the sequences to fit the longest sentence
X_train = pad_sequences(X_train, maxlen = max_words, value=0.)
X_test = pad_sequences(X_test, maxlen = max_words, value=0.)

max_features = X.max(axis = 0)
max_features = max_features.max()

cnn_model = input_data(shape=[None, max_words], name='input')
cnn_model = tflearn.embedding(cnn_model, input_dim = max_features, output_dim = 128)
branch1 = conv_1d(cnn_model, 128, 3, padding = 'valid', activation = 'relu', regularizer = 'L2')
branch2 = conv_1d(cnn_model, 128, 4, padding = 'valid', activation = 'relu', regularizer = 'L2')
branch3 = conv_1d(cnn_model, 128, 5, padding = 'valid', activation = 'relu', regularizer = 'L2')
cnn_model = merge([branch1, branch2, branch3], mode = 'concat', axis = 1)
cnn_model = tf.expand_dims(cnn_model, 2)
cnn_model = global_max_pool(cnn_model)
cnn_model = dropout(cnn_model, 0.5)
cnn_model = fully_connected(cnn_model, 2, activation = 'softmax')
cnn_model = regression(cnn_model, optimizer = 'adam', learning_rate = 0.001, 
                       loss = 'categorical_crossentropy', name = 'target')

model = tflearn.DNN(cnn_model, tensorboard_verbose = 0)
model.fit(X_train, Y_train, n_epoch = 5, shuffle = True, validation_set=(X_test, Y_test), show_metric = True)















"""class TextCNN(object):
    
    def __init__(self, sequence_length, num_classes, vocab_size, 
                 embedding_size, filter_size, num_filters):
        self.sequence_length = sequence_length
        self.num_classes = num_classes
        self.vocab_size = vocab_size
        self.embedding_size = embedding_size
        self.filter_size = filter_size
        self.num_filters = num_filters
   """     
        