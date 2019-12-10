---
layout: page
title: Conclusions and Possible Improvements
---

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

