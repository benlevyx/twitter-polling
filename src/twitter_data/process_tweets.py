"""
process_tweets.py

Preprocessing tweets from raw format into usable relational database format

INPUT: JSON files of tweets
OUTPUT: CSV files of processed data
    - Tweets
    - Users
    - Hashtags/mentions
"""
import tweepy