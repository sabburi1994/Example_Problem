from alchemySchema import BotActionLog
from dbManagerAlchemy import DbManagerAlchemy


def instapy_helper_actionBotLog(insta_data_id,
                                hashtag,
                                link,
                                follow_username,
                                liked,
                                commented,
                                followed):
    dbManager = DbManagerAlchemy()
    if not liked:
        commented = False
        followed = False

    log = BotActionLog(insta_data_id=insta_data_id,
                      hashtag=hashtag,
                      link=link,
                      follow_username=follow_username,
                      liked=liked,
                      commented=commented,
                      followed=followed,
                      log_time='now()')
    dbManager.insertData(log)



def checkValue(value):
    if value == 1:
        return
