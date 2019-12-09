"""
utils.py

General-purpose utility functions.
"""
from datetime import datetime, timedelta
import logging
import sys

from twitpol import config


def get_api_keys():
    with config.API_KEY_FILE.open('r') as f:
        data = f.readlines()
    keys = {}
    for line in data:
        k, v = line.split(' -- ')
        keys[k] = v
    return keys


def date_range(d1, d2=datetime.today(), step=1, fmt="%Y-%m-%d"):
    """Create a range of dates from d1 to d2 by intervals of `day-step`.

    :param d1: str, start date, formatted according to fmt
    :param d2: str, end date, formatted according to fmt (default today)
    :param day_step: int, number of days between each day in the list (default 1 day)
    :param fmt: strftime format string to convert to and frome dates

    :yields: tuple of (int, int) denoting start and end date of each interval
    """
    date1 = datetime.strptime(d1, fmt)
    if isinstance(d2, str):
        date2 = datetime.strptime(d2, fmt)
    else:
        date2 = d2.date()
    day_step = timedelta(days=step)

    curr_date1 = date1
    while curr_date1 < date2:
        curr_date2 = curr_date1 + day_step
        curr_date_str1 = curr_date1.strftime(fmt)
        curr_date_str2 = curr_date2.strftime(fmt)
        curr_date1 = curr_date2

        yield curr_date_str1, curr_date_str2


def format_handler(handler):
    formatter = logging.Formatter(fmt=config.LOG_FORMAT_STR)
    handler.setFormatter(formatter)
    return handler


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    return format_handler(console_handler)


def get_file_handler():
    file_handler = logging.FileHandler(config.LOG_FILE)
    return format_handler(file_handler)


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    logger.propagate = False
    return logger


def get_queries():
    with (config.DATA / 'queries' / 'twitter_search_queries.txt').open() as f:
        queries = []
        for line in f:
            queries.append(line.split(': '))
    return queries
