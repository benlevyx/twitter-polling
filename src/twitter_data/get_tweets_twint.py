import time
import random
from asyncio import TimeoutError as async_TimeoutError

import twint
from aiohttp.client_exceptions import ClientError
import pandas as pd

from twitpol import config, utils, db, timeout, twitter
from twitpol.exceptions import TweetError, InsufficientTweetsError


my_logger = utils.get_logger('my_logger')


def get_queries():
    with (config.DATA / 'queries' / 'twitter_search_queries.txt').open() as f:
        queries = []
        for line in f:
            queries.append(line.split(': '))
    random.shuffle(queries)
    return queries


def get_date_gaps():
    df_gaps = pd.read_csv(config.DATA / 'queries' / 'date_gaps' / 'harris_buttigieg_date_gaps.csv')
    return df_gaps


def run_search(c, name, engine, d1):
    with timeout.timeout(seconds=300):
        twint.run.Search(c)
        df_tweets = twint.storage.panda.Tweets_df
        if len(df_tweets) == 0:
            raise InsufficientTweetsError("0 tweets downloaded")
        df_tweets['name'] = name
        n_tweets = len(df_tweets)
        db.write_df_to_db(df_tweets, engine)
        # Logging the results
        if n_tweets <= 500:
            raise InsufficientTweetsError(f"{n_tweets} tweets downloaded")
        else:
            msg = f'{name}:{d1}:Downloaded {n_tweets} tweets'
            my_logger.info(msg)


def main():
    c = twitter.make_config()
    queries = get_queries()
    gaps = get_date_gaps()
    engine = db.get_db_engine()
    for query in queries:
        name, q = query
        dates = gaps[gaps['name'] == name]
        if len(dates) == 0:
            continue
        c.Search = q
        for start_date, end_date in zip(dates['start'], dates['end']):
            for d1, d2 in utils.date_range(start_date, end_date, step=1):
                c.Since = d1
                c.Until = d2

                # Running the search
                for i in range(15):
                    try:
                        my_logger.info(f'{name}:{d1}:Attempt {i + 1}')
                        run_search(c, name, engine, d1)
                        break
                    except (TimeoutError, ClientError, TweetError, async_TimeoutError) as e:
                        msg = f'{name}:{d1}:{e}'
                        my_logger.error(msg)
                time.sleep(2)

        n_tweets_total = db.count_tweets(where=f"name = '{name}'")
        my_logger.info(f'TOTAL OF {n_tweets_total} TWEETS DOWNLOADED FOR {name}')


if __name__ == '__main__':
    main()
