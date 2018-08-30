import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence, Column, Integer, String
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


USERNAME = 'instabroUser'
PASSWORD = 'Reis23#'
DBNAME = 'instabroDb'
HOSTNAME = 'localhost'
TABLENAME = 'inputBot_unfollowlog'
DB_STRING = 'postgresql+psycopg2://{}:{}@{}/{}'.format(USERNAME, PASSWORD, HOSTNAME, DBNAME)


@contextmanager
def db_session(db_url):
    engine = create_engine(db_url, convert_unicode=True)
    connection = engine.connect()
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))
    yield db_session
    db_session.close()
    connection.close()


import json

class DbManagerAlchemy(object):

    def insertData(self, addScheme):
        with db_session(DB_STRING) as db:
            db.add(addScheme)
            db.commit()

    def getSession(self):
        with db_session(DB_STRING) as db:
            return db
