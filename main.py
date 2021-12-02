from src.apps import get_streaming_tweets, get_historical_tweets

app_to_execute = 'historical_tweet_app'

if app_to_execute == 'streaming_tweet_app':
    get_streaming_tweets()
elif app_to_execute == 'historical_tweet_app':
    get_historical_tweets()
else:
    raise ValueError('Invalid value {}'.format(app_to_execute))
