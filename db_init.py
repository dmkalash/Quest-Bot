import os
from urllib import parse as urlparse

from peewee import PostgresqlDatabase, SqliteDatabase


def db_init():
    if 'HEROKU' in os.environ:
        urlparse.uses_netloc.append('postgres')
        url = urlparse.urlparse(os.environ['DATABASE_URL'])
        DATABASE = {
         'engine': 'peewee.PostgresqlDatabase',
         'name': url.path[1:],
         'user': url.username,
         'password': url.password,
         'host': url.hostname,
         'port': url.port,
        }
        database = PostgresqlDatabase(
            DATABASE.get('name'),
            user=DATABASE.get('user'),
            password=DATABASE.get('password'),
            host=DATABASE.get('host'),
            port=DATABASE.get('port')
        )
        print('Postgres database created')
    else:
        DATABASE = 'quest.db'
        database = SqliteDatabase(DATABASE)
        print('SQLite database created')
    return database


database = db_init()
