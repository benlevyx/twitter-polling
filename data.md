---
layout: page
title: Data Collection
---

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
