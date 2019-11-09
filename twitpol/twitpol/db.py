from sqlalchemy import create_engine

from twitpol import config, utils


def get_db_engine(include_database=True, create_database=True):
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
    df.to_sql(config.DB_SETTINGS["tweets_table"], con=engine, if_exists='append')
    # try:
    #     df.to_sql(config.DB_SETTINGS["database"], con=engine, if_exists='append')
    # except:
    #     df.applymap(str).to_sql(config.DB_SETTINGS["tweets_table"], con=engine, if_exists='append')
