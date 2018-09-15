# -*- coding: utf-8 -*-
from datetime import datetime
from shared import State


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


class UserState:
    def __init__(self, state, event_id, modified_on):
        self.status = state
        self.event_id = event_id
        self.modified_on = datetime.now

    @staticmethod
    def from_dict(user_state: dict):
        if user_state is not None:
            user = UserState(user_state.get('state'),
                             user_state.get('event_id'),
                             user_state.get('modified_on'))
            return user
        else:
            return None

    def __repr__(self):
        return repr((self.event_id, self.status, self.modified_on))


class MongoEntity(object):
    def __init__(self):
        self.created_on = datetime.now()
        self.modified_on = None


class User(MongoEntity):
    def __init__(self, user_id, username, email: str, phone_number: str = None,
                 first_name: str = None, last_name: str = None,
                 car: Car = None, user_state: [UserState] = []):
        super(User, self).__init__()
        self.user_id = user_id
        self.username = username
        self.email = email
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.car = car
        self.user_state = user_state

    def is_registered_in_event(self, event_id: str):
        return any(s['event_id'] == event_id
                   and s['state'] == State.REGISTERED.name
                   for s in self.user_state)

    @staticmethod
    def from_dict(user):
        user_id = user.get('id') or user.get('user_id')
        return User(user_id, user['username'], user['email'],
                    user.get('phone_number'), user['first_name'],
                    user['last_name'], Car.from_dict(user.get('car')),
                    user.get('user_state'))

    def __repr__(self):
        return '<User {} - {}>'.format(self.user_id, self.username)


class ActivityLog(MongoEntity):
    def __init__(self, user_id, action, activity_time: datetime = datetime.now,
                 details: dict = None):
        super(ActivityLog, self).__init__()
        self.user_id = user_id
        self.action = action
        self.activity_time = activity_time
        self.details = details

    @staticmethod
    def from_dict(activity_log):
        return ActivityLog(activity_log["user_id"], activity_log["action"],
                           activity_log["activity_time"],
                           activity_log["details"])


class Event(MongoEntity):
    def __init__(self, from_time, to_time, event_id, created_on, is_active):
        super(Event, self).__init__()
        self.from_time = from_time
        self.to_time = to_time
        self.is_active = is_active
        self.event_id = event_id

    @staticmethod
    def from_dict(event: dict):
        return Event(event.get('from_time'), event.get('to_time'),
                     event.get('event_id'), event.get('creted_on'),
                     event.get('is_active'))

    def __repr__(self):
        return '**From** {:%Y-%m-%d %H:%M}**, To** {:%Y-%m-%d %H:%M}'\
                .format(self.from_time, self.to_time)
