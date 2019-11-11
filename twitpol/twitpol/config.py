"""
config.py

Configuration settings for the entire project
"""
import logging
from pathlib import Path
from datetime import datetime

# Various folders
ROOT = Path(__file__).parent.parent.parent
DATA = ROOT / 'data'
MODELS = ROOT / 'models'
SRC = ROOT / 'src'
LOGS = ROOT / 'logs'

API_KEY_FILE = Path('TWITTER_KEYS')
TWITTER_CREDENTIALS_FILE = Path('twitter_credentials.yaml')

# Settings for AWS RDS
DB_SETTINGS = dict(
    host='database-2.czpegg91dqsv.us-east-2.rds.amazonaws.com',
    port=3306,
    user='admin',
    password='dbpass111',
    charset='utf8',
    database='tweets_db',
    tweets_table='tweets'
)

# Settings for crawl of twitter
start_date = '2019-03-01'  # March 1st
end_date = '2019-11-09'    # November 9th (day this was written)

# Logger settings
LOG_FILE = LOGS / f'stream{datetime.now().strftime("%Y.%m.%d.%H%M%S")}.log'
LOG_FORMAT_STR = "%(levelname)s:%(name)s:%(funcName)s:%(lineno)d (%(asctime)s) — %(message)s"
