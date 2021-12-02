import os
import sys
import logging
import threading
import json
from datetime import datetime, timedelta
from dateutil.parser import parse
from pymongo import MongoClient
from datetime import datetime, timedelta
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import Stream
from .dataprocessing import do_dataprocess
from src.utils.sendemail import send_mail
from glom import glom
from src.config import config
from src.utils.core import get_brand_config

logging.basicConfig(filename="twittStream.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)

class TweetListener(Stream):
    def __init__(self, api):
        super().__init__(api) # call superclass's init

    def on_data(self, raw_data):
        # data = json.loads(raw_data)
        data_process_thread = threading.Thread(target=do_dataprocess, args=(raw_data,logger))
        data_process_thread.start()

        return(True)

    
    def on_error(self, status_code):
        print(status_code)
        """Called when a non-200 status code is returned"""
        # if status_code == 420:
        #     #returning False in on_error disconnects the stream
        #     return False
        return True

def get_streaming_tweets():
    user_email = glom(config, 'mail_setting.user_email')
    user_email_pass = glom(config, 'mail_setting.user_email_pass')
    consumer_key = glom(config, 'twitter_app.consumer_key')
    consumer_secret = glom(config, 'twitter_app.consumer_secret')
    access_token = glom(config, 'twitter_app.access_token')
    access_token_secret = glom(config, 'twitter_app.access_token_secret')
    brand_config_filepath = glom(config, 'brand_configuration_file')

    try:
        brand_config = get_brand_config(brand_config_filepath)
        hastags_list = []
        for data in brand_config['brands']:
            brand = data['name']
            category = data['categories'][0]
            hastags = data['platforms'][0]['hashtags']
            for hastag in hastags:
                hastags_list.append(hastag)

        # print('hastag list------>',hastags_list)
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        twitterStream = Stream(auth, TweetListener(api))
        twitterStream.filter(track=hastags_list,is_async=True, languages=["en"])
    except Exception as e:
        print("Error Occured during Streaming")
        send_mail(user_email, user_email_pass, e)
    


        

    
