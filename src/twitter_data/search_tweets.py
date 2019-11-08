"""
search_tweets.py

Using search-twitter-python to acquire tweets from Twitter's Full Archive search API
[sandbox mode]
"""
import os
import json

import searchtweets as st

from twitpol import config, utils


# Twitter credentials file
credentials_file = config.TWITTER_CREDENTIALS_FILE

# # Creating sandbox search args
# search_args = {
#     'endpoint': 'https://api.twitter.com/1.1/tweets/search/fullarchivev/dev.json',
#     'consumer_key': api_keys['API_KEY'],
#     'consumer_secret': api_keys['API_KEY_SECRET']
# }
# # Setting environment variables
# os.environ['SEARCHTWEETS_CONSUMER_KEY'] = api_keys['API_KEY']
# os.environ['SEARCHTWEETS_CONSUMER_SECRET'] = api_keys['API_KEY_SECRET']
# os.environ['SEARCHTWEETS_ENDPOINT'] = ''

search_args = st.load_credentials(filename=credentials_file,
                                  yaml_key='search_tweets_api',
                                  env_overwrite=False)
print(search_args)
# Test query
query = 'Bernie Sanders'

# Generating query rule (5 to test)
MAX_RESULTS = 10
rule = st.gen_rule_payload(query,
                           results_per_call=MAX_RESULTS,
                           from_date="2019-04-01",
                           to_date="2019-04-30")

# Collecting tweets
collected_tweets = st.collect_results(rule,
                                      max_results=MAX_RESULTS,
                                      result_stream_args=search_args)

print(type(collected_tweets[0]))
print(len(collected_tweets))

# with open(config.DATA / 'test_tweets.json') as fout:
[print(tweet.all_text, tweet.created_at) for tweet in collected_tweets]
