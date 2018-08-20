# -*- coding: utf-8 -*-

from pymongo import MongoClient
from datetime import datetime
from .models import User, Car
from .utils import todict


class UserRepository(object):

    def __init__(self):
        client = MongoClient('localhost:27017')  # ToDo use connection config
        self.collection = client.assistant_bot.users

    def add_user(self, user: User):
        self.collection.insert_one(todict(user))

    def find_user(self, user_id):
        user = self.collection.find_one({'user_id': user_id})
        return User.from_dict(user) if user is not None else None

    def get_users(self):
        cursor = self.collection.find({})
        users = map(lambda u: User.from_dict(u), cursor)
        return list(users)

    def find_participants(self):
        cursor = self.collection.find({'participated': True})
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

    def participate(self, user_id):
        self.__update_participation(user_id, True)

    def withdraw(self, user_id):
        self.__update_participation(user_id, False)

    def __update_participation(self, user_id: str, value: bool):
        self.collection.update_one({'user_id': user_id},
                                   {'$set': {'participated': value}})

    # ToDo revisit logic
    def update_user_state(self, user_id, state):
        event_filter = {"from_time": {"$lte": datetime.now()}, "to_time": {
            "$gte": datetime.now()}, "is_active": 1}
        active_event_id = self.collection.find_one(event_filter)

        if active_event_id is not None:
            res = self.collection.update_one(
                {"user_id": user_id,
                 "user_state.event_id": active_event_id['identifier']},
                {"$set": {"user_state.$.activity_time": datetime.now(),
                          "user_state.$.action": state}})

        if res.matched_count < 1:
            res = self.collection.update_one(
                {"user_id": user_id},
                {"$push": {"user_state":
                           {"activity_time": datetime.now(),
                            "action": state,
                            "event_id": active_event_id['identifier']}}})
