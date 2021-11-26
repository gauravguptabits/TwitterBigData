import os
import logging
import json
from datetime import datetime, timedelta
logging.basicConfig(filename="twitter.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)
import re
import tweepy
import uuid
import ast
# from credentials import access_token, access_token_secret, consumer_key, consumer_secret, mongodb_user, mongodb_pass
import urllib.parse
import pymongo
from pymongo import MongoClient
from datetime import datetime
from dbconnect import db
# #######################################################
# from dotenv import load_dotenv
# load_dotenv()
# mongodb_user  = os.environ['mongodb_user']
# mongodb_pass = os.environ['mongodb_pass']
# #*******************************************#
consumer_key = os.environ['consumer_key']
consumer_secret = os.environ['consumer_secret']
access_token = os.environ['access_token']
access_token_secret = os.environ['access_token_secret']

# ####################################################
# client = MongoClient('mongodb://localhost:27017/')

# username = urllib.parse.quote_plus(mongodb_user)
# password = urllib.parse.quote_plus(mongodb_pass)
# client = MongoClient('mongodb://%s:%s@localhost:27017/bigdata' % (username, password))

# client = MongoClient('mongodb://localhost:27017/')

# username = urllib.parse.quote_plus(mongodb_user)
# password = urllib.parse.quote_plus(mongodb_pass)
# client = pymongo.MongoClient("mongodb+srv://%s:%s@twitterdb.xgiie.mongodb.net/bigdata?retryWrites=true&w=majority" % (username, password))
# db = client['bigdata']




auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
# api = tweepy.API(auth,wait_on_rate_limit=True)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Change query api and req_params as requirement
query_api = api.search
def get_req_param(hastag):
    # current_date = datetime.now().strftime('%Y-%m-%d')
    # previous_date = (datetime.now() - timedelta(7)).strftime('%Y-%m-%d')
    current_date = '2021-11-23'
    previous_date = '2021-01-01'
    req_params = {"q": hastag, "count": 100, "lang": "en", 
                  "since": previous_date, "until": current_date}
    # req_params = {"q": hastag, "count": 100, "lang": "en"}
    return req_params


def get_metadata_update(req_id, req_params, req_res_status, req_res_message ):
    mdata = {"req_id": req_id,
             "req_params": req_params,
             "req_resp_status": req_res_status,
             "req_res_message": req_res_message}
    twitterMetaData = db.twitterMetaData
    twitterMetaData.insert_one(mdata)

def get_twitterdata_update(req_id,brand,category, tweetdata):
    twitterData = db.twitterData
    twdata = {"req_id":req_id,"brand":brand,"category":category,"tweetInfo":tweetdata}
    # print('twdata========>>>>>>>>',twdata)
    try:
        twitterData.insert_one(twdata)
        # print('tweet data inserted in mongodb successfully')
    except:
        print('tweet data already exist in mongodb')
        logger.info("Fialed to insert, already exist")

    # dup_count = twitterData.count_documents({"tweetInfo.id":tweetdata['id']})
    # if dup_count==0:
    #     twdata = {"req_id":req_id,"brand":brand,"category":category,"tweetInfo":tweetdata}
    #     # print('twdata========>>>>>>>>',twdata)
    #     twitterData.insert_one(twdata)
    #     print('tweet data inserted in mongodb successfully')
    # else:
    #     print('tweet data already exist in mongodb')
    #     logger.info("Fialed to insert, duplicate data")


def get_twitter_data(brand,category,req_param):
    count = 0
    tweet_count = 0
    try:
        req_id = str(uuid.uuid1())
        logger.debug(req_param)
        tweets = tweepy.Cursor(query_api, **req_param).items(20)
        for tweet in tweets:
            tweet_count +=1
            print('tweet at time=',str(datetime.now()))
            # logger.debug(req_param)
            # logger.info(tweet._json)
            if tweet:
                tweet._json['created_at'] = tweet.created_at
                req_res_status = 200
                req_res_message = "twitter data fetched successfully"
                print(tweet._json)
                get_twitterdata_update(req_id,brand,category,tweet._json)
                if count == 0:
                    get_metadata_update(req_id, req_param, req_res_status, req_res_message)
                    count+=1
            else:
                req_res_status = 404
                req_res_message = "twitter data not found for Hastag: "+ req_param['q']
                get_metadata_update(req_id, req_param, req_res_status, req_res_message)


    except tweepy.error.TweepError as e:
        req_res_status = e.response.status_code
        req_res_message = ast.literal_eval(e.response._content.decode('utf-8'))
        req_res_message = req_res_message['errors'][0]['message']
        get_metadata_update(req_id, req_param, req_res_status, req_res_message)
     
    return tweet_count


if __name__=="__main__":
    
    # hastags = ["#AmazonIndia", "#PanasonicIndia", "#SamsungIndia"]
    # hastags = ["#PanasonicACs"]
    # for hastag in hastags:
    #     req_param = get_req_param(hastag)
    #     get_twitter_data(req_param)
    with open('category_updated.json') as f:
        datas = json.load(f)

    for data  in datas['brands']:
        # print('*'*100)
        # print(brand)
        brand = data['name']
        category = data['categories'][0]
        hastags = data['platforms'][0]['hashtags']
        # print('hastags======>>>>>>>>>>>',hastags)
        for hastag in hastags:
            start_time = datetime.now().strftime('%Y-%m-%d, %H:%M:%S')
            req_param = get_req_param(hastag)
            tweet_count = get_twitter_data(brand,category,req_param)
            end_time = datetime.now().strftime('%Y-%m-%d, %H:%M:%S')
            logger.info(f"Scripts metrics: Start time:{start_time}\tend Time:{end_time}\tNum of tweets:{tweet_count}\t Hastag:{hastag}")







