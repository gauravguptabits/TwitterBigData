# import os
# import sys
import itertools
from kafka import KafkaProducer
import logging
# import threading
import json
# from datetime import datetime, timedelta
# from dateutil.parser import parse
# from pymongo import MongoClient
# from datetime import datetime, timedelta
import tweepy
# from tweepy import Stream
# from tweepy import OAuthHandler
# from tweepy.streaming import Stream
# from .dataprocessing import do_dataprocess
# from src.utils.sendemail import send_mail
from src.utils.core import get_brand_config
from glom import glom
from src.config import config

logging.basicConfig(filename="twittStream.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger=logging.getLogger()
logger.setLevel(logging.INFO)


class BrandStream(tweepy.Stream):
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        super().__init__(consumer_key, consumer_secret, access_token, access_token_secret)
        self.producer = None

    def set_kafka_producer(self, kafka_producer):
        self.producer = kafka_producer
        return

    def on_data(self, raw_data):
        data = json.loads(raw_data).get('text')
        logger.info(f'On-Data {data}')
        self.producer.send('tweets', raw_data)
        return

def get_hashtag_list(brand_config_filepath):
    brand_config = get_brand_config(brand_config_filepath)
    brands_hashtags = [data['platforms'][0]['hashtags'] for data in brand_config['brands']]
    hashtags_to_track = list(itertools.chain(*brands_hashtags))
    return hashtags_to_track

def get_streaming_tweets():
    brand_config_filepath = glom(config, 'brand_configuration_file')
    consumer_key = glom(config, 'twitter_app.consumer_key')
    consumer_secret = glom(config, 'twitter_app.consumer_secret')
    access_token = glom(config, 'twitter_app.access_token')
    access_token_secret = glom(config, 'twitter_app.access_token_secret')
    hashtags = get_hashtag_list(brand_config_filepath)
    producer = KafkaProducer(bootstrap_servers=['localhost:9091', 'localhost:9092', 'localhost:9093'])


    logger.info(hashtags)
    stream = BrandStream(consumer_key, consumer_secret,
                         access_token, access_token_secret)
    stream.set_kafka_producer(producer)
    stream.filter(track=hashtags, languages=['en'])
        

    
