# A harvester

A harvester used to harvest tweet with geo-location.

The harvester has two parts. friend_harvester and tweet_harvester. a database is used to store search records to avoid tweet duplication.

The friend_harvester only collect friends informaiton starting from a seed user.(AFLNews for exmaple). It sotres new user ID in the database and mark 'friends_harvested' to true after collecting one's friends( also add time stamp in 'last_time_friends_harvested')

The tweet_harvester find a un-visted user in database and collection this user's timeline. After collecting this user's tweet, the tweet_harvester mark the 'tweet_harvested' to true and add time stamp in 'last_time_tweet_harvested'

## Getting started

* Install TwitterAPI

```
pip3 install TwitterAPI MongoDB
```

* A Twitter Application Account for developer:[apply one](https://apps.twitter.com/)
```
Login with a twitter account and then apply for a application, collect your consumer key and tokens etc.
```

# HOW TO USE IT
## In the file support.py (deleted.)
* change 'search_tweets' to whichever tokens are you going to search.
* change the 'consumer_key','consumer_secret','access_token_key' and 'access_token_secret' to your own token


## Exception log
* Any exception occured will be record into log file. Usually the only exception is the duplication issue when inserting an existing tweet into database.

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Twitter API](https://github.com/geduldig/TwitterAPI) - API wrapper for harvest


* **Zelong Cong** - *Initial work* 

