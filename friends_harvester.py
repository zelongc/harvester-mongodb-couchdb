#!/usr/bin/python

#author: Zelong Cong

from TwitterAPI import TwitterAPI
from TwitterAPI import TwitterRestPager
from TwitterAPI.TwitterError import TwitterConnectionError,TwitterRequestError
from support import *
import argparse
import threading
import connect_mongo
import time

lock=threading.Lock()

ap = argparse.ArgumentParser()
ap.add_argument("-t","--tokens",required=True,help="The access tokens")
args = vars(ap.parse_args())


token_number=int(args['tokens'])
#create a database Object

db_client = connect_mongo.db_client()
####### Recreate the function when using the couchDB
def FileSave(user_info):
    lock.acquire(True)
    try:
        content={}
        content['_id']=user_info['id_str']
        content["friends_harvested"] = False
        content["tweets_harvested"] = False
        content["lt_harvest_friends"] = False
        content["lt_harvest_tweets"] = False
        db_client.insert_new_user(content)

    except Exception as e:
        print(e)
    finally:
        lock.release()


def harvest_friends():
    # get a user Id from database
    user_id= db_client.find_user_for_friends()

    api = TwitterAPI(consumer_key=Auth[token_number]['consumer_key'],
                     consumer_secret=Auth[token_number]['consumer_secret'],
                     access_token_key=Auth[token_number]['access_token_key'],
                     access_token_secret=Auth[token_number]['access_token_secret'],
                     auth_type='oAuth1')
    cursor = -1
    # while 1:
    r = api.request('friends/list', {"user_id": user_id, 'count': 200, 'cursor':cursor})

    for each_user_info in r.get_iterator():
        print(each_user_info)
        FileSave(each_user_info)

    time.sleep(15)





if __name__=="__main__":
    while 1:

        harvest_friends()
