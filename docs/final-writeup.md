# Can Twitter Predict the 2020 Democratic Primaries?

## Introduction and motivation 
With the Democratic primary elections coming up in 2020, polls that describe and predict the popularity of each candidate get increasing attention. However, since the presidential elections of 2016, the accuracy of these polls has been fundamentally critized. It turns out that generalizing limited, often biased voting samples to an entire nation is a very hard thing to do. Additionally, polls are only able to capture trends in popularity with a certain delay. If candidate X has performed great in a certain debate or a recent scandal about candidate Y was brought to light, the impact on the polls is only seen after at least a couple of days. 

This project will attempt to tackle these two intrinsic flaws of the current polling systems by leveraging Twitter data. Potentially, sentiment expressed in tweets mentioning a certain candidate relates to the popularity of that same candidate. If this would be the case, polls could be updated by following the Twitter sentiment over time. As such, the sample sizes are significantly expanded due to the large amount of tweets posted at every moment and the public opinion about certain events can be captured instantaneously. This website describes the different steps taken to assess the feasibility of the goal described above. Note that this project will only focus on the five most popular candidates for the democratic elections: Joseph Biden, Peter Buttigieg, Kamala Harris, Bernie Sanders and Elizabeth Warren. 

First, a short literature review is discussed. Predicting elections has always been a hot-topic, leading too many different approaches discussed in literature. Understanding what has been done before with according results is a crucial first step before performing any analysis.

Secondly, the best data source will be identified and consecutive collection will be executed. For the tweets, the Twitter API is used to scrape all posts mentioning the five candidates considered from early March until end of October 2019. Additionally, 'ground truth' polling data needs to be collected to assess the correlation with the twitter sentiment. Realizing that this does not exist, the best source for multiple pollster data appeared to be the well-known FiveThirtyEight.com. The actual implementation of collecting the tweets and ground truth polling data will be discussed in the section 'Data Collection'.

Consequently, a sentiment score should be assigned to all selected tweets. A deep neural network has been trained on an online available, labeled dataset to predict a score between 0 and 1 based on the actual words used in the tweet. Here, 0 and 1 correspond to a very negative and very positive sentiment, respectively. The optimal weights are then used to predict the sentiment on the political tweets that are collected.

After all data has been collected and generated, Exploratory Data Analysis (EDA) can be done. Visualizations of both tweet sentiment and ground truth show the general trends in the data.

Next, the association between the twitter sentiment over time and the ground truth can finally be assessed in a statistically rigorous way. Baseline regression, Kalman filter and Bayesian models will be discussed consequently. 

Lastly, the results from the analysis, appropriate conclusions and potential improvements will be discussed.


## Literature review 

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

As noted by Gayo-Avello (2012), the apparent norm among studies of political sentiment on Twitter is to apply overly simplistic sentiment models with the hope that a large-enough corpus will compensate for the simplicity and lack of accuracy of the model. The following table summarizes some of the more common techniques:

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

## Data collection

### Twitter 

In order to gain an accurate measure of overall sentiment for each candidate over the time period of interest (March to November 2019), we needed a dataset that was fully representative of each candidate's Twitter presence. Initially, we looked at using the [official Twitter API](https://developer.twitter.com/). However, Twitter places strict limits on overall download numbers and particularly limits the downloading of tweets dating more than 7 days before the download time. Thus, we had to find another option.

We decided to use the python package [`twint`](https://github.com/twintproject/twint). This package is an Open-Source Intelligence (OSINT) tool that is specifically designed for scraping tweets and user information from Twitter _without limits_. Under the hood, it uses asynchronous webscraping libraries commonly available in Python to query Twitter just like any other web browser. It then iterates through pages of results, returning all the information the user has requested.

Based on initial trials of the tool and our own manual searching, we determined that the task of scraping all the desired tweets would take well over a week and might involve upwards of a million tweets (the final total was over 2 million). Thus, we opted to do the data collection task using Amazon Web Services: first, we set up a virtual machine using AWS EC2 and connected it to a MySQL relational database. Then the Twitter scraper was run on the EC2 instance, periodically writing its scraped tweets to the database.

As we soon found out, the strength of the `twint` package (circumventing Twitter's API) was also its weakness: the tool was great at getting huge volumes of tweets but could unexpectedly miss entire weeks of data. Since this would have severely biased the counts of tweets and sentiment scores for each candidate, we had to re-run the scraper several times for days whose tweet counts were abnormally low. This techique may have introduced some additional over-correction bias (over-sampling from the same days for the same candidates may have reduced the probability of missing tweets for those candidates on those days); however this was dealt with by carefully smoothing the sentiment scores (see methods).

The code to run the scraper can be found [here](https://github.com/benlevyx/twitter-polling/blob/master/src/twitter_data/get_tweets_twint.py).

### Ground truth popularity 

In order to evaluate how well our sentiment analysis-based predictions align with the true candidate popularity, we needed to establish the ground truth popularity of each candidate as a function of time based on polling data. To do this, we relied on FiveThirtyEight polling [data](https://projects.fivethirtyeight.com/polls/) from March 1st, 2019, when the race began to heat up and the polls became more consistent, to the present. Because it would be difficult to analyze candidates that have consistently had very little support, we only considered those candidates that have achieved at least 5% support at some point in the nomination campaign. Therefore, we limited our analysis to Joe Biden, Bernie Sanders, Elizabeth Warren, Kamala Harris and Pete Buttigieg.

With the polling data at hand, the first step was to examine each poll and select only those that were conducted nationally (as opposed to at the state level) and those that asked respondents to select which candidate they prefer out of the entire field. Having obtained these particular polls, the next step was to build a model that would approximate the true support each of candidate on each day since March 1st. A naïve approach would have been to treat all of the polls equally and apply some sort of nonparametric model to create a smooth curve through the polling data. However, given that each poll has a different sample size and each pollster has a different rating from FiveThirtyEight, it made more sense to weigh the influence of each poll by some combination of these two factors. (For background, FiveThirtyEight assigns ratings to each pollster based on its methodology and historical accuracy. For example, pollsters that conducted their surveys over the phone are deemed more credible than those that conduct online surveys, and thus generally receive a higher rating from FiveThirtyEight).

The weight associated with the sample size, $n$, of a given poll was defined to be $\sqrt{n}$. The statistic justification for this decision is that given a fraction, $p$, of voters that truly support a given candidate, the sampling distribution of a well-conducted poll is $N(p, \frac{p(1-p)}{n})$. Given that the standard deviation of the sampling distribution is inversely proportional to $\sqrt{n}$, the confidence of the given poll is also on the order of $\sqrt{n}$. 

Meanwhile, the weight assigned to FiveThirtyEight’s pollster ratings was set to $e^{-\lambda x}$ where $x$ is a mapping from ratings to numbers such that A+, A and B respectively correspond to 0, 1 and 4, etc., and $\lambda$ is a hyperparameter to optimize. This exponentially decaying function guarantees that higher ratings are given a larger weight. Linearly combining these two credibility-related factors, the final weight assigned to a given poll was $\alpha \sqrt{n} + (1 - \alpha) e^{-\lambda x}$ where $\lambda$ and $\alpha$ are hypermeters to tune. 

Before we could optimize the hyperparameters defined above, we first had to select a flexible model that could accurately fit the polling data for each of the five candidates under consideration and could handle different weights for each of the data points. The following nonparametric techniques were dismissed because they don’t support weighted observations: Gaussian process, LOESS, kNN and Nadaraya-Watson kernel regression, while the following nonparametric techniques were rejected because they resulted in extremely jagged curves: cubic spline, support vector regression and kernel ridge regression. Overall, the most suitable model among those considered was a random forest (which is equivalent to bagging in this case since there is only one predictor). 

Having specified the model, the next step was to optimize the hyperparameters. This process was complicated by the fact that we have no way of knowing the true support of each candidate at each point in time – all we have access to are the polls that estimate this support. To bypass this circular pattern in which the polling data is used to estimate the ground truth, which, in turn, is used to evaluate the models that are creating using the polling data, the data-generating process of the polls was thought of in the following way: each poll is an unbiased estimator of the true percentage of support of a given candidate and has noise around that true value that is inversely proportional to the weight associated with the given poll. (Note: although individual pollsters tend to have some degree of bias in a certain direction according to FiveThirtyEight, we can invoke the law of large numbers and assume that the dozens of pollsters that conduct the polls are collectively unbiased.) 

This view about the data generating process enabled us to estimate the ground truth and select the optimal hyperparameters in a principled manner. Regarding the ground truth, if a poll has a relatively high weight, then we’d expect it to be closer, on average, to the ground truth than a poll with a relatively low weight. As such, it makes sense to rely more heavily on the poll with the larger weight to guide our belief about the actual, ground truth polling data. Therefore, we estimated the ground truth by building a random forest model where each poll was weighted by the weight defined by a given value of $\alpha$ and $\lambda$. 

In terms of selecting the optimal hyperparameters, the key task was to define an objective function to minimize over. Our view of the data generating process provided a logical choice for an objective function – simply weigh the squared error between our estimated ground truth polling data and the observed polling data by the given poll’s corresponding weight. This is a reasonable approach because if a given poll has a relatively high weight, we don’t expect it to deviate significantly from the ground truth, which means that if it does, the penalty should be relatively high since this provides strong evidence against our current belief of the ground truth. On the other hand, if a given poll has a relatively low weight, we expect it to have a lot of noise, so even if it is far from the estimated ground truth it doesn’t offer much evidence against our current belief of the ground truth and thus shouldn’t be heavily penalized. 

With this framework in place, the next step was to determine which estimated ground truth is most consistent with the observed polling data by performing a grid search over different values of $\alpha$ and $\lambda$ and identifying which pair of hyperparameters minimizes the weighted mean squared error. 

Pseudocode for algorithm described above:

* Perform a grid search over plausible values of $\alpha$ and $\lambda$
    * Initialize cost to 0
    * Iterate over five candidates
        * Extract relevant polling info and calculate weight for each poll based on current values of $\alpha$ and $\lambda$
        * Determine the optimal depth of the regression trees using 5-fold cross validation where the squared error associated with each poll is weighted by the corresponding weight
        * Build a random forest model where the depth is set to the optimal depth 
        * Obtain an overall mean squared error by again performing weighted 5-fold cross validation and averaging over the mean squared errors of each of the folds
        * Add overall mean squared error to cost


* Select the pair ($\alpha, \lambda$) that minimizes the weighted mean squared error across all five candidates. 

The optimal values of $\alpha$ and $\lambda$ turned out to be 0.4 and 0.075, respectively. 

Finally, a 6-day running average was used to smooth out our best guess of the underlying ground truth.

The resulting estimates are shown below for each candidate. In the plots, the transparency of each poll is set to the weight of each poll divided by the maximum weight of all the polls (therefore, the influence of each poll on the estimate is directly proportional to the darkness of the corresponding dot).
![](https://i.imgur.com/pHVNjUr.png)
![](https://i.imgur.com/Fih3pKr.png)
![](https://i.imgur.com/chUSz9b.png)
![](https://i.imgur.com/ZqVyGSu.png)
![](https://i.imgur.com/NgwqGd7.png)

The notebook that estimates this ground truth polling can be found [here](https://github.com/benlevyx/twitter-polling/blob/master/notebooks/ground%20truth/ground_truth_polls.ipynb).

## Sentiment analysis 

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
The train and test set accuracy analysis of the selected model is summarized [here](https://github.com/benlevyx/twitter-polling/blob/master/notebooks/sentiment%20analysis/sentiment_final_model.ipynb).



## EDA 

Having collected the tweets, estimated the ground truth popularity of each candidate and developed the sentiment analysis model the next step was to perform exploratory data analysis (EDA).

First, it is interesting to see how the sentiment analysis performs in general and on political tweets in particular. The following table gives a sample of some tweets that express a very strong opinion:

| Candidate | Tweet        | Sentiment    |
| :-------------: |:-------------:| -----:|
| Sanders | "Bernie fucked up.. He had his shot, Hillary plotted against him it's over for him.. He actually said he does not support Monterey compensation as part of reparations... Feel the bern as you GTFOH."     | 0.078 |
| Sanders   | "Haha sure he will!!!! that fictitious fund is where?"     | 0.971 |
| Buttigieg | "Pete Buttigieg promotes alcohol, abortion, illegal immigration, casinos, homosexuality, and men marrying men. The bible calls all of these sins that Jesus Christ died to deliver us from. Jesus dies for them, Buttigieg promotes them." | 0.078 |
| Buttigieg | "Mayor Pete, after watching this interview, you are my new preferred candidate. Thank you for running. Can you wait to hear you on the debate stage." | 0.939 |
| Harris | "Biden and Bernie need to allow a younger generation to rise. The two men did wonderful work & are good people. Time for Kamala & the many other candidates to claim the Presidency." | 0.549 |
| Biden | "Joe, I like you. I really do but saying shut up is drumphs way. You, we are better than that." | 0.834 |
| Warren | "This little fake Indian is smoking too much Peyote in her Tri-level Tee Pee! Elizabeth Warren Demands Special Protection For Transgender Migrants Trying To Enter The U.S." | 0.155 |

Clearly, the model is sometimes surprisingly good at grasping the underlying sentiment, while it fails in other cases. For instance, the last tweet in the table about Warren is clearly very negative and despite the metaphorical expression, the model predicts a very negative sentiment. On the other hand, for the second tweet about Sanders in the table, the model predicts a very positive sentiment while it is very likely that the writer meant it sarcastically. It is unfortunate that we are not able to get an overall performance of the sentiment analysis on our specific set of tweets but we will continue our project with the model as it is, keeping in mind the difficulty of predicting sentiment on political tweets before drawing any conclusions. 

Next, we can explore the distribution of the sentiment in all tweets for specific candidates. The following graphs illustrate for Warren and Biden how the sentiment is distributed as a function of the number of likes the corresponding tweet received. While it is hard to identify any trends from this, there might be a slightly higher number of likes for negative tweets than positive ones. 

![](https://i.imgur.com/s7eo0l7.png)

Consequently, the sentiment on Twitter can be plotted over time. As the end goal of this project is to eveluate the correlation between twitter data and popularity of a specific presidential candidate, we came up with two specific variables to consider over time: number of tweets and aggregated sentiment weighted by likes. 

The first variable allows us to explore how the amount of tweets mentioning a particular candidate relates to his/her popularity. For different sentiment cut-offs, the number of tweets for each candiddate is plotted over time on the figures below (left). The absolute ground truth over time from the polling data is plotted as well. Note that the number of tweets per day is divided by the max number of tweets that has happened during the entire timeframe considered. This has been done for visualization purposes only.

Secondly, the aggregated sentiment for every day has to be determined. Intuitively, it makes sense to weight a particular sentiment to its popularity, or number of likes. A representative sentiment for each day is thus computed as:

$$ 
sentiment_{d} = \frac{\sum_{i = 0}^N likes_i *sentiment_i}{\sum_{i = 0}^N likes_i}
$$

Here, d stands for a particular day and N corresponds to the total number of tweets mentioning a particular candidate posted that day. On the right figures below, this aggregated, weighted sentiment is plotted over time, again with the absolute ground truth overlaid.

![](https://i.imgur.com/CtYwNfP.png =340x250)
![](https://i.imgur.com/SdmEMdi.png =340x250)

![](https://i.imgur.com/krxNgVN.png =340x250)
![](https://i.imgur.com/smiDwz3.png =340x250)

![](https://i.imgur.com/2yHZQSk.png =340x250)
![](https://i.imgur.com/kVxdcbo.png =340x250)

![](https://i.imgur.com/By82NJL.png =340x250)
![](https://i.imgur.com/NhxoNSA.png =340x250)

![](https://i.imgur.com/nn8gLgS.png =340x250)
![](https://i.imgur.com/FksNjQc.png =340x250)

Both the number of tweets over time and the weighted aggregated sentiment show significant ups and downs. From the graphs alone, it is unsure whether these variables can relate to the ground truth. Some parts of the graphs might seem promising. For instance, the number of tweets for Biden appear to decrease when his popularity goes down. Similarly, the weighted aggregated sentiment for Harris seems to rise and fall around the same time as Harris' ground truth. Whether these potential trends are due to noise and coincidence or the twitter data is truly significant in elections polls, is to be determined in the modeling part below.


## Modeling

### Baseline regression models 

Following EDA, we wanted to determine in a statistically rigorous way whether the aggregated Twitter sentiment for each candidate is correlated with his/her popularity as measured by polls (what we refer to as ground truth above). To do this, we performed a basic regression analysis for each candidate to calculate the statistical significance of Twitter sentiment as a predictor of ground truth. First, we fitted an OLS model by regressing the ground truth weekly time series on the aggregated mean twitter sentiment for the week before each poll date. The p-value provided by Statmodels summary method was very high for all candidates. This indicated that there is no evidence against the null hypothesis that the coefficient of the sentiment predictor is zero. In other words, the aggregated sentiment was not statistically significant. We also repeated the same analysis by regressing the ground truth weekly percentage change on the weekly sentiment percentage change. The p-values were also very high for this experiment.

In summary, these experiments indicated that the aggregated Twitter sentiment did not provide significant signal to predict the outcome of the next poll.

### More advanced models

The next step after this preliminary regression analysis was to develop more advanced models that could make use of any possible signal present in the Twitter sentiment. But before we could begin the modeling process, we first had to specify the precise goal of any potential model. As explained in the introduction, the primary objective of this project is to determine the extent to which political tweets reflect the popularity of the candidates. Therefore, to help answer this question, we sought to develop a model that could use previous polls along with relevant tweets to predict future polling numbers (on the order of a few days up to a week in advance). If tweets do in fact shed light on the popularity of the candidates, we’d expect this information to produce estimates of the ground truth polling numbers that  are more accurate than those formed using previous polls alone. On the other hand, if the tweets are completely unrelated to the underlying popularity of the candidates, we’d expect this data to worsen the predictions, as the model would be misinterpreting this noise as signal.

### Kalman filter 
Our initial approach was to fit a separate Kalman filter (state-space model) for each candidate to predict  his/her latent true popularity by modeling it as a linear dynamical system. The state of the system would be two-dimensional; the first dimension would be the true proportion of the electorate that would vote for a specific candidate (i.e. popularity), while the second dimension of the state would be the true Twitter sentiment change for each candidate from one time step to the next. In short, our idea was that the current popularity of each candidate should be equal to his/her popularity at the previous time step, plus/minus the effect from the change in Twitter sentiment for this candidate. We could draw the following analogy to make the idea clearer: the first dimension of the state of the system is analagous to the position of a moving object at any given time, while for the second dimension of the system state, the true sentiment change is analagous to the velocity of the moving object. In other words, the current position of the object (true popularity of candidate) would depend on its previous position and its previous velocity (sentiment change).

Both the true sentiment change and the true popularity of each candidate are latent variables that we don't directly observe. Instead, we only get to observe noisy observations of these variables given by the polls (the ground truth time series that we constructed) and the sentiment change that we calculate based on a sample of tweets that we obtain on a daily basis.

However, unlike a moving object's position over time, which can be accurately described by kinematic equations, there was no clear relationship between the Twitter sentiment change and the popularity of the candidates in polls, as was indicated by the regression analysis discussed above. On the contrary, the regression analysis revealed that the aggregated sentiment or sentiment change is not correlated to the ground truth. For this reason, there was no principled way to write down the dynamics of the system in terms of actual transition and observation matrices used in the Kalman filter equations. Consequently, we decided not to proceed with this approach.


### Bayesian model 

An alternative way to approach this prediction task is from a Bayesian perspective. In the problem, we start off with the latest polls and then combine this information with recent tweet counts to predict future polling numbers. In this context, the latest polls represent our prior belief of the popularity of the candidates, while the tweet counts represent the data that we use to update our prior view to a posterior belief of the candidates’ popularity. To create a Bayesian model, we first had to set a prior distribution on the polling numbers of each candidate and specify the distribution from which the tweet counts are generated. 

Because the support of all candidates in the race must add up to one it was sensible to model the polling numbers as being Dirichlet distributed. (To handle the fact that the popularity of the top five candidates doesn’t sum to one, we scaled the support of each candidate proportionally to ensure that their cumulative support added up to one.) An added benefit of this Bayesian approach is that it allowed us to model the popularity of all the candidates jointly rather than having to model each candidate separately. In addition to simplifying the modeling process, this model better reflects reality since it automatically considers the fact that the candidates' support are negatively correlated with each other. 

In terms of the data-generating process of the tweets, we envisioned the number of positive tweets about each candidate as being generated at a rate that matches the true proportion of the Democratic electorate who support this candidate. In this model, each supporter of a given candidate independently decides (with very small probability) to post a positive tweet about their preferred candidate. To simplify matters, we disregarded negative tweets and slightly positive tweets that had a sentiment score between 0.5 and 0.6. We didn't take into account negative tweets since there was no easy way to combine these negative tweets with the positive tweets to create an overall polling score for each candidate (e.g. it didn't make sense to treat each negative tweet as a negative vote for the associated candidate since doing so would underestimate their true support and could even lead to a candidate receiving negative votes, which makes no sense). Another motivation for ignoring all negative tweets was that it ensured that we wouldn't inadvertantly be taking into account the views of Republican Twitter users who generally post negative tweets about the Democratic candidates but whose opinions have no influence on the Democratic primaries. 

Our view of the data-generating process coupled with the fact that we disregarded negative tweets enabled us to take advantage of Dirichlet-multinomial conjugacy, in which we modeled the positive tweets as being independently drawn from a multinomial distribution with five categories, each with a probability proportional to the true support of the corresponding candidate. 

Formally, our goal was to model the vector $\mathbf{\theta} = [\theta_1, ..., \theta_5]$ where $\theta_i$ represents the true proportion of the Democratic electorate supporting candidate $i$. Our prior belief on $\mathbf{\theta}$ is based on the latest available polls and is modeled as $\mathbf{\theta} \sim Dir([\alpha_1, ..., \alpha_5])$, where $\alpha_i$ is proportional to the support of candidate $i$ according to the latest polls. Meanwhile, the number of positive tweets ($X$) corresponding to each candidate is modeled as $\mathbf{X}|\mathbf{\theta} \sim MultiNom(\mathbf{\theta})$. 

The posterior distribution ($\mathbf{\theta}|\mathbf{X}$) is extremely straightforward to compute in this case due to conjugacy: $\mathbf{\theta}|\mathbf{X} \sim Dir([\theta_1 + X_1, ..., \theta_5 + X_5])$. Moreover, each $\alpha_i$ has the added interpretation of being the pseudocount of positive Tweets for candidate $i$. This means that the degree to which the posterior is influenced by the prior and data is proportional to $|\mathbf{\alpha}|_1$ and $|\mathbf{X}|_1$, respectively. 

Having specified the model, we first wanted to see how the posterior estimates of the candidates' polling numbers compare to their true polling numbers when the weight of the prior is equal to the weight of the data. The plots below compare the ground truth time series with the posterior mean times series for each candidate. From a preliminary visual inspection, it can be observed that the posterior estimates of the support for each candidate are not correlated with the ground truth polls. 

The code used to generate the following plots can be found [here](https://github.com/benlevyx/twitter-polling/blob/master/notebooks/dirichlet%20model/dirichlet_model_visualization.ipynb).

![](https://i.imgur.com/PgSfZOf.png)

Next, we sought to quantitatively measure the extent to which the number of positive tweets about each candidate is related to the candidate's true support. To do this, we introduced hyperparameters $\beta_{\alpha}$ and $\beta_{X}$ to scale the L1 norms of $\mathbf{\alpha}$ and $\mathbf{X}$, respectively. The ratio of these hyperparameters controls the relative weights of the prior and data, while the sum of the hyperparameters controls the shape of the posterior distribution, as higher values of $\beta_{\alpha} + \beta_{X}$ produce sharper distributions that have less variance around the mean. We then performed a two-dimensional grid search over these hyperparameters to identify the optimal parameter values. The details of this grid search are presented below:

* We split the time period for which we have polls (March through November) into intervals of six days. For each of these intervals, the goal was to predict the polling numbers five days in advance using the polling numbers on the first day ($t_1$) and Twitter data over the course of the next five days ($t_2$ through $t_6$). 
* Because our ground truth polling estimates were formed using all available polling data, it wasn't appropriate to use our polling estimate on $t_1$ to form our prior since this estimate was influenced by future polls that had not yet been conducted. Therefore, for each day, we applied the same methodology to estimate the ground truth polling data using all polls that had been conducted up until the given day. 
* For each of the intervals, we set the $\mathbf{\alpha}$ vector associated with the prior Dirichlet distribution to $\frac{\beta_{\alpha}}{\sum_{i=1}^{5}S_{t_1,i}}[S_{t_1,1}, ..., S_{t_1,5}]$, where $S_{t_1,i}$ represents the estimated support of candidate $i$ on day $t_1$ according to the polls. This ensured that the L1 norm of $\mathbf{\alpha}$ summed to $\beta_{\alpha}$ and that the elements of $\alpha$ were proportional to the support of the respective candidates. Meanwhile, the data vector $\mathbf{X}$ was simply scaled by $\beta_{X}$.
* The ground truth polling vector on $t_6$ ($\mathbf{S}_{t_6}$) was normalized so that the popularity of the candidates summed to one. 
* The likelihood of the normalized $\mathbf{S}_{t_6}$ vector was calculated under the posterior distribution $\mathbf{\theta}|X, \beta_{\alpha}, \beta_{X}$ for each of the intervals, and the average likelihood across all intervals was recorded.
* The model with the values of $\beta_{\alpha}$ and $\beta_{X}$ that maximized the average likelihood computed above was considered to be the best model to predict future polling numbers.

The grid search described above revealed that the optimal values of $\beta_{\alpha}$ and $\beta_{X}$ were 110,000 and 0.003, respectively. Given that the average L1 norm of $\mathbf{X}$ was roughly 23,000, this meant that the fraction of weight that was placed on the Twitter data was practically zero ($\frac{23000 * 0.003}{23000 * 0.003 + 1100000} \approx 0$). In other words, given the latest available polls and the Twitter data, the model entirely ignored the Twitter data and exclusively used the latest polls to predict the future polling numbers. Overall, this analysis indicated that the number of positive Tweets about each candidate is totally unrelated to the candidate’s true support. 

The notebook that performs this grid search can be found [here](https://github.com/benlevyx/twitter-polling/blob/master/notebooks/dirichlet%20model/dirichlet_model_grid_search.ipynb).

All the analysis performed thus far provided conclusive evidence that tweets cannot be used to gain insight into candidates' popularity. As such, there was no need to develop any other models, as we were confident that even the most sophisticated model wouldn't be able to extract any useful signal from the tweets. That being said, there were still several flaws with this Bayesian model that ideally would have been addressed. 

In this model, our formulation of the data-generating process in which supporters of a given candidate independently decide whether to post a tweet in favor that candidate was overly simplistic. Part of the allure of this view of the data-generating process was that it made it natural to model the data using a multinomial distribution and thus allowed us to take advantage of the computational simplicity and model interpretability associated with Dirichlet-multinomial conjugacy. 

However, just because this model was convenient to use doesn't mean it was the most appropriate choice. Not only did it disregard all negative tweets, which make up half of all tweets, but it also made the unrealistic assumption that each positive tweet can be interpreted as a vote for the candidate, when in reality, the tweets at best offer a rough sense of how the candidates and their policies are perceived by the public. 

Additionally, this model failed to account for the fact that the popularity of certain candidates are tightly related. For example, Elizabeth Warren and Bernie Sanders are the two most progressive candidates in the field, which means that are both trying to win over the most progressive wing of the Democratic party. This means that increasing support for Warren should theoretically come at the expense of Bernie Sanders’s support and vice versa. Meanwhile, Joe Biden is generally seen as a safe, moderate, well-known candidate, which means that he tends to be the default choice for voters who aren’t particularly passionate about any of the other candidates. This means that lack of positive sentiment about other candidates theoretically bodes well for Biden.

Listed below are some of the features of a more advanced Bayesian model that addresses these deficiencies of our model (this model would still use the same Dirichlet prior distribution on the polling numbers):

* A correlation matrix ($\mathbf{\Sigma}$) that measures the strength and direction of the correlation of the popularity of the various candidates. This correlation matrix would be specified by a combination of the empirical correlation matrix formed by the ground truth polling data and domain knowledge about how the ideologies and personalities of the candidates relate to each other. 

* An overall sentiment score for each candidate $\mathbf{S} = [S_1, ..., S_5]$ that is formed by weighing each tweet (both positive and negative) by the distance of the sentiment score from a neutral score of 0.5. (One way to mitigate the risk of falsely interpreting negative tweets from Republicans as negative sentiment among Democrats would be to look up the Twitter handles associated with common conservative news outlet and ignore tweets from users who follow these particuar accounts.)

* A generative model that explains how the observed sentiment scores are generated from the true popularity of each candidate and the interdependencies between the candidates' popularity (i.e. $p(\mathbf{S}|\mathbf{\theta}, \mathbf{\Sigma})$). One option would be to use a multivariate normal distribution, $\mathbf{S} \sim MVN(f(\mathbf{\theta}), \frac{\mathbf{\Sigma}}{\kappa})$ where $f$ represents an affine transformation, and $\kappa$ represents a scaling factor. These operations would likely be needed to account for the fact that $\mathbf{S}$ and $\mathbf{\theta}$ are on different scales (e.g. an increase in sentiment score of 0.01 doesn't correspond to an increase in popularity of 0.01). 

At this point, the posterior distribution of $\mathbf{\theta}$ can be specified: $p(\mathbf{\theta}|\mathbf{S},\mathbf{\Sigma}) \propto p(\mathbf{S}|\mathbf{\theta}, \mathbf{\Sigma}) \ p(\mathbf{\theta})$, where $\mathbf{\theta} \sim Dir(\mathbf{\alpha})$. This posterior distribution can be approximated by numerical methods such as Markov chain Monte Carlo.

## Conclusion and possible improvements 

### Discussion

By looking at the plots of the ground-truth popularity of each candidate versus his/her implied popularity obtained based on the count of positive sentiment tweet counts as well as the prior polls, it is evident that the posterior support of each candidate is not correlated with the ground truth polls. This can be attributed to a range of factors.

#### Demographic bias 

First, the sample of people tweeting about politics on Twitter is likely not a representative sample of the entire electorate voting in the Democratic primaries. This is referred to as demographic bias. Specifically, not every age, gender and social group is represented in Twitter at a proportion that is representative of the entire population.

Moreover, the Twitter sample is geographically biased. Unfortunately, there is no simple way to ensure that tweets are sampled from users located in different region of the U.S. to ensure that different parts of the country are fairly represented in these Twitter-based polls.

#### Self-selection bias 

The group of people who actively tweet on Twitter about politics is a biased sample that doesn't necessarily reflect the sample of people participating in the polling surveys. 

Those people who publicly display their feelings about candidates are generally politically active. As a result, people who are moderate or not politically active to the same extent are not equally represented, let alone people who do not share their political preferences publicly at all.

These points are corroborated by the fact that the support predicted for Biden based in part on Twitter data is consistently lower than the support estimated by the ground truth polls. Meanwhile, the support for Harris and Buttigieg according to these predictions is consistently higher than what the polls estimate. This may be the case since Biden is an old-school candidate while Harris and Buttigieg are relatively hip candidates with more notable online presences. This may explain why Harris and Buttigieg attract higher attention on social media than Biden relative to their true popularity.

#### Sentiment as vote

A strong assumption of the Bayesian model is that each positive-sentiment tweet is considered to be a vote for the corresponding candidate. However, the fact that a user posts a positive comment for a candidate does not necessarily mean that he/she would vote for this specific candidate. Furthermore, using this approach, it is not easy to identify whether specific users have posted positive tweets about multiple candidates. Finally, a considerable number of political tweets are characterized by sarcasm, which is difficult for sentiment analysis models to detect, and which may therefore be erroneously classified as positive sentiment. These flaws in our models may explain why the posterior support based on positive sentiment tweet counts is not aligned with the support estimated by the polls.

#### Bias in the collection of data

- twint sampling (black box not sure if it is representative sample of the whole Twitter)
- twitter bots (what if multiple accounts write positive stuff multiple times)
- how could we improve this?



## Final Conclusion

- state clear conclusion: it seems that twitter cannot be used as polling tool - too many biases 



- what could we improve (do more things based on user-level data )
- debias for bots/republican 
- take into account the negative tweets




