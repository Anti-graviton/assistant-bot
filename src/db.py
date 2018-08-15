from pymongo import MongoClient, ASCENDING
from bson import ObjectId
from datetime import datetime
import re

db = MongoClient().FanapAssistant


class User:
    def __init__(self, user_id, phone_number, first_name, last_name, car_num=None, car_model=None):
        self.id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.car_num = car_num
        self.car_model = car_model
        self.created_on = datetime.now()

    def name(self):
        if self.last_name is not None:
            return "%s %s" % (self.first_name, self.last_name)
        else:
            return self.first_name


class UserRepository:
    def __init__(self):
        self.users = db.Users

    def create(self, user: User):
        return self.users.insert_one(user.__dict__)

    def get_all_users(self):
        return list(self.users.find({}))

    def get_by_id(self, user_id):
        return self.users.find_one({'id': user_id})

    def get_by_ids(self, user_ids):
        cursor = self.users.find({'id': {'$in': user_ids}})
        users = []
        for user in cursor:
            users.append(user)
        return users

    def stash_car_num(self, user_id, car_num):
        self.users.update_one({'id': user_id}, {'$set': {'car_num': car_num}})

    def stash_car_model(self, user_id, car_model):
        self.users.update_one({'id': user_id}, {'$set': {'car_model': car_model}})

    def flush_car_stash(self, user_id):
        self.user.update_one({'id': user_id}, {'$unset': {'car_num': '', 'car_model': ''}})

    def save_car(self, user_id):
        car = self.users.find_one({'id': user_id}, {'car_num': 1, 'car_model': 1, '_id': 0})
        if 'car_num' not in car or car['car_num'] is None:
            return None
        if 'car_model' not in car or car['car_model'] is None:
            return None
        self.users.update_one({'id': user_id}, {'$push': {'cars': dict(id=ObjectId(), car_num=car['car_num'],
                                                                       car_model=car['car_model'])
                                                          },
                                                '$unset': {'car_num': '', 'car_model': ''}})

    def delete_user_car(self, user_id, car_id):
        user = self.users.find_one({'id': user_id}, {'cars.car_num': 1, 'cars.car_model': 1, 'cars.id': 1, '_id': 0})
        car = list(filter(lambda c: c['id'] == ObjectId(str(car_id)), user['cars']))
        if len(car) > 0:
            car = car[0]
            self.users.update_one({'id': user_id}, {'$push': {'removed_cars':
                                                              {'car_num': car['car_num'],
                                                               'car_model': car['car_model']
                                                               }
                                                          },
                                                    '$pull': {'cars': {'id': ObjectId(str(car_id))}}
                                                    })

    def user_exists(self, user_id):
        return self.get_by_id(user_id) is not None


class Bid:
    price_pattern = r"\d{1,3}(\.\d{1,2}|)$"

    def __init__(self, user_id, price):
        if not self.isValidPrice(price):
            raise ValueError()
        self.user = user_id
        self.price = float(price)
        self.created_on = datetime.now()

    def isValidPrice(self, price):
        return re.match(self.price_pattern, price)


class BidsRepository:
    def __init__(self):
        self.bids = db.Bids

    def create(self, bid):
        self.bids.insert(bid.__dict__)

    def get_bidders(self):
        users_cursor = self.bids.aggregate([
            {'$sort': {'created_on': ASCENDING}},
            {'$group': {'_id': {'user': "$user"}, 'price': {'$last': "$price"}, 'user': {'$last': "$user"}}},
            {'$match': {'price': {'$gt': 0}}},
            {'$project': {'_id': 0, 'user': 1}}
        ])
        users_ids = []
        for user in users_cursor:
            users_ids.append(user['user'])
        users_dict = UserRepository().get_by_ids(users_ids)
        users = list(map(lambda u: User(u['id'], u['phone_number'], u['first_name'], u['last_name']), users_dict))
        return users


class Lot:
    def __init__(self, user_id):
        self.user_id = user_id
        self.created_on = datetime.now()


class LotsRepository:
    def __init__(self):
        self.lots = db.Lots

    def create(self, lot: Lot):
        self.lots.insert_one(lot.__dict__)

    def get_players(self):
        users_ids = []
        lots_cursor = self.lots.find({}, {'user_id': 1, '_id': 0})
        for lot in lots_cursor:
            users_ids.append(lot['user_id'])
        users_dict = UserRepository().get_by_ids(users_ids)
        users = list(map(lambda u: User(u['id'], u['phone_number'], u['first_name'], u['last_name']), users_dict))
        return users

    def get_by_user(self, user_id):
        return self.lots.find_one({'user_id': user_id})

    def delete_by_user(self, user_id):
        self.lots.delete_one({'user_id': user_id})
