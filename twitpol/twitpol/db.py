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
