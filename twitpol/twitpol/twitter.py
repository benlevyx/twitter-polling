import time
import random
from asyncio import TimeoutError as async_TimeoutError

import twint
from aiohttp.client_exceptions import ClientError
import pandas as pd

from twitpol import config, utils, db, timeout
from twitpol.exceptions import TweetError, InsufficientTweetsError


my_logger = utils.get_logger('my_logger')


def make_config(hide_output=False, get_location=False, get_pandas=True, store_object=False):
    c = twint.Config()
    c.Pandas = get_pandas
    c.Location = get_location
    c.Hide_output = hide_output
    c.store_object = store_object

    return c
