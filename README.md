## About

- Script to fetch data from Twitter and save in MongoDB. 
- Look for updating configuration file based on environment you are running on. 
    - Checkout `src/config` folder.
    - `.env` file in root folder.

Structure of .env file [WE NEED PUSH THIS FILE ON SOURCE CONTROL]
```
consumer_key=<value>
consumer_secret=<value>
access_token=<value>
access_token_secret=<value>
bearer_token=<value>
user_email=<value>
user_email_pass=<value>
mongodb_user=<value>
mongodb_pass=<value>
PYTHON_ENV=staging or local
PYTHON_APP_NAME=historical_tweet_app or streaming_tweet_app

```

## How to run

via Docker
- `docker-compose up -d --build`