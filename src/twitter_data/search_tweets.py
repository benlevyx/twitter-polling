"""
search_tweets.py

Using search-twitter-python to acquire tweets from Twitter's Full Archive search API
[sandbox mode]
"""
import os

import searchtweets as st

from twitpol import config, utils


# Loading API keys
api_keys = utils.get_api_keys

# Creating sandbox search args
# search_args = {
#     'endpoint': 'https://api.twitter.com/1.1/tweets/search/fullarchivev/dev.json',

# }
search_args = st.load_credentials(filename='not_a_file.yml', yaml_key='not_a_key')
print(search_args)
# Setting environment variables
os.environ['SEARCHTWEETS_CONSUMER_KEY'] = api_keys['API_KEY']
os.environ['SEARCHTWEETS_CONSUMER_SECRET'] = api_keys['API_KEY_SECRET']
os.environ['SEARCHTWEETS_ENDPOINT'] = ''

# Test query
query = 'Bernie Sanders'

# Generating query rule (5 to test)
MAX_RESULTS = 5
rule = st.gen_rule_payload(query, results_per_call=MAX_RESULTS)

# Collecting tweets
collected_tweets = st.collect_results(rule,
                                      max_results=MAX_RESULTS,
                                      result_stream_args=search_args)
