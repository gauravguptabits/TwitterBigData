import json
from copy import deepcopy

def get_brand_config(config_file_path):
    datas = {}
    with open(config_file_path) as f:
        datas = json.load(f)
    
    brand_config = deepcopy(datas)
    brand_config['brands'] = list(filter(lambda brand: brand.get('active', False), brand_config['brands']))
    return brand_config
