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
from tweepy.streaming import StreamListener
from dataprocessing import do_dataprocess
from sendemail import send_mail

logging.basicConfig(filename="twittStream.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)

user_email = os.environ["user_email"]  
user_email_pass = os.environ["user_email_pass"] 
consumer_key = os.environ['consumer_key']
consumer_secret = os.environ['consumer_secret']
access_token = os.environ['access_token']
access_token_secret = os.environ['access_token_secret']


class TweetListener(StreamListener):
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


def send_notification(e):
    send_mail(user_email, user_email_pass,e)

def main():
    try:
        with open('category_updated.json') as f:
            datas = json.load(f)
        hastags_list = []
        for data  in datas['brands']:
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
        send_notification(e)




if __name__=="__main__":
    main()
    


        

    