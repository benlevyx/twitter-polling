import traceback

import twint
from aiohttp.client_exceptions import ClientPayloadError, ClientConnectorError

from twitpol import config, utils, db


twint_logger = utils.get_logger('twint_logger')


def make_config(hide_output=True, get_location=False):
    c = twint.Config()
    c.Pandas = True
    c.Location = get_location
    c.Hide_output = hide_output
    return c


def get_queries():
    with (config.DATA / 'queries' / 'twitter_search_queries.txt').open() as f:
        queries = []
        for line in f:
            queries.append(line.split(': '))
    return queries


def main():
    c = make_config()
    queries = get_queries()
    engine = db.get_db_engine()
    for query in queries:
        name, q = query
        c.Search = q

        for d1, d2 in utils.date_range(config.start_date, config.end_date, step=5):
            c.Since = d1
            c.Until = d2

            # Running the search
            try:
                twint.run.Search(c)
                df_tweets = twint.storage.panda.Tweets_df
                df_tweets['name'] = name
                n_tweets = len(df_tweets)
                db.write_df_to_db(df_tweets, engine)
                # Logging the results
                msg = f'{name}:{d1}:Downloaded {n_tweets} tweets'
                if n_tweets == 0:
                    twint_logger.warning(msg)
                else:
                    twint_logger.info(msg)
            except (ClientPayloadError, ClientConnectorError):
                twint_logger.error(traceback.format_exc())

        n_tweets_total = db.count_tweets(where=f"name = '{name}'")
        twint_logger.info(f'TOTAL OF {n_tweets_total} TWEETS DOWNLOADED FOR {name}')


if __name__ == '__main__':
    main()
