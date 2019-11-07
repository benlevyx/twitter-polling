"""
utils.py

General-purpose utility functions.
"""
import config


def get_api_keys():
    with config.API_KEY_FILE.open('r') as f:
        data = f.readlines()
    keys = {}
    for line in data:
        k, v = line.split(' -- ')
        keys[k] = v
    return keys
