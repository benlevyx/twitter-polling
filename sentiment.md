---
layout: page
title: Sentiment Analysis
---


### Goal

The goal of this component was to calculate the sentiment score of a tweet ranging from 0 to 1. A sentiment score below 0.5 and closer to 0 corresponds to negative sentiment, whereas a sentiment score greater than 0.5 and closer to 1 corresponds to positive sentiment. 

### Training data

The dataset that we used to train our classifier is the Sentiment140 [dataset](http://help.sentiment140.com/for-students) which consists of 1.6 million labeled tweets of multifarious content. In the early stages of development, this dataset was augmented with cases from the Twitter US Airline Sentiment [dataset](https://www.kaggle.com/crowdflower/twitter-airline-sentiment). However, we quickly realized that the type and tone of language used in airline short reviews differs significantly from this used in political comments. For example, this dataset contained many cases classified as positive sentiment tweets in which a user would write "thank you" to show appreciation for the services of a particular airline. However, we observed that in the vast majority of political tweets related to the democratic primaries, the phrases "thank you" or "no, thanks" were used in a sarcastic manner to convey negative sentiment about a candidate. Hence, we decided to remove this dataset from our training data. Instead, we augmented Sentiment140 with the GOP Debate Twitter Sentiment [dataset](https://www.kaggle.com/crowdflower/first-gop-debate-twitter-sentiment) which consists of 13900 labelled tweets related to the GOP Debate held in August 2016. This dataset was used since it contains tweets with similar content and language to the tweets related to the democratic primaries.

The final model was trained on 966436 instances, validated on 322147 instances and tested on a held out test set of 322147 instances. All of the sets contained a mix of randomly shuffled Sentiment140 and GOP Debate tweets.



### Preprocessing

The tweets were first preprocessed to remove hashtags, mentions and web links, which do not carry any syntactic information or sentiment signal. We also defined a list of stopwords which are the most frequently used words not carrying any sentiment information (e.g. “the”, “a”, “this”, “you” etc.) and removed such words from each tweet. Please note that words like "no" or "not" may be considered stopwords in the NLP literature, however, in the scope of sentiment analysis, such words drive the polarity of a sentence. For example, the word "nice" should result in positive sentiment. However, the phrase "not nice" should result in negative sentiment. Hence, we did not remove such words from the tweets.

Furthermore, Sentiment140 comes preprocessed, since emoticons have already been removed by tweets. In the same fashion, we removed emoticons from the GOP Debate Twitter Sentiment dataset. As it is also mentioned in literature (Go et al. 2009), stripping out the emoticons lets the model learn from the other words used in the sentence. Instead, if emoticons are not stripped off, classifiers tend to put a high weight on the emoticons which results in lower performance when trying to classify tweets without emoticons or with multiple ones.

### Model

Deep neural networks achieve state-of-the-art performance on natural language processing so we decided to experiment with various deep learning architectures for this task using Keras. 

First, we fitted a baseline model which consisted of an embedding layer which was then fed to a densely connected layer. The embedding layer was also trained with the rest of the network. This achieved a validation accuracy of about 79%. 

We then experimented with recurrent neural networks and particularly LSTM architecture. We also tried a bidirectional LSTM network but this did not achieve a higher performance than the unidirectional LSTM network.

Finally, we also experimented with using a pre-trained embedding layer instead of training it together with the rest of the layers added on top of it.

The model that we chose in the end is a recurrent neural network. Specifically, the first layer is an embedding layer which maps each word to a vector in a 100-dimensional space. The weights of this layer were not trained since we used a pre-trained Twitter GloVE word embedding fitted on 2 billion tweets (https://nlp.stanford.edu/projects/glove/). The embedding layer feeds to a sequence of two LSTM layers of 64 and 32 neurons respectively, which then feed to a densely connected hidden layer of 32 neurons which uses the ReLU activation function. Finally, there is an output layer of one neuron which uses the sigmoid activation function to constrain the score between 0 and 1.

The code developed to fit the models can be found [here](https://github.com/benlevyx/twitter-polling/blob/master/notebooks/sentiment%20analysis/sentiment_analysis_exploration.ipynb).

### Performance
Unfortunately, it was not possible to test the performance of the model on a large number of tweets related to the Democratic primaries, since relevant labelled Twitter datasets are not publicly available.

Instead, we held out 20% of the training dataset (more than 300000 tweets) to check how the model generalizes to unseen data. Similar to the training set, the test set consists of cases from both the Sentiment140 dataset and the GOP debate Twitter Sentiment dataset. Hence, the model was tested on a mix of political and non-political tweets. The model achieved accuracy of 0.82 on test set 
The train and test set accuracy analysis of the selected model is summarized [here](https://github.com/benlevyx/twitter-polling/blob/master/notebooks/sentiment%20analysis/sentiment_final_model.ipynb).


