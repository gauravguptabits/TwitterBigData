import os
import urllib.parse
from pymongo import MongoClient

mongodb_user  = os.environ['mongodb_user']
mongodb_pass = os.environ['mongodb_pass']

# ########################################################

# username = urllib.parse.quote_plus(mongodb_user)
# password = urllib.parse.quote_plus(mongodb_pass)
# client = MongoClient('mongodb://%s:%s@localhost:27017/bigdata' % (username, password))

client = MongoClient('mongodb://localhost:27017/')

# username = urllib.parse.quote_plus(mongodb_user)
# password = urllib.parse.quote_plus(mongodb_pass)
# client = MongoClient("mongodb+srv://%s:%s@twitterdb.xgiie.mongodb.net/bigdata?retryWrites=true&w=majority" % (username, password))

db = client['bigdata']