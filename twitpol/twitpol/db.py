from sqlalchemy import create_engine
from sqlalchemy.types import VARCHAR
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
        df['id'] = df['id'].astype(int)
        _write_df_to_db(df, engine)
    except TypeError:
        try:
            df['id'] = df['id'].astype(int)
            cols_to_str = ['tweet', 'hashtags', 'cashtags', 'user_id_str',
                           'username', 'name', 'link', 'quote_url', 'search',
                           'near', 'geo', 'source', 'user_rt', 'reply_to']
            df[cols_to_str] = df[cols_to_str].astype(str)
            _write_df_to_db(df, engine, dtype={'None': VARCHAR(5)})
        except TypeError:
            df = df.applymap(str)
            _write_df_to_db(df, engine)


def _write_df_to_db(df, engine, **kwargs):
    df.to_sql(config.DB_SETTINGS["tweets_table"], con=engine, if_exists='append', **kwargs)


def count_tweets(where=None, engine=None):
    sql_str = f'SELECT COUNT(*) FROM {config.DB_SETTINGS["tweets_table"]}'
    if where is not None:
        sql_str += f' WHERE {where}'
    sql_str += ';'
    if engine is None:
        engine = get_db_engine()
    return pd.read_sql(sql_str, con=engine)


def clear_db_table(tbl=None, engine=None):
    tbl, engine = _check_tbl_engine(tbl, engine)
    engine.execute(f'DELETE FROM {tbl};')


def drop_duplicate_rows(tbl=None, engine=None):
    tbl, engine = _check_tbl_engine(tbl, engine)
    sql_query = f'''
    DELETE t1 FROM {tbl} t1
    INNER JOIN {tbl} t2
    WHERE
        t1.index < t2.index AND
        t1.id = t2.id;
    '''
    engine.execute(sql_query)


def add_unique_constraint(col, tbl=None, engine=None):
    tbl, engine = _check_tbl_engine(tbl, engine)
    sql_str = f'''
    ALTER TABLE {tbl}
    ADD UNIQUE ({col});
    '''
    engine.execute(sql_str)


def _check_tbl_engine(tbl, engine):
    if tbl is None:
        tbl = config.DB_SETTINGS['tweets_table']
    if engine is None:
        engine = get_db_engine()
    return tbl, engine


def write_dict_to_db(dct, tbl, engine):
    df = pd.DataFrame(dct)
    df.to_sql(tbl, con=engine)
