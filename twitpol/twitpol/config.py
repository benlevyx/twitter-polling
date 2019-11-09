"""
config.py

Configuration settings for the entire project
"""
from pathlib import Path

# Various folders
ROOT = Path(__file__).parent.parent.parent
DATA = ROOT / 'data'
MODELS = ROOT / 'models'
SRC = ROOT / 'src'

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
start_date = '2019-01-01'
end_date = '2019-11-09'
