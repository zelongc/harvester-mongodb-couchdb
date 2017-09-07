#!/usr/bin/python

# author: Zelong Cong
import argparse
import time

from TwitterAPI.TwitterError import TwitterConnectionError, TwitterRequestError
from TwitterAPI import TwitterRestPager
import connect_mongo
from support import *

ap = argparse.ArgumentParser()
ap.add_argument("-t", "--tokens", required=True, help="The access tokens")
args = vars(ap.parse_args())

token_number = int(args['tokens'])
# create a database Object

db_client = connect_mongo.db_client()

  # save user information in the database:
  # 1. add attributes to the document.
  # 2. customize document '_id'. -> User id

def FileSave(user_info):

    content = {}
    content['_id'] = user_info['id_str']
    content["friends_harvested"] = False
    content["tweets_harvested"] = False
    content["lt_harvest_friends"] = False
    content["lt_harvest_tweets"] = False

    db_client.insert_new_user(content)


def harvest_friends():
    # get a user Id from database
    user_id = db_client.find_user_for_friends()
    api = TwitterAPI(consumer_key=Auth[token_number]['consumer_key'],
                     consumer_secret=Auth[token_number]['consumer_secret'],
                     access_token_key=Auth[token_number]['access_token_key'],
                     access_token_secret=Auth[token_number]['access_token_secret'],
                     auth_type='oAuth1')
    cursor = -1
    # while 1:
    try:
        count=0
        # r = api.request('friends/list', {"user_id": user_id, 'count': 200, 'cursor': cursor})
        r2 = TwitterRestPager(api,'friends/list', {"user_id": user_id, 'count': 200 })
        for each_user_info in r2.get_iterator(40):
            FileSave(each_user_info)

    except TwitterRequestError as e:
        print(e.status_code)
        if e.status_code < 500:
            if e.status_code == 429 or e.status_code == 420:
                print('I am sleeping')
                time.sleep(450)
            elif e.status_code == 401:
                pass
            else:
                raise
            print('TwitterRequestError')
            # something needs to be fixed before re-connecting
            pass
        else:
            print('TwitterRequestError')
            # temporary interruption, re-try request
            pass

    # TwitterConnectionError is thrown when the connection times out or is interrupted.
    # You can always immediately try making the request again.
    except TwitterConnectionError:
        print('disconnected from Twitter Connection Error')
        # temporary interruption, re-try request
        pass
    except Exception as e:
        print(Exception)
        pass

if __name__ == "__main__":
    while 1:
        harvest_friends()
