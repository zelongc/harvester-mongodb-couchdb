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


def harvest_friends():
    num=1
    # get a user Id from database
    user_id = "40814404"
    api = TwitterAPI(consumer_key=Auth[token_number]['consumer_key'],
                     consumer_secret=Auth[token_number]['consumer_secret'],
                     access_token_key=Auth[token_number]['access_token_key'],
                     access_token_secret=Auth[token_number]['access_token_secret'],
                     auth_type='oAuth1')
    cursor = -1
    # while 1:
    r2=TwitterRestPager(api,'followers/list', {"user_id": user_id, 'count': 200})
    r = api.request('followers/list', {"user_id": user_id, 'count': 200})

    for each_user_info in r2.get_iterator():
        if 'Australia' in each_user_info['location']:
            num+=1
            print(num)


if __name__ == "__main__":

    harvest_friends()
