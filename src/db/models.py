# -*- coding: utf-8 -*-

from enum import Enum
from datetime import datetime


class Activity(Enum):
    WIN = 1
    WITHDRAW = 2
    EDIT_CAR = 3


class ActivityLog:
    def __init__(self, activity: Activity, activity_time: datetime,
                 detail: object = None):
        self.activity = activity
        self.activity_time = activity_time
        self.detail = detail


class Car:

    def __init__(self, plate_number, model):
        self.plate_number = plate_number
        self.model = model

    @staticmethod
    def from_dict(car: dict):
        return Car(car.get('plate_number'), car.get('model'))\
            if car is not None else None

    def __repr__(self):
        return '{} - {}'.format(self.model, self.plate_number)


class MongoEntity(object):

    def __init__(self):
        # _id will be automatically added by PyMongo
        self.created_on = datetime.now()
        self.modified_on = None


class User(MongoEntity):

    def __init__(self, user_id, username, email: str, phone_number: str = None,
                 first_name: str = None, last_name: str = None,
                 car: Car = None, participated=False):
        super(User, self).__init__()
        self.user_id = user_id
        self.username = username
        self.email = email
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.car = car
        self.participated = participated
        # self.activities = None

    @staticmethod
    def from_dict(user):
        return User(user['user_id'], user['username'], user['email'],
                    user.get('phone_number'), user['first_name'],
                    user['last_name'], Car.from_dict(user.get('car')),
                    user.get('participated'))

    def __repr__(self):
        return '<User {} - {}>'.format(self.id, self.username)
