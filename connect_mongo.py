from pymongo import MongoClient
import datetime

class db_client(object):

    def __init__(self):
        self.client = MongoClient('mongodb://115.146.92.106:27017/')
        self.db_tweet=self.client['tweet']
        self.collection_users=self.db_tweet['users']
        self.collection_tweets=self.db_tweet['tweets']

    # find a user whose friends information are not in the database.
    # set friends_harvested to True, indicating his friends is harvested.
    # set lt_harvest_friends to current time to indicate the time his friends was harvested.
    # return ID
    def find_user_for_friends(self):
        return self.collection_users.find_one_and_update(
            {"friends_harvested":False},
            {"$set":
                 {"friends_harvested":True,'lt_harvest_friends': datetime.datetime.utcnow()}
             })['_id']

    # find a user whose tweet information are not in the database
    def find_user_for_tweeets(self):
        return self.collection_users.find_one_and_update(
            {"tweets_harvested":False},
            {"$set":
                 {"tweets_harvested":True,"lt_harvest_tweets": datetime.datetime.utcnow()}
             })["_id"]


    def insert_new_user(self, content):
        try:
            self.collection_users.insert(content)
        except Exception as e:
            with open('mongodb_log', 'a') as f:   # a -> append to the bottom line
                f.write("[" + datetime.datetime.now().__str__() + "]" + '\n')
                f.write(str(e) + '\n')
                f.write((content['_id'] + '\n'))


    # insert a new document to the tweet collection
    def insert_new_tweet(self, content):
        try:
            self.collection_tweets.insert(content)
        except Exception as e:
            with open('mongodb_log', 'a') as f:   # a -> append to the bottom line
                f.write("[" + datetime.datetime.now().__str__() + "]" + '\n')
                f.write(str(e) + '\n')
                f.write((content['_id'] + '\n'))

