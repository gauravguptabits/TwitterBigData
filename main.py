import sys
import argparse
from src.apps import get_streaming_tweets, get_historical_tweets


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [APP_NAME]",
        description="Execute the streaming or historical tweet fetching."
)
    parser.add_argument('--app', required=True)
    return parser


if __name__ == '__main__':
    parser = init_argparse()
    args = parser.parse_args()
    app_to_execute = args.app
    if app_to_execute == 'streaming_tweet_app':
        get_streaming_tweets()
    elif app_to_execute == 'historical_tweet_app':
        get_historical_tweets()
    else:
        raise ValueError('Invalid value {}'.format(app_to_execute))
