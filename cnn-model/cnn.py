# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 11:03:17 2017

@author: Kristoffer
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.cross_validation import train_test_split
import tflearn
import tensorflow as tf
from tflearn.data_utils import VocabularyProcessor
from tflearn.data_utils import pad_sequences, to_categorical, load_csv
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_1d, global_max_pool
from tflearn.layers.merge_ops import merge
from tflearn.layers.estimator import regression

batch_size = 64
# Import dataset from csv file and drop unecessary field
#dataset = pd.read_csv('datasetFullList')
#dataset.drop('index', axis=1, inplace=True)

X, Y = load_csv('datasetFullList', target_column = 2, columns_to_ignore = [0])

# Count max words from the longest sentence
#max_words = max([len(x.split()) for x in dataset['text']])
max_words = max([len(x[0].split(" ")) for x in X])

# Get vocabulare size from longest sentence
vocab = VocabularyProcessor(max_words)

# Encode pos, neu and neg to numbers
labelEncoder = LabelEncoder()
#labelEncoder.fit(dataset['rating'])
#dataset['rating'] = labelEncoder.transform(dataset['rating'])
labelEncoder.fit(Y)
Y = labelEncoder.transform(Y)

# Split dataset to 2 lists
#X = dataset['text']
#Y = dataset['rating']

# Change the list of sentences to a list of sequence of words
X = np.array(list(vocab.fit_transform([x[0] for x in X])))

# Split the datasets to training set and test test
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.20, random_state = 1)

# Pad the sequences to fit the longest sentence
X_train = pad_sequences(X_train, maxlen = max_words, value=0.)
X_test = pad_sequences(X_test, maxlen = max_words, value=0.)

# Convert labels to binary vector
Y_train = to_categorical(Y_train, nb_classes = 3)
Y_test = to_categorical(Y_test, nb_classes = 3)

cnn_model = input_data(shape=[None, max_words], name='input')
cnn_model = tflearn.embedding(cnn_model, input_dim = len(vocab.vocabulary_), output_dim = 128)
#cnn_model= tflearn.layers.core.reshape(cnn_model, new_shape = [batch_size, 1, max_words, 128])
branch1 = conv_1d(cnn_model, nb_filter = 100,  filter_size = 3, padding = 'same', activation = 'relu', regularizer = 'L2')
branch2 = conv_1d(cnn_model, nb_filter = 100,  filter_size = 4, padding = 'same', activation = 'relu', regularizer = 'L2')
branch3 = conv_1d(cnn_model, nb_filter = 100,  filter_size = 5, padding = 'same', activation = 'relu', regularizer = 'L2')
cnn_model = merge([branch1, branch2, branch3], mode = 'concat', axis = 1)
cnn_model = tf.expand_dims(cnn_model, 2)
cnn_model = global_max_pool(cnn_model)
cnn_model = dropout(cnn_model, 0.5)
cnn_model = fully_connected(cnn_model, 3, activation = 'softmax')
cnn_model = regression(cnn_model, optimizer = 'adam', learning_rate = 0.001, 
                       loss = 'categorical_crossentropy', name = 'target')

model = tflearn.DNN(cnn_model, tensorboard_verbose = 0)
model.fit(X_train, Y_train, n_epoch = 5, shuffle = False, validation_set=(X_test, Y_test), show_metric = True, batch_size = batch_size)


validate = [['Restaurangens mat var så pass dålig att jag spydde'], ['Älskar den servicen som de ger'], ['vet ej vad jag skall säga, inget dåligt inget bra']]
validate_x = np.array(list(vocab.transform([x[0] for x in validate])))
validate_x = pad_sequences(validate_x, maxlen = max_words, value = 0.)
result = model.predict(validate_x)





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
        