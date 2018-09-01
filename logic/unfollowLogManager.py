import pandas as pd

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os
from datetime import datetime, timedelta

#added by abburi
import sqlite3
import warnings

warnings.filterwarnings("ignore") # to not display pandas incompatibility error which i was getting

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
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        return connection, cursor

    def replace_data(self, connection, cursor, value):
        query = "UPDATE inputbot_unfollowlog SET unfollowed = 1 WHERE following_name = ?"
        print "changing unfollowed = True for %s"%value
        cursor.execute(query, value)
        connection.commit()

    def insert_data(self, connection, cursor, value):
        query = "INSERT INTO inputbot_unfollowlog (id, following_name, unfollowed, follow_time, insta_data_id) VALUES (?,?,?,?,?)"
        cursor.execute(query, value)
        connection.commit()

    #better logic
    def data_manipulation(self, connection, cursor, array):
        query = "SELECT id, following_name from inputbot_unfollowlog"
        cursor.execute(query)
        result = cursor.fetchall()
        ids = []
        following_name = []
        for x in result:
            ids.append(x[0])
            following_name.append(x[1])

        if len(array) > len(following_name): # if value not in db but in array, inserting new data
              for i in range(len(array)):
                    if array[i] not in following_name:
                            value = (ids[-1]+1, array[i], 0, datetime.now().date(), "USER_Temp")
                            print "Inserted Values are: "
                            for x in value:
                                print x
                            self.insert_data(connection, cursor, value)
                    
        elif len(following_name) > len(array): # if value in db but not in array, changing unfollow to true
                for i in range(len(following_name)):
                    if following_name[i] not in array:
                        value = ("%s"%following_name[i],)
                        self.replace_data(connection, cursor, value)

        else:           # no value to change
                pass

    def correctUnfollowLog(self, userArray):
        connection, cursor = self.db_connection('log-data.db')
        self.data_manipulation(connection, cursor, userArray)

    def getDataFromUnfollowLog(self, days=2, amountUserToUnfollow=0):
        try:
            pass
        except Exception as e:
            print(e)
        return data_all

if __name__ == "__main__":
    fl = UnfollowLogManager('niclasguenther')
    fl.correctUnfollowLog(['insta1', 'insta2', 'insta3'])
    #users_list = fl.getDataFromUnfollowLog(days=2, amountUserToUnfollow=20)
