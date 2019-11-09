"""
utils.py

General-purpose utility functions.
"""
from datetime import datetime, timedelta

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

        yield curr_date_str1, curr_date_str2

        curr_date1 = curr_date2
