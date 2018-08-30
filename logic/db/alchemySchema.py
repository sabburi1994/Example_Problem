from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence, Column, Integer, String, Boolean,DATETIME, JSON

class BotActionLog(Base):
     __tablename__ = 'inputBot_botactionlog'

     id = Column(Integer, primary_key=True)
     insta_data_id = Column(String)
     hashtag = Column(String)
     link = Column(String)
     follow_username = Column(String)
     liked = Column(Boolean)
     commented = Column(Boolean)
     followed = Column(Boolean)
     log_time = Column(String)
