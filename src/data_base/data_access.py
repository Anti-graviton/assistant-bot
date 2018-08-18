import pymongo
import data_model
from pymongo import MongoClient
from enum import Enum
from datetime import datetime

class data_access(object):
    """description of class"""
client = MongoClient('localhost:27017')

def get_collection(collectionName):
    db = client['test']
    return db[collectionName]

def  add_user(user):
         get_collection('User').insert_one(user.__dict__)

def does_user_exist(user_id):
         filter = { "user_id": user_id }
         res=get_collection('User').find_one(filter)
         if res is None:
            return False
         else:
            return True

def does_car_already_registered(plate_number):
    filter={"car.plate_number":plate_number}
    res=get_collection('User').find_one(filter)
    if res is None:
        return False
    else:
       return True


def add_or_update_user_state(user_id,state):

     event_filter = { "from_time": { "$lte": datetime.now() },"to_time":{"$gte":datetime.now() },"is_active":1 }
     active_event_id=get_collection('Event').find_one(event_filter)

     if active_event_id is not None:
         res= get_collection('User').update_one({"user_id": user_id,"user_state.event_id":active_event_id['identifier']},{"$set": {"user_state.$.activity_time":datetime.now(),"user_state.$.action":state}})
     if res.matched_count <1 :
                  res= get_collection('User').update_one({"user_id": user_id},{"$push": {"user_state":{"activity_time":datetime.now(),"action":state,"event_id":active_event_id['identifier']}}})








