# Final Writeup

## Introduction and motivation (MM)
With the democratic primary elections coming up in 2020, polls that describe and predict the popularity of each candidate get increasing attention. Since the presidential elections of 2016, the accuracy of these polls have been fundamentally critized. It turns out that generalizing limited, often biased voting samples for an entire nation is a very hard to thing to do. Additionally, polls are only able to capture trends in popularity with a certain delay. If candidate X has performed great in a certain debate or a recent scandal about candidate Y was brought to light, the impact on the polls is only seen after at least a couple of days. 

This project will attempt to tackle these two intrinsic flaws of the current polling systems by using Twitter data. Potentially, sentiment expressed in tweets mentioning a certain candidate relates to the popularity of that same candidate. If this would be the case, polls could be updated by following the twitter sentiment over time. As such, the sample sizes are significantly expanded due to the large amount of tweets are posted at every moment and the public opinion about certain events can be captured instantaneously. This website describes the different steps taken to assess the feasibility of the above-described goal. Note that this project will only focus on the five most popular candidates for the democratic elections: Joseph Biden, Peter Buttigieg, Kamala Harris, Bernie Sanders and Elizabeth Warren. 

First, a short literature review is discussed. Predicting elections has always been a hot-topic, leading too many different approaches discussed in literature. Understanding what has been done before with according results is a crucial first step before performing any analysis.

Secondly, the best data source will be identified and consecutive collection will be executed. For the tweets, the Twitter API is used to scrape all posts mentioning the five candidates considered from early March until mid November 2019. Additionally, 'ground truth' polling data needs to be collected to assess the correlation with the twitter sentiment. Realizing that such a thing does not exist, the best source for multiple pollster data appeared to be the well-known FiveThirtyEight.com. The actual implementation of collecting the tweets and ground truth polling data will be discussed in the section 'Data Selection'.





## Literature review (BL)

## Data collection

### Twitter (BL)

### Polls (ground truth) (WF)

In order to evaluate how well our sentiment analysis-based predictions align with the true candidate popularity, we needed to establish the ground truth popularity of each candidate as a function of time based on polling data. To do this, we relied on FiveThirtyEight (data.fivethirtyeight.com) polling data  from March 1st, 2019, when the race began to heat up and the polls became more consistent, to the present. Because it would be difficult to analyze candidates that have consistently had very little support, we only considered those candidates that have achieved at least 5% support at some point in the nomination campaign. Therefore, we limited our analysis to Joe Biden, Bernie Sanders, Elizabeth Warren, Kamala Harris and Pete Buttigieg.

With the polling data at hand, the first step was to examine each poll and select only those that were conducted nationally (as opposed to at the state level) and those that asked respondents to select which candidate they prefer out of the entire field. Having obtained these particular polls, the next step was to build a model that would approximate the true support each of candidate on each day since March 1st. A naïve approach would have been to treat all of the polls equally and apply some sort of nonparametric model to create a smooth curve through the polling data. However, given that each poll has a different sample size and each pollster has a different rating from FiveThirtyEight, it made more sense to weigh the influence of each poll by some combination of these two factors. (For background, FiveThirtyEight assigns ratings to each pollster based on its methodology and historical accuracy. For example, pollsters that conducted their surveys over the phone are deemed more credible than those that conduct online surveys, and thus generally receive a higher rating from FiveThirtyEight).

The weight associated with the sample size, $n$, of a given poll was defined to be $\sqrt{n}$. The statistic justification for this decision is that given a fraction, $p$, of voters that truly support a given candidate, the sampling distribution of a well-conducted poll is $N(p, \frac{p(1-p)}{n})$. Given that the standard deviation of the sampling distribution is inversely proportional to $\sqrt{n}$, the confidence of the given poll is also on the order of $\sqrt{n}$. 

Meanwhile, the weight assigned to FiveThirtyEight’s pollster ratings was set to $e^(-\lambda * x)$ where x is a mapping from ratings to numbers such that A+, A and B respectively correspond to 0, 1 and 4, etc., and lambda is a hyperparameter to optimize. This exponentially decaying function guarantees that higher ratings are given a larger weight. Linearly combining these two credibility-related factors, the final weight assigned to a given poll was alpha * sqrt(n) + (1-alpha) * e ^(-lambda *x) where lambda and alpha are hypermeters to tune. 

Before we could optimize the hyperparameters defined above, we first had to select a flexible model that could accurately fit the polling data for each of the five candidates under consideration and could handle different weights for each of the data points. The following nonparametric techniques were dismissed because they don’t support weighted observations: Gaussian process, LOESS, kNN and Nadaraya-Watson kernel regression, while the following nonparametric techniques were rejected because they resulted in extremely jagged curves: cubic spline, support vector regression and kernel ridge regression. Overall, the most suitable model among those considered was random forest (which is equivalent to bagging in this case since there is only one feature). 
Having specified the model, the next step was to optimize the hyperparameters. This process was complicated by the fact that we have no way of knowing the true support of each candidate at each point in time – all we have access to are the polls that estimate this support. To bypass this circular pattern in which the polling data is used to estimate the ground truth, which, in turn, is used to evaluate the models that are creating using the polling data, the data-generating process of the polls was thought of in the following way: each poll is an unbiased estimator of the true percentage of support of a given candidate and has noise around that true value that is inversely proportional to the weight associated with the given poll. (Note: although individual pollsters tend to have some degree of bias in a certain direction according to FiveThirtyEight, we can invoke the law of large numbers and assume that the dozens of pollsters that conduct the polls are collectively unbiased.) 

This view about the data generating process enabled us to estimate the ground truth and select the optimal hyperparameters in a principled manner. Regarding the ground truth, if a poll has a relatively high weight, then we’d expect it to be closer, on average, to the ground truth than a poll with a relatively low weight. As such, it makes sense to rely more heavily on the poll with the larger weight to guide our belief about the actual, ground truth polling data. Therefore, we estimated the ground truth by building a random forest model where each poll was weighted by the weight defined by a given value of alpha and lambda. 

In terms of selecting the optimal hyperparameters, the key task was to define an objective function to minimize over. Our view of the data generating process provided a logical choice for an objective function – simply weigh the squared error between our estimated ground truth polling data and the observed polling data by the given poll’s corresponding weight. This is a reasonable approach because if a given poll has a relatively high weight, we don’t expect it to deviate significantly from the ground truth, which means that if it does, the penalty should be relatively high since this provides strong evidence against our current belief of the ground truth. On the other hand, if a given poll has a relatively low weight, we expect it to have a lot of noise, so even if it is far from the estimated ground truth it doesn’t offer much evidence against our current belief of the ground truth and thus shouldn’t be heavily penalized. 

With this framework in place, the next step was to determine which estimated ground truth is most consistent with the observed polling data by choosing different values of alpha and lambda and identifying which pair of hyperparameters minimized the weighted mean squared error. 

Pseudocode for algorithm described above:

- Perform a grid search over plausible values of alpha and lambda 
-	Initialize cost to 0
-	Iterate over five candidates
o	Extract relevant polling info and calculate weight for each poll based on current values of alpha and lambda
o	Determine the optimal depth of the regression trees using 5-fold cross validation where the squared error associated with each poll is weighted by the corresponding weight
o	Build a random forest model where the depth is set to the optimal depth 
o	Obtain an overall mean squared error by again performing weighted 5-fold cross validation and averaging over the mean squared errors of each of the folds
o	Add overall mean squared error to cost

-  Select the pair (alpha, lambda) that minimizes the weighted mean squared error across all five candidates. 


Finally, a 6-day running average was used to smooth out our best guess of the underlying ground truth.


## Sentiment analysis (DV)

### Goal

The goal of this component was to calculate the sentiment score of a tweet ranging from 0 to 1. A sentiment score below 0.5 and closer to 0 corresponds to negative sentiment whereas a sentiment score greater than 0.5 and closer to 1 corresponds to positive sentiment. 

### Training Data

The dataset that we used to train our classifier is the Sentiment140 dataset (http://help.sentiment140.com/for-students) which consists of 1.6 million labelled tweets of multifarious content. We augmented this dataset with GOP Debate Twitter Sentiment dataset (https://www.kaggle.com/crowdflower/first-gop-debate-twitter-sentiment) which consists of 13900 labelled tweets related to the GOP Debate held in August 2016. This dataset was used since it probably contains tweets with similar content and language used to the tweets that we want to classify.

### Preprocessing

The tweets were first preprocessed to remove hashtags, mentions and web links which do not carry any syntactic information or sentiment signal. We also defined a list of stopwords which are the most frequently used words not carrying any sentiment information (e.g. “the”, “a”, “this”, “you” etc.) and removed such words from each tweet. 

### Model

Deep neural networks achieve state-of-the-art performance on natural language processing so we decided to experiment with various deep learning architectures for this task using Keras. 

First, we fitted a baseline model which consisted of an embedding layer which was then fed to a densely connected layer. The embedding layer was also trained with the rest of the network. This achieved a validation accuracy of about 79%. 

We then experimented with recurrent neural networks and particularly LSTM architecture. We also tried a bidirectional LSTM network but this did not achieve a higher performance than the unidirectional LSTM network.

Finally, we also experimented with using a pre-trained embedding layer instead of training it together with the rest of the layers added on top of it.

The model that we chose in the end is a recurrent neural network. Specifically, the first layer is an embedding layer which maps each word to a vector in a 100-dimensional space. The weights of this layer were not trained since we used a pre-trained Twitter GloVE word embedding fitted on 2 billion tweets (https://nlp.stanford.edu/projects/glove/). The embedding layer feeds to a sequence of two LSTM layers of 64 and 32 neurons respectively, which then feed to a densely connected hidden layer of 32 neurons which uses the ReLU activation function. Finally, there is an output layer of one neuron which uses the sigmoid activation function to constrain the score between 0 and 1.

The code developed to fit the models can be found in https://github.com/benlevyx/twitter-polling/blob/master/notebooks/sentiment_analysis_exploration.ipynb .
The train and test set accuracy analysis of the selected model is summarized in https://github.com/benlevyx/twitter-polling/blob/master/notebooks/sentiment_final_model.ipynb .



## EDA (MM)

## Modelling

### Baseline regression models 

Following EDA, we wanted to confirm in a statistical way whether the aggregated twitter sentiment for each candidate is correlated to its popularity as this is measured by polls (what we refer to as ground truth above). To do this, for each candidate, we did a basic regression analysis to calculate the statistical significance of twitter sentiment as a predictor of ground truth. First, we fitted an OLS model by regressing the ground truth weekly time series on the aggregated mean twitter sentiment for the week before each poll date. The p-value provided by statmodels summary method was very high for all candidates. This indicated that there is no evidence against the null hypothesis that the coefficient of the sentiment predictor is 0. In other words, the aggregated sentiment was not statistically significant. We also repeated the same analysis by regressing the ground truth weekly percentage change on the weekly sentiment percentage change. The p-values were also very high for this experiment.

In summary, these experiments proved that the aggregated twitter sentiment did not provide signfiicant signal to predict the outcome of the next poll.

### Kalman filter (DV)
Our initial thought was to fit a separate Kalman filter (state-space model) for each candidate to predict his/her latent true popularity by modelling it as a linear dynamical system. The state of the system would be the true proportion of the electorate voting for a specific candidate, which is a latent variable. In short, our idea was that the current state of the system should be equal to the previous state of the system plus/minus the effect from twitter sentiment. In other words, we could consider the state of the system as the position of a moving object Then, we could consider the sequantial weekly polls as well as the weekly aggregated twitter sentiment as noisy observations generated based on the state of the system at each point. 


### Bayesian model (WF)


## Conclusion and possible improvements (All)
