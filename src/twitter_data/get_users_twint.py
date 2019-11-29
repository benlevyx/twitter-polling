import time
import random
from asyncio import TimeoutError as async_TimeoutError

import twint
from aiohttp.client_exceptions import ClientError
import pandas as pd
import numpy as np
import backoff

from twitpol import config, utils, db, timeout, twitter
from twitpol.exceptions import TweetError, InsufficientTweetsError


my_logger = utils.get_logger('my_logger')


def get_users_chunk(i, chunk_size, engine):
    ids = pd.read_sql(f"SELECT id, username FROM users LIMIT {i * chunk_size}, {chunk_size};", con=engine)
    return ids


def _possibly_empty(df):
    if len(df) == 0:
        return []
    else:
        return df.iloc[0, 0]


def find_followers(c):
    with timeout.timeout(seconds=500):
        twint.run.Followers(c)
        followers = twint.storage.panda.Follow_df
        return _possibly_empty(followers)


def find_following(c):
    with timeout.timeout(seconds=500):
        twint.run.Following(c)
        following = twint.storage.panda.Follow_df
        return _possibly_empty(following)


@backoff.on_exception(backoff.expo,
                      TweetError,
                      max_tries=15)
def run_search(username):
    c = twitter.make_config(hide_output=False)
    c.Username = username
    try:
        followers = find_followers(c)
        following = find_following(c)
        msg = f'{username}:{len(followers)} followers - {len(following)} following'
        my_logger.info(msg)
    except (TimeoutError, ClientError, TweetError, async_TimeoutError, IndexError) as e:
        msg = f'{username}:{e}'
        my_logger.error(msg)
        raise TweetError("Error")
    if len(following) == 0:
        raise InsufficientTweetsError()
    return followers, following


def main():
    engine = db.get_db_engine()
    chunk_size = 1000
    total_users = pd.read_sql('SELECT COUNT(*) as n FROM users;', con=engine).iloc[0, 0]
    my_logger.info(f"Total users: {total_users}")

    for i in range(int(np.ceil(total_users / chunk_size))):
        users_chunk = get_users_chunk(i, chunk_size, engine)
        user_info = []
        for idx, row in users_chunk.iterrows():
            print(row)
            user_id, username = row
            followers, following = run_search(username)
            user_info.append((user_id, username, followers, following))
        df = pd.DataFrame(user_info, columns=['user_id', 'username', 'followers', 'following'])
        df.to_sql('user_profiles', con=engine, if_exists='append')

        msg = f'Saved {len(df)} accounts'
        my_logger.info(msg)


if __name__ == '__main__':
    main()
