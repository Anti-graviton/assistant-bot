from datetime import datetime
from bson import ObjectId


class BaseModel(object):

    id = ObjectId()
    date_created = datetime.now()
    date_modified = None


class User(BaseModel):

    def __init__(self, user_id, username, nickname, first_name, last_name, email, cars=[]):
        self.user_id = user_id
        self.active = True
        self.date_created = datetime.now()
        self.username = username
        self.nickname = nickname
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.cars = cars

    def __repr__(self):
        return '<User {} - {}>'.format(
            self.user_id,
            'Active' if self.active else 'Inactive')


class Car(BaseModel):

    def __init__(self, plate_number, model):
        self.plate_number = plate_number
        self.model = model
        self.active = True

    def __repr__(self):
        return '<Car {} - {}>'.format(
            self.model, self.plate_number)
