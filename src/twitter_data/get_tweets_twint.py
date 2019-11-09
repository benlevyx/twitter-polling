import twint

from twitpol import config, utils


def get_db_engine():
    #TODO: Implement this (maybe in another module)
    db_params = config.DB_SETTINGS.copy()
    db_params.pop('database')



def make_config(hide_output=True, get_location=True):
    c = twint.Config()
    c.Pandas = True
    c.Location = get_location
    c.Pandas_clean = True
    c.Hide_output = hide_output


def get_queries():
    pass


def run_search(c):
    twint.run.Search(c)
    return twint.storage.panda.Tweets_df

def write_df_to_db(df):
    df.to_sql(config.DB_SETTINGS.database, con=engine, if_exists='append')


def main():
    c = make_config()
    queries = get_queries()
    for q in queries:
        c.Search = q
        for d1, d2 in utils.date_range('2019-01-01', '2019-11-09', day_step=1):
            c.Since = d1
            c.Until = d2

            df_tweets = run_search(c)



if __name__ == '__main__':
    main()
