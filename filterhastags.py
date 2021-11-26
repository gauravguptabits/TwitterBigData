import json

hastags_list = []

with open('category_updated.json') as f:
    datas = json.load(f)

for data  in datas['brands']:
    # print('*'*100)
    # print(brand)
    brand = data['name']
    category = data['categories'][0]
    hastags = data['platforms'][0]['hashtags']
    for hastag in hastags:
        hastags_list.append(hastag.lower())

# print('hastag list============>',hastags_list)

cat_hastags = set(hastags_list)

def get_hastags(htags, hastag_set):
        stream_hastags= ["#"+x["text"].lower() for x in htags]
        hastag_set.update(stream_hastags)


def get_hastag_list(raw_data):
    # print("streamming data inside filter ===========>",raw_data)
    data = json.loads(raw_data)
    try:
        hastag_set = set()
        if "extended_tweet" in data and data["extended_tweet"]["entities"]["hashtags"]:
            htags = data["extended_tweet"]["entities"]["hashtags"]
            get_hastags(htags, hastag_set)
        elif "entities" in data and data["entities"]["hashtags"] :
            htags = data["entities"]["hashtags"]
            get_hastags(htags, hastag_set)
        if "retweeted_status" in data:
            if "extended_tweet" in data["retweeted_status"] and data["retweeted_status"]["extended_tweet"]["entities"]["hashtags"]:
                htags = data["retweeted_status"]["extended_tweet"]["entities"]["hashtags"]
                get_hastags(htags, hastag_set)
            elif "entities" in data["retweeted_status"] and data["retweeted_status"]["entities"]["hashtags"]:
                htags = data["retweeted_status"]["entities"]["hashtags"]
                get_hastags(htags, hastag_set)

            if "quoted_status" in data["retweeted_status"]:
                if "extended_tweet" in data["retweeted_status"]["quoted_status"] and data["retweeted_status"]["quoted_status"]["extended_tweet"]["entities"]["hashtags"]:
                    htags = data["retweeted_status"]["quoted_status"]["extended_tweet"]["entities"]["hashtags"]
                    get_hastags(htags, hastag_set)
                elif "entities" in data["retweeted_status"]["quoted_status"] and data["retweeted_status"]["quoted_status"]["entities"]["hashtags"]:
                    htags = data["retweeted_status"]["quoted_status"]["entities"]["hashtags"]
                    get_hastags(htags, hastag_set)
            # print("in retweet status==========>",htags)
        # else:
        #     print("hastag are  not available in main data-")
        # print('final hastag_set =====================>',hastag_set)
        common_hastags = list(cat_hastags.intersection(hastag_set))
        if len(common_hastags):
            search_hastag = common_hastags[0]
            print('search hastag---------------------->',search_hastag)
            
            with open('category_updated.json') as f:
                cat_datas = json.load(f)
            for cat_data in cat_datas['brands']:
                hastags = cat_data['platforms'][0]['hashtags']
                if search_hastag in [x.lower() for x in hastags]:
                    brand = cat_data['name']
                    category = cat_data['categories'][0]
                    # print("cat brand ======>",brand, category)
                    return (brand, category)

        else:
            # print("No common hastag found ===============")
            brand = "Other"
            category = "Other"
            return (brand, category)
    except:
        print("Some error occured during filtering hastag")
        brand = "Other"
        category = "Other"
        return (brand, category)


