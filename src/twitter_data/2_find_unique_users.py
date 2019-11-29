import pandas as pd

from twitpol import db, config, utils


my_logger = utils.get_logger('my_logger')


def get_users(engine=None):
    if not engine:
        engine = db.get_db_engine()
    all_users = pd.read_sql('SELECT DISTINCT user_id, username FROM tweets;', con=engine)
    my_logger.info(f"Found {len(all_users)} distinct users")
    return all_users


def create_users_table(engine=None, drop=False):
    if not engine:
        engine = db.get_db_engine()
    if drop:
        engine.execute('''DROP TABLE IF EXISTS users;''')
    engine.execute('''
        CREATE TABLE users(
            id INT PRIMARY KEY,
            username VARCHAR(20) UNIQUE,
            followers LONGTEXT,
            following LONGTEXT
        );
        ''')


def main():
    engine = db.get_db_engine()
    df_users = get_users(engine)
    df_users = df_users.rename(columns={"user_id": "id"})
    df_users.to_sql('users', con=engine, if_exists='append', index=False)


if __name__ == '__main__':
    main()