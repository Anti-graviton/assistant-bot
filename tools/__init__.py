import pymongo
from pymongo import MongoClient
from mattermostdriver import Driver

client = MongoClient('localhost', 27017)

db = client.matterthon
user_collection = db['users']

print("Creating Mattermost Driver...")
driver_options = {
    'url': '172.16.30.11',
    'login_id': 'kia',
    'password': '123456',
    'port': 8065,
    'scheme': 'http'
}

driver = Driver(driver_options)
