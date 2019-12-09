import pandas as pd

from twitpol import config, utils, db


processed_dir = config.PROCESSED

engine = db.get_db_engine()
data = pd.read_sql('SELECT * FROM TWEETS LIMIT 100', con=engine)

# `processed_dir` is not a string, but a POSIXPath object.
# This doesn't change much for our purposes, except it allows you to do path
# concatenation for windows or mac with this neat backslash syntax, rather
# than typing os.path.join(...) every time you want to build a new path. Yay
# platform-independence!
data.to_csv(processed_dir / 'example_data.csv')
