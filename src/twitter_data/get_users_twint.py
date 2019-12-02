from asyncio import TimeoutError as async_TimeoutError
import multiprocessing as mp
import os

import twint
from aiohttp.client_exceptions import ClientError
import pandas as pd
import numpy as np
import backoff

from twitpol import utils, db, timeout, twitter
from twitpol.exceptions import TweetError, InsufficientTweetsError


my_logger = utils.get_logger('my_logger')
engine = db.get_db_engine()
chunk_size = 10


def get_users_chunk(i, chunk_size, engine):
    ids = pd.read_sql(f"SELECT id, username FROM users LIMIT {i * chunk_size}, {chunk_size};", con=engine)
    return ids


def _possibly_empty(df):
    if len(df) == 0:
        raise TweetError("None found")
    else:
        return df.iloc[0, 0]


@backoff.on_exception(backoff.expo,
                      (TweetError, TimeoutError),
                      max_tries=10)
def find_followers(c):
    with timeout.timeout(seconds=500):
        twint.run.Followers(c)
        followers = twint.storage.panda.Follow_df
        return _possibly_empty(followers)


@backoff.on_exception(backoff.expo,
                      (TweetError, TimeoutError),
                      max_tries=10)
def find_following(c):
    with timeout.timeout(seconds=500):
        twint.run.Following(c)
        following = twint.storage.panda.Follow_df
        return _possibly_empty(following)


def run_search(username):
    c = twitter.make_config(hide_output=False)
    c.Username = username
    followers, following = [], []
    try:
        followers = find_followers(c)
        following = find_following(c)
        msg = f'{username}:{len(followers)} followers - {len(following)} following'
        my_logger.info(msg)
        if len(following) == 0:
            raise InsufficientTweetsError("No following found")
    except (TimeoutError, ClientError, TweetError, async_TimeoutError, IndexError) as e:
        msg = f'{username}:{e}'
        my_logger.error(msg)
        raise TweetError("Error")
    return followers, following


def worker(i):
    users_chunk = get_users_chunk(i, chunk_size, engine)
    user_info = []
    for idx, row in users_chunk.iterrows():
        print(row)
        user_id, username = row
        try:
            followers, following = run_search(username)
            user_info.append((user_id, username, followers, following))
        except TweetError as e:
            my_logger.error(f"{username}:{e}")
    df = pd.DataFrame(user_info, columns=['user_id', 'username', 'followers', 'following'])
    str_cols = ['username', 'followers', 'following']
    df[str_cols] = df[str_cols].astype(str)
    print(df.shape)
    df.to_sql('user_profiles', con=engine, if_exists='append')

    msg = f'Process {os.getpid()}:Saved {len(df)} accounts'
    my_logger.info(msg)


def main():
    total_users = pd.read_sql('SELECT COUNT(*) as n FROM users;', con=engine).iloc[0, 0]
    my_logger.info(f"Total users: {total_users}")

    chunk_idxs = list(range(int(np.ceil(total_users / chunk_size))))
    # with mp.Pool(mp.cpu_count()) as pool:
    #     pool.map(worker, chunk_idxs)
    for idx in chunk_idxs:
        worker(idx)


if __name__ == '__main__':
    main()
