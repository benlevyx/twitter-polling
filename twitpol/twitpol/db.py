from sqlalchemy import create_engine

from twitpol import config, utils


def get_db_engine(include_database=True, create_database=True):
    # TODO: Implement this (maybe in another module)
    db_params = config.DB_SETTINGS.copy()
    db_name = db_params.pop('database')
    db_str = f'mysql+pymysql://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}/{db_params["port"]}/'
    if create_database:
        engine = create_engine(db_str)
        engine.cursor().execute(f'CREATE DATABASE IF NOT EXISTS {db_name};')
    if include_database:
        db_str += db_name
    engine = create_engine(db_str)
    return engine
