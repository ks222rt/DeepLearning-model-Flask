# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 11:03:17 2017

@author: Kristoffer
"""

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


class TextCNN(object):
    
    def __init__(self, sequence_length, num_classes, vocab_size, 
                 embedding_size, filter_size, num_filters):
        self.sequence_length = sequence_length
        self.num_classes = num_classes
        self.vocab_size = vocab_size
        self.embedding_size = embedding_size
        self.filter_size = filter_size
        self.num_filters = num_filters
        
        