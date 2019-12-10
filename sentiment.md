---
layout: page
title: Sentiment Analysis
---


### Goal

The goal of this component was to calculate the sentiment score of a tweet ranging from 0 to 1. A sentiment score below 0.5 and closer to 0 corresponds to negative sentiment, whereas a sentiment score greater than 0.5 and closer to 1 corresponds to positive sentiment. 

### Training data

The dataset that we used to train our classifier is the Sentiment140 [dataset](http://help.sentiment140.com/for-students) which consists of 1.6 million labeled tweets of multifarious content. We augmented this dataset with GOP Debate Twitter Sentiment [dataset](https://www.kaggle.com/crowdflower/first-gop-debate-twitter-sentiment) which consists of 13900 labelled tweets related to the GOP Debate held in August 2016. This dataset was used since it likely contains tweets with similar content and language to the tweets that we want to classify.

### Preprocessing

The tweets were first preprocessed to remove hashtags, mentions and web links, which do not carry any syntactic information or sentiment signal. We also defined a list of stopwords which are the most frequently used words not carrying any sentiment information (e.g. “the”, “a”, “this”, “you” etc.) and removed such words from each tweet. 

### Model

Deep neural networks achieve state-of-the-art performance on natural language processing so we decided to experiment with various deep learning architectures for this task using Keras. 

First, we fitted a baseline model which consisted of an embedding layer which was then fed to a densely connected layer. The embedding layer was also trained with the rest of the network. This achieved a validation accuracy of about 79%. 

We then experimented with recurrent neural networks and particularly LSTM architecture. We also tried a bidirectional LSTM network but this did not achieve a higher performance than the unidirectional LSTM network.

Finally, we also experimented with using a pre-trained embedding layer instead of training it together with the rest of the layers added on top of it.

The model that we chose in the end is a recurrent neural network. Specifically, the first layer is an embedding layer which maps each word to a vector in a 100-dimensional space. The weights of this layer were not trained since we used a pre-trained Twitter GloVE word embedding fitted on 2 billion tweets (https://nlp.stanford.edu/projects/glove/). The embedding layer feeds to a sequence of two LSTM layers of 64 and 32 neurons respectively, which then feed to a densely connected hidden layer of 32 neurons which uses the ReLU activation function. Finally, there is an output layer of one neuron which uses the sigmoid activation function to constrain the score between 0 and 1.

The code developed to fit the models can be found [here](https://github.com/benlevyx/twitter-polling/blob/master/notebooks/sentiment%20analysis/sentiment_analysis_exploration.ipynb).

### Performance
Unfortunately, it was not possible to test the performance of the model on a large number of tweets related to the Democratic primaries, since relevant labelled Twitter datasets are not publicly available.

Instead, we held out 20% of the training dataset (more than 300000 tweets) to check how the model generalizes to unseen data. Similar to the training set, the test set consists of cases from both the Sentiment140 dataset and the GOP debate Twitter Sentiment dataset. Hence, the model was tested on a mix of political and non-political tweets.
The train and test set accuracy analysis of the selected model is summarized [here](https://github.com/benlevyx/twitter-polling/blob/master/notebooks/sentiment%20analysis/sentiment_final_model.ipynb).


