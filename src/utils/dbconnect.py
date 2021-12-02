import logging
import os
import urllib.parse
from pymongo import MongoClient
from src.config import config
from glom import glom

__all__ = ['build_connection', 'insert_tweet_metadata', 'insert_tweet']
SUCCESS_FETCH_STATUS_MSG = 'Twitter data fetched successfully'

logging.basicConfig(format='%(asctime)s %(message)s',
                    handlers=[
                        logging.FileHandler("twitter.log"),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def build_connection():
    db_host = glom(config, 'db_config.host')
    db_port = glom(config, 'db_config.port')
    db_name = glom(config, 'db_config.dbname')
    db_user = glom(config, 'db_config.user')
    db_pass = glom(config, 'db_config.pass')

    url = f'mongodb://{db_host}:{db_port}/'
    client = MongoClient(url)
    db = client[db_name]
    return db


def insert_tweet_metadata(req_id, req_params, db,
                          req_res_status=200,
                          req_res_message=SUCCESS_FETCH_STATUS_MSG):
    # logger.info('Updating metadata information')
    mdata = {
        "req_id": req_id,
        "req_params": req_params,
        "req_resp_status": req_res_status,
        "req_res_message": req_res_message
    }
    twitterMetaData = db.twitterMetaData
    return twitterMetaData.insert_one(mdata)


def insert_tweet(req_id, brand, category, tweetdata, db):
    # logger.info('Inserting Tweet')
    twitterData = db.twitterData
    twdata = {"req_id": req_id, "brand": brand,
              "category": category, "tweetInfo": tweetdata}
    try:
        twitterData.insert_one(twdata)
    except:
        logger.error("Fialed to insert, already exist")
    return
