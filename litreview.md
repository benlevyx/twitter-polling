---
layout: page
title: Literature Review
---

There exists a considerable body of work in the computational social sciences attempting to use Twitter for predicting or explaining political outcomes. Many papers have directly attempted to "predict" electoral results (in quotations because these predictions are actually retrospective and therefore not true predictions) using various features derived from corpora of tweets for the time period before an election.

In general, the process of predicting election results from Twitter has consisted of four core tasks:

1. Tweet collection
2. Sentiment analysis and feature extraction
3. Definition of ground truth
4. Predictive modeling

### Tweet collection

The most common way in which tweets were gathered was through Twitter's official API. Two modes of collection are available: (1) the so-called "firehose" stream, which provides a random sample of roughly 1% of all Twitter traffic on a given day (used by Chung & Mustafaraj, 2011; Burnap et al., 2014), and (2) Twitter's enterprise API, which allows greater control over the tweet collection but comes at a monetary cost (used by Wang et al., 2012)

Some researchers also used publicly available datasets that had been published by Twitter (Tumasjan et al., 2010; Bollen et al., 2011). This, of course, comes with the limitation that these datasets are only available for specific time periods and that the collection and filtering processes are more opaque.

The sizes of corpora varied from hundreds of thousands (Tumasjan et al, 2010; Chung & Mustafaraj, 2011) to several million (Wang et al., 2012; Burnap et al., 2015; Bollen et al., 2011).

### Sentiment analysis and feature extraction

As noted by Gayo-Avello (2012), the apparent norm among studies of political sentiment on Twitter is to apply overly simplistic sentiment models with the hope that a large-enough corpus will compensate for the simplicity and lack of accuracy of the model. The following table summarizes some of the more common techniques for sentiment analysis on political tweets:

**Table 1:** Comparison of sentiment models in surveyed studies.

| --------+---------+-------- |
| Study | Type of sentiment model | Accuracy (if applicable) |
| -------- | -------- | -------- |
| Wang et al., (2012) | Manual annotation + supervised (Naive Bayes) | 59% |
| Tumasjan et al. (2010) | Lexicon-based (LIWC) | 
| Chung & Mustafaraj (2011) | Lexicon-based (SentiWordNet) | 
| Burnap et al. (2015) | Lexicon-based | 
Bermingham & Smeaton (2011) | Manual annotation + supervised learning (AdaBoost) | 65.09% |
Bollen et al. (2011) | Lexicon-based


The most popular features used were either raw counts of tweets over the entire time period of interest for each candidate/party, or some sort of relative "sentiment score" based on the numbers of positive and negative tweets and their sentiment magnitudes.

When it comes to general sentiment analysis on tweets of any theme, the most common techniques used in literature are Naive Bayes, support vector  mchines and logistic regression models while more complex approaches include convolutional and recurrent neural networks. The following table summarizes some of thet techniques which have been used in the past:

**Table 2:** Comparison of sentiment analysis models on Twitter.

| --------+---------+-------- |
| Study | Type of sentiment model | Accuracy (if applicable) |
| -------- | -------- | -------- |
| Socher et al., (2013b) | Recurrent Neural Networks | 82.4% |
| Socher et al., (2013b) | Naive Bayes | 81.8 |
| Socher et al., (2013b) | SVM | 79.4 |
| Sahni et al. (2009) |  Unigrams and Bigrams + Logistic Regression| 81.7
| Sahni et al. (2009) | Unigrams + Naive Bayes | 79.2


The simplistic approach to sentiment scoring seems to be one of the most significant limitations in the studies we have read. In general, sentiment analysis is a non-trivial task, and this is especially the case on Twitter, *particularly* in the realm of politics, where sarcasm, double entendre, ambiguous shorthands, and other linguistic oddities abound. Thus, building a strong sentiment classifier was one of the foci of our study.

### Definition of ground truth

Gayo-Avello also stresses the importance of a clearly defined ground truth for the task of prediction. There are a myriad of possible target variables, ranging from the results of the elections themselves, to political opinion polls, candidate approval polls, polls with specific candidates missing, polls with different questions (E.g. who would you vote for today? Who do you trust the most?), and polls collected through a variety of different methods with different degrees of reliability. Just like in the case of sentiment modeling, the definition of just what exactly is being predicted is non-trivial.

For instance, Tumasjan et al. (2010) sought to predict the percentage of seats won by each party in the 2009 German election. Similarly, Burnap et al. (2015) tried to predict the seat count for each party in the 2010 U.K. national election. On the other hand, Chung & Mustafaraj (2011) attempted to predict the share of the vote for each candidate in a U.S. Senate special election. Bermingham & Smeaton (2011) opted to predict election results in Ireland by training their regression model on public opinion polls.

An important distinction arises in these studies: the difference between election result prediction (i.e. predicting the winner of an election or some outcome measure like seat percentage) and popularity (i.e. predicting political polls). It is important to clearly define and justify whether Twitter data are being used to predict how *individuals feel* about a given politician or political party, versus how the election results actually turn out. For instance, in the parliamentary systems in some of the papers (U.K., Germany, Ireland), winning seats may not necessarily correlate with how *individuals feel* and therefore may not have the same relationship wtih Twitter as, say, head-to-head contests as seen in the United States.

### Predictive modeling

Similar to the simplicity of the sentiment models, the models for predicting election outcomes are rather simple in the papers surveyed. However, unlike the task of predicting sentiment from text, predicting poll outcomes (a better-defined, quantitative outcome variable) from quantitative predictors (sentiment and other indices) is much more straightforward. Here are the models used and relevant statistics from the papers surveyed:


**Table 2:** Comparison of prediction models in surveyed studies.

| Paper | Method | Accuracy measure (if applicable) |
| -------- | -------- | -------- |
| Tumasjan et al. (2010) | Non-parametric (share of traffic) | 1.65% mean absolute error |
| Chung & Mustafaraj (2011) | Non-parametric | 41.41% accuracy
|Burnap et al. (2015) | Non-parametric | None reported
| Bermingham & Smeaton (2011) | Linear regression | ~4% mean absolute error |

### Conclusions from literature search

There appears to be a gap in the literature on the four fronts discussed above. Thus, in this project, we hope to use advanced data science techniques to build a more robust model that can better answer the question, "can Twitter be used to predict public opinion in politics?"
