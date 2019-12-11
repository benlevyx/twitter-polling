---
layout: page
title: Conclusions and Possible Improvements
---

## Discussion

### Possible Issues with Twitter Data

By looking at the plots of the ground-truth popularity of each candidate versus his/her implied popularity obtained based on the count of positive sentiment tweet counts as well as the prior polls, it is evident that the posterior support of each candidate is not correlated with the ground truth polls. This can be attributed to a range of factors:

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

`twint`

Although `twint` gave us several advantages over the traditional Twitter API in terms of no historical or overall volume limits, the package may have introduced its own issues into the integrity of data collection. We noticed that the `twint` scraper was prone to missing entire days or even weeks at a time, and we subsequently needed to re-run the scraper to fill these gaps. It is entirely possible that `twint` failed to collect significant amounts of tweets for certain days or candidates. Unfortunately, there was no way to check whether there was any trend in collection failures for different candidates, meaning that the tweet counts may have been lower than they should have been for particular candidates. Our hope was that by smoothing out the counts of positive tweets over several days, we would have decreased the probability that any particular candidate would have had artificially lower tweet counts than other candidates for the entirety of the moving average window.

*Bots*

Twitter is notorious for having large numbers of bots (fake accounts), since it is so cheap to create an account and run it anonymously through an automated script. Pew Research found that [the majority of political news stories shared on Twitter come from bots](https://www.pewresearch.org/fact-tank/2018/04/09/5-things-to-know-about-bots-on-twitter/). Since we were interested in what *actual people* think of politicians, this was a significant concern. The design of a bot detection algorithm was outside the scope of this project (indeed, such an algorithm could have comprised its own project entirely), but in future efforts to estimate political sentiment in the real world from tweets, filtering for bots should be a key step in data cleaning.

### Model Improvements

All the analysis performed in the project offered strong evidence that tweets cannot be used to gain insight into candidates' popularity. As such, there was no need to develop any other models, as we were confident that even the most sophisticated model wouldn't be able to extract any useful signal from the tweets. That being said, there were still several flaws with our Bayesian model that ideally would have been addressed. 

In this model, our formulation of the data-generating process in which supporters of a given candidate independently decide whether to post a tweet in favor that candidate was overly simplistic. Part of the allure of this view of the data-generating process was that it made it natural to model the data using a multinomial distribution and thus allowed us to take advantage of the computational simplicity and model interpretability associated with Dirichlet-multinomial conjugacy. 

However, just because this model was convenient to use doesn't mean it was the most appropriate choice. Not only did it disregard all negative tweets, which make up half of all tweets, but it also made the unrealistic assumption that each positive tweet can be interpreted as a vote for the candidate, when in reality, the tweets at best offer a rough sense of how the candidates and their policies are perceived by the public. 

Additionally, this model failed to account for the fact that the popularity of certain candidates are tightly related. For example, Elizabeth Warren and Bernie Sanders are the two most progressive candidates in the field, which means that are both trying to win over the most progressive wing of the Democratic party. This means that increasing support for Warren should theoretically come at the expense of Bernie Sanders’s support and vice versa. Meanwhile, Joe Biden is generally seen as a safe, moderate, well-known candidate, which means that he tends to be the default choice for voters who aren’t particularly passionate about any of the other candidates. This means that lack of positive sentiment about other candidates theoretically bodes well for Biden.

Listed below are features we could add to our Bayesian model that could potentially address some of these deficiencies: 

A correlation matrix ($$\mathbf{\Sigma}$$) that measures the strength and direction of the correlation of the popularity of the various candidates. This correlation matrix would be specified by a combination of the empirical correlation matrix formed by the ground truth polling data and domain knowledge about how the ideologies and personalities of the candidates relate to each other. 

An overall sentiment score for each candidate $$\mathbf{S} = [S_1, ..., S_5]$$ that is formed by weighing each tweet (both positive and negative) by the distance of the sentiment score from a neutral score of 0.5. (One way to mitigate the risk of falsely interpreting negative tweets from Republicans as negative sentiment among Democrats would be to look up the Twitter handles associated with common conservative news outlet and ignore tweets from users who follow these particuar accounts.)

A generative model that explains how the observed sentiment scores are generated from the true popularity of each candidate and the interdependencies between the candidates' popularity (i.e. $$p(\mathbf{S} \mid \mathbf{\theta}, \mathbf{\Sigma})$$). One option would be to use a multivariate normal distribution, $$\mathbf{S} \sim N(f(\mathbf{\theta}), \frac{\mathbf{\Sigma}}{\kappa})$$ where $$f$$ represents an affine transformation, and $$\kappa$$ represents a scaling factor. These operations would likely be needed to account for the fact that $$\mathbf{S}$$ and $$\mathbf{\theta}$$ are on different scales (e.g. an increase in sentiment score of 0.01 doesn't correspond to an increase in popularity of 0.01). 

At this point, the posterior distribution of $$\mathbf{\theta}$$ can be specified: $$p(\mathbf{\theta} \mid \mathbf{S},\mathbf{\Sigma}) \propto p(\mathbf{S} \mid \mathbf{\theta}, \mathbf{\Sigma}) \ p(\mathbf{\theta})$$, where $$\mathbf{\theta} \sim Dir(\mathbf{\alpha})$$. This posterior distribution can be approximated by numerical methods such as Markov chain Monte Carlo.

## Main Takeaway

The key assumption motivating this project is that the subset of Democratic primary voters who are active on Twitter constitutes a representative sample of the overall Democratic electorate. This assumption is critical because it means that political tweets can be used to gain insight into the views of the broader population of Democratic primary voters. However, the fact that there is no discernable relationship between the views of the subpopulation of Twitter users (as measured by Tweet sentiment) and the views of the population as a whole (as measured by polling numbers) calls into question the validity of this assumption. 

means that If this were the case, it would be reasonable to perform the classic statistical inference task of using a 


- state clear conclusion: it seems that twitter cannot be used as polling tool - too many biases 

- what could we improve (do more things based on user-level data )
- debias for bots/republican 
- take into account the negative tweets


