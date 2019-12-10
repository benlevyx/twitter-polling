---
layout: page
title: Introduction and Motivation
cover: true
permalink: /
---

With the Democratic primary elections coming up in 2020, polls that describe and predict the popularity of each candidate get increasing attention. However, since the presidential elections of 2016, the accuracy of these polls has been fundamentally critized. It turns out that generalizing limited, often biased voting samples to an entire nation is a very hard thing to do. Additionally, polls are only able to capture trends in popularity with a certain delay. If candidate X has performed great in a certain debate or a recent scandal about candidate Y was brought to light, the impact on the polls is only seen after at least a couple of days. 

This project will attempt to tackle these two intrinsic flaws of the current polling systems by leveraging Twitter data. Potentially, sentiment expressed in tweets mentioning a certain candidate relates to the popularity of that same candidate. If this would be the case, polls could be updated by following the Twitter sentiment over time. As such, the sample sizes are significantly expanded due to the large amount of tweets posted at every moment and the public opinion about certain events can be captured instantaneously. This website describes the different steps taken to assess the feasibility of the goal described above. Note that this project will only focus on the five most popular candidates for the democratic elections: Joseph Biden, Peter Buttigieg, Kamala Harris, Bernie Sanders and Elizabeth Warren. 

First, a short literature review is discussed. Predicting elections has always been a hot-topic, leading too many different approaches discussed in literature. Understanding what has been done before with according results is a crucial first step before performing any analysis.

Secondly, the best data source will be identified and consecutive collection will be executed. For the tweets, the Twitter API is used to scrape all posts mentioning the five candidates considered from early March until end of October 2019. Additionally, 'ground truth' polling data needs to be collected to assess the correlation with the twitter sentiment. Realizing that this does not exist, the best source for multiple pollster data appeared to be the well-known FiveThirtyEight.com. The actual implementation of collecting the tweets and ground truth polling data will be discussed in the section 'Data Collection'.

Consequently, a sentiment score should be assigned to all selected tweets. A deep neural network has been trained on an online available, labeled dataset to predict a score between 0 and 1 based on the actual words used in the tweet. Here, 0 and 1 correspond to a very negative and very positive sentiment, respectively. The optimal weights are then used to predict the sentiment on the political tweets that are collected.

After all data has been collected and generated, Exploratory Data Analysis (EDA) can be done. Visualizations of both tweet sentiment and ground truth show the general trends in the data.

Next, the association between the twitter sentiment over time and the ground truth can finally be assessed in a statistically rigorous way. Baseline regression, Kalman filter and Bayesian models will be discussed consequently. 

Lastly, the results from the analysis, appropriate conclusions and potential improvements will be discussed.