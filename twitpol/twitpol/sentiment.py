import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from keras.models import Sequential
from keras.layers import Embedding, Flatten, Dense, LSTM
from keras import optimizers
from keras import losses
from keras import metrics
from keras import callbacks

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.text import tokenizer_from_json
from keras.preprocessing.sequence import pad_sequences

import json
from twitpol import config


stopwords = []
with open(config.DATA / 'sentiment' / 'stopwords.txt') as f:
    lines = f.readlines()
for i in range(1,len(lines)):
    stopwords.append(lines[i].strip())


emoticons = []
with open(config.DATA / 'sentiment' / 'emoticons.txt') as f:
    lines = f.readlines()
for i in range(1,len(lines)):
    emoticons.append(lines[i].strip())


#function to remove hashtags and mentions
#remove stopwords and emoticons
#trasform everything to lowercase
def preprocess_tweet(tweet):
    tweet_lower = tweet.lower()
    tweet_words = tweet_lower.split()
    toberemoved = []
    for word in tweet_words:
        if word.startswith('@') or word.startswith('#') or word.startswith('http'):
            toberemoved.append(word)
        elif word in stopwords or word in emoticons:
            toberemoved.append(word)
    for word in toberemoved:
        tweet_words.remove(word)

    return ' '.join(tweet_words)



#function that gives the sentiments given a list of tweets
#and a tokenizer which has been fitted on the training set
def predict_sentiment(tweets):
    #load tokenizer
    with open(config.DATA / 'sentiment' / 'tokenizer_200k.json') as f:
        data = json.load(f)
        tokenizer = tokenizer_from_json(data)

    #compile the keras model
    embedding_dim = 100
    max_words = 300000
    max_length = 50
    lstm_model4 = Sequential()
    lstm_model4.add(Embedding(max_words, embedding_dim, input_length=max_length))
    lstm_model4.add(LSTM(64, return_sequences=True))
    lstm_model4.add(LSTM(32))
    lstm_model4.add(Dense(32, activation='relu'))
    #output layer
    lstm_model4.add(Dense(1, activation='sigmoid'))
    lstm_model4.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])
    lstm_model4.load_weights(config.MODELS / 'sentiment'/ 'LSTM_model5_nostop.h5')
    #pre-process tweets to remove mentions and hashtags
    political_tweets_proc = list(map(preprocess_tweet, tweets))
    #transform the tweets to sequences of numbers
    pol_seqs = tokenizer.texts_to_sequences(political_tweets_proc)
    #pad with zeros
    pol_seqs_padded = pad_sequences(pol_seqs, maxlen=max_length)
    return lstm_model4.predict(pol_seqs_padded)



    