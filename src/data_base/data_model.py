from enum import Enum

class data_model(object):
    """description of class"""
class User:
    def __init__(self, user_id, phone_number=None, first_name=None, last_name=None, car=None, user_sate=[]):
        self.id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.car=car
        self.user_state=user_state
        self.created_on = datetime.now()

class Car:
    def __init__(self,model,plate_number):
        self.model=model
        self.plate_number=plate_number

class UserState:
    def __init__ (self,state,activity_time,event_id):
        self.event_id=event_id
        self.action=action
        self.activity_time=activity_time

class Event:
    def __init__(self,from_time,to_time,event_id,created_on,is_active,identifier):
        self.from_time=from_time
        self.to_time=to_time
        self.is_active=is_active
        self.identifier:identifier
        self.created_on=created_on



State = Enum("State","registered participated won")

    



