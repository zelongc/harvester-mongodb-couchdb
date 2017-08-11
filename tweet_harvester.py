#!/usr/bin/python

# author: Zelong Cong


import argparse
import time

from TwitterAPI.TwitterError import TwitterConnectionError, TwitterRequestError
from TwitterAPI import TwitterRestPager
import connect_mongo
from support import *

# aquire the arguments---Target City
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--tokens", required=True, help="The access tokens")
args = vars(ap.parse_args())

token_number = int(args['tokens'])
# create a database Object

db_client = connect_mongo.db_client()


# save user information in the database:
# 1. add attributes to the document.
# 2. customize document '_id'. -> User id

def FileSaveUser(user_info):
    content = {}
    content['_id'] = user_info['id_str']
    content["friends_harvested"] = False
    content["tweets_harvested"] = False
    content["lt_harvest_friends"] = False
    content["lt_harvest_tweets"] = False

    db_client.insert_new_user(content)


def FileSave(content):
    if content['geo'] or content['coordinates']:
        FileSaveUser(content['user'])
        content['_id'] = content['id_str']
        db_client.insert_new_tweet(content)

def search_user():
    keepdoing = True
    while keepdoing:
        try:
            # get a user ID
            user_id = db_client.find_user_for_tweeets()
            api = TwitterAPI(consumer_key=Auth[token_number]['consumer_key'],
                             consumer_secret=Auth[token_number]['consumer_secret'],
                             access_token_key=Auth[token_number]['access_token_key'],
                             access_token_secret=Auth[token_number]['access_token_secret'],
                             auth_type='oAuth2')

            r = api.request('statuses/user_timeline', {"user_id": user_id, 'count': 200, 'exclude_replies': 'true'})
            # Use the
            r = TwitterRestPager(api, 'statuses/user_timeline', {"user_id": user_id, 'count': 200, 'exclude_replies': 'true'})
            for each in r.get_iterator():
                if 'text' in each:
                    FileSave(each)

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

#  streaming must use oAuth1 mode
def Streaming():
    api = TwitterAPI(consumer_key=Auth[token_number]['consumer_key'],
                     consumer_secret=Auth[token_number]['consumer_secret'],
                     access_token_key=Auth[token_number]['access_token_key'],
                     access_token_secret=Auth[token_number]['access_token_secret'],
                     auth_type='oAuth1')

    while 1:
        for each in city_box.values():
            print('doing streaming')
            try:
                r = api.request('statuses/filter', {'track':'','locations':each})

                print('Begin to get tweets')
                print(r.status_code)
                for item in r.get_iterator():
                    if 'text' in item:
                        print('doing streaming')
                        FileSave(item)

                    elif 'message' in item and item['code'] == 88:
                        print('Streaming API need sleep for 15 minutes!')
                        time.sleep(910)
                        break
                    elif 'disconnect' in item:
                        break

                #TwitterRequestError is thrown whenever the request fails
                # (i.e. when the response status code is not 200). A status
                # code of 500 or higher indicates a server error which is safe
                # to ignore. Any other status code indicates an error with your
                # request which you should fix before re-trying.
            except TwitterRequestError as e:
                if e.status_code < 500:
                    print(e.status_code)
                    print('TwitterRequestError')
                    # something needs to be fixed before re-connecting
                    raise
                else:
                    print('TwitterRequestError')
                    print()
                    # temporary interruption, re-try request
                    pass

            #TwitterConnectionError is thrown when the connection times out or is interrupted.
            # You can always immediately try making the request again.
            except TwitterConnectionError:
                print('disconnected from Twitter Connection Error')
                # temporary interruption, re-try request
                pass
            except Exception:
                print(Exception)
                pass



if __name__ == "__main__":
    search_user()