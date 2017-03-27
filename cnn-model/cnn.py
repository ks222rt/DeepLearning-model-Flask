# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 11:03:17 2017

@author: Kristoffer
"""

"""import tensorflow as tf"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.cross_validation import train_test_split
from tensorflow.contrib import learn
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Embedding
from keras.layers import Conv1D, Flatten, Dropout, Dense, pooling, Activation

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

model.add(Embedding(max_features, 50, input_length=max_words))
model.add(Dropout(float(1)))
model.add(Conv1D(64, 5))
model.add(pooling.MaxPooling1D())
model.add(Dense(250))
model.add(Dropout(0.2))
model.add(Activation('relu'))
model.add(Dense(1))
model.add(Activation('sigmoid'))





















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
        