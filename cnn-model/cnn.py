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

# Import dataset from csv file and drop unecessary field
dataset = pd.read_csv('datasetFullList')
dataset.drop('index', axis=1, inplace=True)

# Count max words from the longest sentence
max_words = max([len(x.split()) for x in dataset['text']])

# Get vocabulare size from longest sentence
vocab = learn.preprocessing.VocabularyProcessor(max_words)

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
X_train = sequence.pad_sequences(X_train, maxlen = max_words)
X_test = sequence.pad_sequences(X_test, maxlen = max_words)

max_features = X.max(axis = 0)
max_features = max_features.max()


# Build the CNN model
model = Sequential()
model.add(Conv1D(nb_filter = 75, filter_length = 3, activation = 'relu',
                 input_dim = 3, input_length = max_words))
model.add(Dropout(1/5))
model.add(MaxPooling1D(pool_length = 8))
model.add(Flatten())
model.add(Dense(100, activation = 'relu'))
model.add(Dropout(0.5))
model.add(Dense(30, activation = 'relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation = 'sigmoid'))
model.compile(loss = 'binary_crossentropy', optimizer = 'adam', class_mode = 'binary')

















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
        