import os
from dotenv import load_dotenv

dotenvpath = os.path.join(os.getcwd(), '.env')
load_dotenv(dotenvpath) if os.path.exists(dotenvpath) else None

config = {
    'brand_configuration_file': os.path.join(os.getcwd(), 'src', 'config', 'category_updated.json'),
    'db_config': {
        'host': 'localhost',
        'port': '27017',
        'dbname': 'bigdata_dev',
        'user': os.environ.get('mongodb_user'),
        'pass': os.environ.get('mongodb_pass')
    },
    'twitter_app': {
        'consumer_key': os.environ.get('consumer_key'),
        'consumer_secret': os.environ.get('consumer_secret'),
        'access_token': os.environ.get('access_token'),
        'access_token_secret': os.environ.get('access_token_secret'),
        'bearer_token': os.environ.get('bearer_token')
    },
    'mail_setting': {
        'user_email': os.environ.get('user_email'),
        'user_email_pass': os.environ.get('user_email_pass')
    }
}
