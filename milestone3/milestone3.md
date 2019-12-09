# Milestone 3
*Group 53 (Matthieu Meeus, Will Fried, Dimitris Vamvourellis, Benjamin Levy)*
*Wed. Nov. 20, 2019*

**Topic: Tweets**

## Revised project statement

Given a time series of real-world polling data of the 2020 Democratic Primary and tweets made about those candidates from March 1st to the current date, our goal is to predict the current public opinion on each Democratic candidate at the current moment before professional polls are conducted and made public. Our idea is to augment the information carried by past polls with current sentiment observed in Twitter about each candidate to infer his/her current true popularity.

## Methodology to date

1. Sentiment model: https://docs.google.com/document/d/1t1lzGS47m2dkHZYUaUgjeVdjpFT6EPPReF_Q_wzB9n8/edit?usp=sharing
2. Ground truth public opinion estimation: https://drive.google.com/file/d/1C_9MbMnzezB4N6DafLBKntfyLDDRuuhH/view?usp=sharing
    
    Notebook: https://github.com/benlevyx/twitter-polling/blob/master/notebooks/ground_truth_polling.ipynb

## Data Collection

Our project requires much more than just the tweets of one individual Twitter user. Instead, we need *all* tweets that mention any of the Democratic candidates for an expansive time period (from March until now). As a result, using the Twitter API was not an option, as they have stringent restrictions on the collection of all data (especially data more than 7 days old). Instead, we used `twint` (https://github.com/twintproject/twint), an open source Python package that gives unlimited access to all tweets, users, and conversations on Twitter.

We created an EC2 instance on Amazon AWS and linked it to an RDS database, allowing for uninterrupted collection of the tweets. We used the following search terms: https://docs.google.com/document/d/1KpRcha1BqeC2U3ziiviK40nse5DVMygkYzimIYBharc/edit?usp=sharing. After downloading tweets for about a week, we had roughly 2 million unique tweets to work with.

## EDA

We have seven candidates in total: Biden, Sanders, Warren, Buttigieg, Harris, Booker, O'Rourke. Due to the size of the dataset (over 2 million tweets total), we first wanted to look at a subset of the most popular candidates to detect issues with the Twitter data itself. Below, we have visualized the popularity of each candidate (calculated using the methodology defined in the Ground truth public opinion estimation document) against a number of features obtained from tweets related to each candidate. For three candidates (Biden, Sanders and Warren), we plot the daily average sentiment and daily number of tweets over time together with the popularity of the candidate over time. The sentiment is taken as a weighted average by likes on all tweets mentioning the candidate during a particular day. A score of 0 corresponds to a negative sentiment, 1 to a positive. Note that the number of tweets per day is divided by the max number of tweets that has happened during the entire timeframe considered. This has been done for visualization purposes only.

![](https://i.imgur.com/tNv41gD.png =300x220)
![](https://i.imgur.com/YNWO0uk.png =300x220)

![](https://i.imgur.com/MHUbWjy.png =300x220)
![](https://i.imgur.com/Y0Va2Gi.png =300x220)

![](https://i.imgur.com/TU7ROrH.png =300x220)
![](https://i.imgur.com/2LwqZCp.png =300x220)


A number of problems are evident. First, All three candidates show sizable gaps in their tweet count (Sanders has a gap after August; the x-axis is truncated for his tweets). This is due to the Twint scraper itself: at certain points, Twitter would block the scraper for a period of time, meaning that even after retrying up to 10 times to download tweets, the scraper failed to get more than a small number of tweets. As a result, it is essential to re-run the scraper for these time periods to ensure uniform coverage over the year.

Second, there are evidently peaks and troughs in the number of tweets and like-weighted sentiment daily averages for each candidate. Looking at Warren's time series and setting aside the period where there were almost no tweets, there are small spikes visible on the right half of the bottom-right graph. These also seem to precede increases in her ground truth polling popularity (especiall the second spike). Looking at Sanders, there is also a characteristic drop in like-weighted average sentiment  that precedes a small slump in the polls in the first half of the time period.

Finally, sentiment is evidently quite noisy and exhibits high temporal correlation (the sentiment on day $d$ depends on the sentiment on day $d-1$ and potentially even $d-2, d-3, ...$). Thus, it might make sense to look not just at sentiment on a given day, but also change in sentiment from the previous day.

## Baseline

*Notebook*: https://github.com/benlevyx/twitter-polling/blob/master/notebooks/baseline_model.ipynb

Before getting to the baseline model for our primary outcome (predicting today's public opinion of each candidate), we would also count among our "baseline model" the models that were developed to both estimate the sentiment of each tweets (using an RNN) and to generate ground truth (using a non-parametric method). For both of these models, please refer to the methodology documents above.

For baseline models we tried the following data/feature configurations

* Interaction between total count of tweets per day and average daily sentiment for each candidate
* Presence or absence of the lag terms from the ground truth opinion time series (e.g. for day $d$, the difference between day $d-1$ and $d-2$)
* Predicting public opinion for day $d$, $d+5$, or $d+10$

And the following models

* Linear regression
* Ridge regression (CV)
* LASSO (CV)
* Random forest regression (100 trees, max depth 3)
* AdaBoost (50 trees, max_depth 1)

The following table shows $R^2$ scores for each combination of these models and data specifications:

![](https://i.imgur.com/vbPVO1T.png)

Clearly, the model performs much more poorly when it has to predict even 10 days in advance. This indicates a potential space for improvement: predicting public opinion several days (even weeks) in advance. Political polls are notoriously poor at this (it's not unlike predicting the weather), meaning that if we can take advantage of the information in the Twitter data, we might be able to improve upon naive forecasting or ML methods.

## Future Steps

The true popularity of each candidate is a latent variable which we want to estimate. However, we only have noisy observations of the truth given by the averaged daily polls as well as the aggregated daily Twitter sentiment which is also noisy. 

We will try to fit a Hidden Markov Model which will generate the posterior distribution of the unobserved true popularity of a candidate given noisy observations of polls and Twitter sentiment. We will first try to approximate the true popularity using a Kalman Filter which assumes that the dynamics are linear. 

Using the Kalman filter we can infer the true popularity of a candidate by taking both the past observations of polls and the sentiment into account, thus producing a smoother version of ground truth. Also, the Kalman filter can be used to predict the popularity of the candidate at the next time step before observing new polls or sentiments.
