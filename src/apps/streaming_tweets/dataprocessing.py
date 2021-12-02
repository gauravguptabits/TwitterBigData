import json
from dateutil.parser import parse
from .filterhastags import get_hastag_list
from src.utils.dbconnect import build_connection

class DataProcess:
    def __init__(self, raw_data,logger=None, brand=None, category=None):
        self.raw_data = raw_data
        self.data = json.loads(raw_data)
        self.brand = brand
        self.category = category
        self.logger = logger

    def changedateformat(self):
        self.data["created_at"] = parse(self.data["created_at"])
        # print('date modified')

    def get_filter_data(self):
        self.brand, self.category = get_hastag_list(self.raw_data)
        print('brand and category: ',self.brand, self.category)

    def save_to_mongodb(self, db):
        twitterStreamData = db.twitterStreamData
        twdata = {"brand":self.brand, "category":self.category,"tweetInfo":self.data}
        try:
            twitterStreamData.insert_one(twdata)
            # self.logger.info("data inserted succesfully")

        except:
            print('data already exist')
            self.logger.info("Fialed to insert, already exist")

def do_dataprocess(raw_data,logger):
    print("tweet streamming data ===========>",raw_data)
    db = build_connection()
    dataprocess = DataProcess(raw_data,logger)
    dataprocess.changedateformat()
    dataprocess.get_filter_data()
    dataprocess.save_to_mongodb(db)



        

