# Milestone 3
*Group 53 (Matthieu Meeus, Will Fried, Dimitris Vamvourellis, Benjamin Levy)*
*Wed. Nov. 20, 2019*

**Topic: Tweets**

## Revised project statement

Given a time series of real-world polling data of the 2020 Democratic Primary and tweets made about those candidates from March 1st to the current date, our goal is to predict the current public opinion on each Democratic candidate at the current moment before professional polls are conducted and made public.

## Methodology to date

1. Collection of Tweets dataset: www.linkhere.com
2. Sentiment model: https://docs.google.com/document/d/1t1lzGS47m2dkHZYUaUgjeVdjpFT6EPPReF_Q_wzB9n8/edit?usp=sharing
3. Ground truth public opinion estimation: https://drive.google.com/file/d/1C_9MbMnzezB4N6DafLBKntfyLDDRuuhH/view?usp=sharing

## EDA

We have seven candidates total: Biden, Sanders, Warren, Buttigieg, Harris, Booker, O'Rourke. Due to the size of the dataset (over 2 million tweets total), we first wanted to look at a subset of the most popular candidates to detect issues with the Twitter data itself.

![](https://i.imgur.com/tNv41gD.png =300x300)
![](https://i.imgur.com/YNWO0uk.png =300x300)

![](https://i.imgur.com/dj4hlVx.png =300x300)
![](https://i.imgur.com/YoFfRCt.png =300x300)

![](https://i.imgur.com/QKI4o5c.png =300x300)
![](https://i.imgur.com/6CfKp0I.png =300x300)

A number of problems are evident. First, All three candidates are sizable gaps in their tweet count (Sanders has a gap after August; the x-axis is truncated for his tweets). This is due to the Twint scraper itself: at certain points, Twitter would block the scraper for a period of time, meaning that even after retrying up to 10 times to download tweets, the scraper failed to get more than a small number of tweets. As a result, it is essential to re-run the scraper for these time periods to ensure uniform coverage over the year.

Second, there are evidently peaks and troughs in the number of tweets and like-weighted sentiment daily averages for each candidate. Looking at Warren's time series and setting aside the period where there were almost no tweets, there are small spikes visible on the right half of the bottom-right graph. These also seem to precede increases in her ground truth polling popularity (especiall the second spike). Looking at Sanders, there is also a characteristic drop in like-weighted average sentiment  that precedes a small slump in the polls in the first half of the time period.

Finally, sentiment is evidently quite noisy and exhibits high temporal correlation (the sentiment on day $d$ depends on the sentiment on day $d-1$ and potentially even $d-2, d-3, ...$). Thus, it might make sense to look not just at sentiment on a given day, but also change in sentiment from the previous day.

## Baseline

Before getting to the baseline model for our primary outcome (predicting today's public opinion of each candidate), we would also count among our "baseline model" the models that were developed to both estimate the sentiment of each tweets (using an RNN) and to generate ground truth (using a non-parametric method). For both of these models, please refer to the methodology documents above.