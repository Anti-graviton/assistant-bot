from pymongo import MongoClient
from datetime import datetime


class UserRepository(object):

    def __init__(self):
        client = MongoClient('localhost:27017')  # ToDo use connection config
        self.collection = client.assistant_bot.users

    def add_user(self, user):
        self.collection.insert_one(user.__dict__)

    def does_user_exist(self, user_id):
        return self.collection.find_one({"user_id": user_id}) is None

    # ToDo revisit method for feasibilty
    def does_car_already_registered(self, plate_number):
        filter = {"car.plate_number": plate_number}
        return self.collection.find_one(filter) is not None

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
