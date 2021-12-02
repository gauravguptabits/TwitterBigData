import os
import urllib.parse
from pymongo import MongoClient
from src.config import config
from glom import glom

__all__ = ['build_connection']

def build_connection():
    db_host = glom(config, 'db_config.host')
    db_port = glom(config, 'db_config.port')
    db_name = glom(config, 'db_config.dbname')
    db_user = glom(config, 'db_config.user')
    db_pass = glom(config, 'db_config.pass')

    url = f'mongodb://{db_host}:{db_port}/'
    client = MongoClient(url)
    db = client[db_name]
    return db
