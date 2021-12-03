import logging
from datetime import datetime, timedelta
import tweepy
from glom import glom
import uuid
import ast
from datetime import datetime
from src.utils.dbconnect import build_connection, insert_tweet_metadata, insert_tweet
from src.utils.core import get_brand_config
from src.config import config
import copy
from math import inf
from deprecated import deprecated

logging.basicConfig(format='%(asctime)s %(message)s',
                    handlers=[
                        logging.FileHandler("twitter.log"),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger()
logger.setLevel(logging.INFO)

'''

@deprecated(version='0.0.1', reason='Need not helper function to source data for last 7 days.')
def get_twitter_data(brand,category,req_param):
    api, _ = initialize()
    query_api = api.search_tweets
    count = 0
    tweet_count = 0
    db = build_connection()
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
                logger.debug(tweet._json)
                insert_tweet(req_id,brand,category,tweet._json, db)
                if count == 0:
                    insert_tweet_metadata(req_id, req_param, req_res_status, req_res_message, db)
                    count+=1
            else:
                req_res_status = 404
                req_res_message = "twitter data not found for Hastag: "+ req_param['q']
                insert_tweet_metadata(req_id, req_param, req_res_status, req_res_message, db)


    except tweepy.error.TweepError as e:
        req_res_status = e.response.status_code
        req_res_message = ast.literal_eval(e.response._content.decode('utf-8'))
        req_res_message = req_res_message['errors'][0]['message']
        insert_tweet_metadata(req_id, req_param, req_res_status, req_res_message)
     
    return tweet_count

@deprecated(version='0.0.1', reason='Need not source data of last 7 days only.')
def get_7days_tweets():
    brand_configuration_file = glom(config, 'brand_configuration_file')
    brand_configuration = get_brand_config(brand_configuration_file)

    for data in brand_configuration['brands']:
        brand = data['name']
        logger.info(f'\n <<<< BRAND: {brand} >>>>>\n')
        category = data['categories'][0]
        hastags = data['platforms'][0]['hashtags']
        # print('hastags======>>>>>>>>>>>',hastags)
        for hastag in hastags:
            start_time = datetime.now().strftime('%Y-%m-%d, %H:%M:%S')
            req_param = get_req_param(hastag)
            logger.info(f'\n <<<< BRAND: {brand} >>>>>\n')
            tweet_count = get_twitter_data(brand, category, req_param)
            end_time = datetime.now().strftime('%Y-%m-%d, %H:%M:%S')
            logger.info(f"Scripts metrics: Start time:{start_time}\tend Time:{end_time}\tNum of tweets:{tweet_count}\t Hastag:{hastag}")

@deprecated(version='0.0.1', reason='Need not source data of last 7 days only.')
def get_req_param(hastag):
    # current_date = datetime.now().strftime('%Y-%m-%d')
    # previous_date = (datetime.now() - timedelta(7)).strftime('%Y-%m-%d')
    current_date = '2021-02-01'
    previous_date = '2021-01-01'
    req_params = {
        "q": hastag, 
        "count": 100, 
        "lang": "en",
        # "since": previous_date, 
        # "until": current_date
    }
    # req_params = {"q": hastag, "count": 100, "lang": "en"}
    return req_params
'''

def initialize():
    logger.info('### Initializing Twitter Client ###')
    consumer_key = glom(config, 'twitter_app.consumer_key')
    consumer_secret = glom(config, 'twitter_app.consumer_secret')
    access_token = glom(config, 'twitter_app.access_token')
    access_token_secret = glom(config, 'twitter_app.access_token_secret')
    access_token_secret = glom(config, 'twitter_app.access_token_secret')
    bearer_token = glom(config, 'twitter_app.bearer_token')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    tweepy.debug(enable=False, level=0)
    # api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    client = tweepy.Client(bearer_token=bearer_token,
                        consumer_key=consumer_key,
                        consumer_secret=consumer_secret,
                        access_token=access_token,
                        return_type='dict',
                        wait_on_rate_limit=True,
                        access_token_secret=access_token_secret)
    return api, client


def get_historical_tweets():
    logger.info('[ENTER] get_historical_tweets')
    start_time = '2020-01-01T00:00:00Z'
    end_time = '2021-01-01T00:00:00Z'
    _, client = initialize()
    brand_configuration_file = glom(config, 'brand_configuration_file')
    brands_configuration = get_brand_config(brand_configuration_file)
    logger.info('Brands to work on\n{}'.format(brands_configuration))

    # API params
    t_fields = ['attachments', 'author_id', 'conversation_id', 'created_at', 'entities', 'geo', 'id', 'withheld',
                'in_reply_to_user_id', 'lang', 'public_metrics', 'possibly_sensitive', 'referenced_tweets', 'reply_settings', 'source', 
                'text']
    u_fields = ['created_at', 'description', 'entities', 'id', 'location', 'name', 'pinned_tweet_id', 'protected',
                'profile_image_url', 'public_metrics', 'url', 'username', 'verified', 'withheld']
    expansion = ['referenced_tweets.id', 'entities.mentions.username','geo.place_id', 'in_reply_to_user_id', 
                'referenced_tweets.id.author_id']
    media_fields = ['duration_ms', 'height', 'media_key', 'preview_image_url', 'type', 'url', 'width', 'public_metrics', 'alt_text']
    place_fields = ['contained_within', 'country', 'country_code', 'full_name', 'geo', 'id', 'name', 'place_type']
    poll_fields = ['duration_minutes', 'end_datetime', 'id', 'options', 'voting_status']

    db = build_connection()

    for brand_config in brands_configuration.get('brands', []):
        brand = brand_config.get('name', None)
        category = brand_config.get('categories', [])        
        platforms = brand_config.get('platforms', [])

        twitter_config = next(plat for plat in platforms if plat['name'] == 'Twitter')
        hashtags = twitter_config.get('hashtags', [])
        ORified_hashtags = " OR ".join(hashtags)
        query = f'({ORified_hashtags}) lang:en'
        # TODO: make paginated API call for all hashtags of this brand.
        tweets = tweepy.Paginator(client.search_all_tweets,
                                    query=query,
                                    start_time=start_time,
                                    end_time=end_time,
                                    tweet_fields=t_fields,
                                    media_fields=media_fields,
                                    poll_fields=poll_fields,
                                    user_fields=u_fields,
                                    max_results=500
                                    ).flatten(limit=inf)
        req_id = str(uuid.uuid1())
        for tweet in tweets:
            tweet_json = copy.deepcopy(tweet.data)
            rt = tweet.get('referenced_tweets')
            created_at = tweet.get('created_at')
            tweet_json['referenced_tweets'] = dict(rt) if rt is not None else {}
            tweet_json['created_at'] = str(created_at)
            insert_tweet(req_id, brand, category, tweet_json, db)
            insert_tweet_metadata(req_id, query, db)

    return
