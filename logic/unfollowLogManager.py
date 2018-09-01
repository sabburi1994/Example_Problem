#import pandas as pd

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
#import os
#from datetime import datetime, timedelta

#added by abburi
import sqlite3
import warnings
import json
from datetime import datetime

warnings.filterwarnings("ignore")

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

#manual functions added by abburi
    def db_connection(self, db_name):
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        return connection, cursor

    def replace_data(self, connection, cursor, value):
        query = "UPDATE inputbot_unfollowlog SET unfollowed = 1 WHERE following_name = ?"
        cursor.execute(query, value)
        connection.commit()

    def insert_data(self, connection, cursor, value):
        query = "INSERT INTO inputbot_unfollowlog (id, following_name, unfollowed, follow_time, insta_data_id) VALUES (?,?,?,?,?)"
        cursor.execute(query, value)
        connection.commit()

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
                            self.insert_data(connection, cursor, value)
                    
        elif len(following_name) > len(array): # if value in db but not in array, changing unfollow to true
                for i in range(len(following_name)):
                    if following_name[i] not in array:
                        value = ("%s"%following_name[i],)
                        self.replace_data(connection, cursor, value)

        else:           # no value to change
                for i in range(len(following_name)):
                    if following_name[i] in array:
                        pass
                    else:
                        value = (ids[-1]+1, array[i], 0, datetime.now().date(), self.insta_data_id)
                        self.insert_data(connection, cursor, value)
                        value = ("%s"%following_name[i],)
                        self.replace_data(connection, cursor, value)
    
    def get_json(self):
        with open("usersFollower.json","r") as json_file:
            json_read_buffer = json.load(json_file)
        return json_read_buffer['users']
    
    def get_date_data(self, cursor, days):
        query = "SELECT following_name, follow_time, unfollowed from inputbot_unfollowlog"
        cursor.execute(query)
        result = cursor.fetchall()
        following_name = []
        followed_time = []
        unfollowed = []
        for x in result:
            following_name.append(x[0])
            followed_time.append(x[1])
            unfollowed.append(x[2])
        userlist = []
        today = datetime.now()
        for i in range(len(following_name)):
            follow_time = datetime.strptime(followed_time[i],"%Y-%m-%d")
            if abs((today - follow_time).days) > days and unfollowed[i] == 0:
                userlist.append(following_name[i])
            else:
                pass
        dict_list = {'following_name':userlist}
        with open("unfollowuserlist.json","w") as json_file:
            json.dump(dict_list, json_file)
        return userlist, len(userlist)
        
# manual functions end by abburi 

    def correctUnfollowLog(self, userArray):
        try:
            connection, cursor = self.db_connection('log-data-main.db')        
            self.data_manipulation(connection, cursor, userArray)
        except Exception as e:
            print(e)
            
    def getDataFromUnfollowLog(self, days, amountUserToUnfollow):
        connection, cursor = self.db_connection('log-data-main.db')        
        try:
            userlist, amountUserToUnfollow = self.get_date_data(cursor, days)
            data_all = [userlist, amountUserToUnfollow]
        except Exception as e:
            print(e)
        return data_all

if __name__ == "__main__":
    fl = UnfollowLogManager('niclasguenther')
    userArray = fl.get_json()
    fl.correctUnfollowLog(userArray)
    fl.getDataFromUnfollowLog(days=2, amountUserToUnfollow=20)
