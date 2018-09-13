# -*- coding: utf-8 -*-

from pymongo import MongoClient
from datetime import datetime, timedelta
from .models import User, Car, Event, UserState
from shared import State
from .utils import todict


class MongoRepository(object):
    def __init__(self):
        self.client = MongoClient('localhost:27017')  # ToDo use connection config


class UserRepository(MongoRepository):
    def __init__(self):
        super().__init__()
        self.collection = self.client.assistant_bot.users

    def add_user(self, user: User):
        self.collection.insert_one(todict(user))

    def find_user(self, user_id):
        user = self.collection.find_one({'user_id': user_id})
        return User.from_dict(user) if user is not None else None

    def get_users(self):
        cursor = self.collection.find({})
        users = map(lambda u: User.from_dict(u), cursor)
        return list(users)

    def find_participants(self, event_id):
        user_filter={'user_state':{'$elemMatch':{'event_id':event_id, 'state':State.REGISTERED.name}}}
        cursor = self.collection.find(user_filter)
        users = map(lambda u: User.from_dict(u), cursor)
        return list(users)

    def has_car(self, user_id):
        return self.find_user(user_id).car is not None

    def remove_car(self, user_id):
        return self.collection.update_one({'user_id': user_id},
                                          {'$unset': {'car': ''}})

    def add_car(self, user_id, model: str, plate_number: str):
        car = Car(plate_number, model)
        return self.collection.update_one({'user_id': user_id},
                                          {'$set': {'car': car.__dict__}})
            
    def participate(self, user_id, active_event_id):
        self.__update_user_state (user_id, State.REGISTERED, active_event_id)

    def withdraw(self, user_id, active_event_id):
        self.__update_user_state (user_id, State.UNREGISTERED, active_event_id)

    def __update_user_state(self, user_id: str, state: State, active_event_id: str):
        user_filter={"user_id":user_id, "user_state":{'$elemMatch': {'event_id':active_event_id}}}
        res = self.collection.update_one(user_filter,
                {"$set": {"user_state.$.modified_on": datetime.now(),
                          "user_state.$.state":state.name}})

        if res.matched_count < 1:
            res = self.collection.update_one(
                {"user_id": user_id},
                {"$push": {"user_state":
                           {"modified_on": datetime.now(),
                            "state": state.name,
                            "event_id": active_event_id}}})


class EventRepository(MongoRepository):
    def __init__(self):
        client = MongoClient('localhost:27017')
        self.collection = client.assistant_bot.events

    def find_active_event(self):
        now=datetime.now()
        event_filter ={'$and': [{'is_active':True},{'from_time':{'$lte':now}},{'to_time':{'$gte':now}}]}
        active_event = self.collection.find_one(event_filter)
        return Event.from_dict(active_event) if active_event is not None else None

    def add_event(self, duration):
        now = datetime.now()
        event_id = str(now.year)+'-'+str(now.month)+ '-'+str(now.day)+'-'+str(now.hour)+str(now.minute)+str(now.second)+str(now.microsecond)
        event = Event(now, now+timedelta(hours=duration), event_id, datetime.now(), True)
        self.collection.insert_one(todict(event))

    def deactive_event(self):
        event_filter={"is_active":True}
        update={"$set":{"is_active":False}}
        result=self.collection.update_one(event_filter,update)
        if result.matched_count>0:
            return True
        else:
            return False
