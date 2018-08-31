import pandas as pd

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os
from datetime import datetime, timedelta

#added by abburi
import sqlite3

USERNAME = 'postgres'
PASSWORD = 'pass123'
DBNAME = 'postgres'
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


class UnfollowLogManager(object):

    def __init__(self, insta_data_id):
        self.insta_data_id = insta_data_id

#added by abburi
    def db_connection(self, db_name):
        connection = sqllite3.connect(db_name)
        cursor = connection.cursor()
        return connection, cursor

    def replace_data(self, connection, cursor, value):
        query = "UPDATE inputbot_unfollowlog SET unfollowed = 0 WHERE following_name = ?"
        cursor.execute(query, value)
        connection.commit()

    def insert_data(self, connection, cursor, value):
        query = "INSERT INTO inputbot_unfollowlog (id, following_name, unfollowed, unfollowed_time, follow_time, insta_data_id) VALUES (?,?,?,0,?,?)"
        cursor.execute(query, value)
        connection.commit()

    def get_data(self, connection, cursor, array):
        query = "SELECT id, unfollowed from inputbot_unfollowlog"
        cursor.execute(query)
        result = cursor.fetchall()
        ids = []
        following_name = []
        for x in result:
            ids.append(x[0])
            following_name.append(x[1])
        for i in range(len(array)):
            if array[i] == following_name[i]:
                    self.replace_data(connection, cursor, following_name[i])
            else:
                value = (array[i], following_name[i], 1, 0, datetime.now().date(), "USER%s"%i)
                self.insert_data(connection, cursor, value)
#end by abburi
    def correctUnfollowLog(self, userArray):
        print "Starting this function"
        connecction, cursor = db_connection('log-data.db')
        get_data(connection, cursor, UserArray)

    def getDataFromUnfollowLog(self, days=2, amountUserToUnfollow=0):
        try:
            pass
        except Exception as e:
            print(e)
        return data_all

if __name__ == "__main__":
    fl = UnfollowLogManager('niclasguenther')
    fl.correctUnfollowLog(['insta1', 'insta2', 'insta4'])
    users_list = fl.getDataFromUnfollowLog(days=2, amountUserToUnfollow=20)
