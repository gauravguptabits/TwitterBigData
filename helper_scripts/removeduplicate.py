import os
from sshtunnel import SSHTunnelForwarder
import pymongo
import pprint
import logging
from bson.objectid import ObjectId

logging.basicConfig(filename="test_twittStream.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)

# mongodb_user  = os.environ['mongodb_user']
# mongodb_pass = os.environ['mongodb_pass']
MONGO_HOST = os.environ['MONGO_HOST']
MONGO_DB = os.environ['MONGO_DB']
MONGO_USER = os.environ['MONGO_USER']
MONGO_PASS = os.environ['MONGO_PASS']

server = SSHTunnelForwarder(
    MONGO_HOST,
    ssh_username=MONGO_USER,
    ssh_password=MONGO_PASS,
    remote_bind_address=('127.0.0.1', 27017)
)

server.start()

client = pymongo.MongoClient('127.0.0.1', server.local_bind_port) # server.local_bind_port is assigned local port
db = client[MONGO_DB]
pprint.pprint(db.collection_names())
col = db.twitterData
for d in col.find():
    # print(d)
    try:
        db.twitterData2.insert_one(d)
    except:
        print('data already existed')
        logger.info("Fialed to insert, duplicate data")

# After insertion complete, rename twitterData2 to twitterData

# id = "6176aa16a0d4b2e901ee8ca9"
# objInstance = ObjectId(id)
# myquery = { "_id": objInstance }
# mydoc = db.twitterStreamData.find(myquery)

# for x in mydoc:
#     # print('obj is --------------------------',x)
#     try:
#         col2 = db.twitterStreamData2.insert_one(x)
#     except:
#         print('data already exist')
#         logger.info("Fialed to insert, duplicate data")

###STOP SERVER ####
server.stop()