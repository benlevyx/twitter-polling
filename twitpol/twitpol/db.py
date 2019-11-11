from sqlalchemy import create_engine
import pandas as pd

from twitpol import config, utils


def get_db_engine(include_database=True, create_database=False):
    db_str = f'mysql+pymysql://{config.DB_SETTINGS["user"]}:{config.DB_SETTINGS["password"]}@{config.DB_SETTINGS["host"]}:{config.DB_SETTINGS["port"]}/'
    if create_database:
        engine = create_engine(db_str)
        engine.execute(f'CREATE DATABASE IF NOT EXISTS {config.DB_SETTINGS["database"]};')
    if include_database:
        db_str += config.DB_SETTINGS["database"]
    engine = create_engine(db_str)
    return engine


def write_df_to_db(df, engine=None):
    if engine is None:
        engine = get_db_engine()
    try:
        df.to_sql(config.DB_SETTINGS["tweets_table"], con=engine, if_exists='append')
    except TypeError:
        df.applymap(str).to_sql(config.DB_SETTINGS["tweets_table"], con=engine, if_exists='append')


def count_tweets(where=None, engine=None):
    sql_str = f'SELECT COUNT(*) FROM {config.DB_SETTINGS["tweets_table"]}'
    if where is not None:
        sql_str += f' WHERE {where}'
    sql_str += ';'
    if engine is None:
        engine = get_db_engine()
    return pd.read_sql(sql_str, con=engine)


def clear_db_table(tbl=None, engine=None):
    if tbl is None:
        tbl = config.DB_SETTINGS['tweets_table']
    if engine is None:
        engine = get_db_engine()
    engine.execute(f'DELETE FROM {tbl};')
