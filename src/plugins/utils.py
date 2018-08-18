# -*- coding: utf-8 -*-

from mmpy_bot.dispatcher import Message
from db.repository import UserRepository
from db.models import User


class ExtendedMessage(Message):
    def __init__(self, message: Message):
        super(ExtendedMessage, self).__init__(message._client, message._body, message._pool)

    def get_user_id(self):
        return self._body['data']['post']['user_id']

    def get_user_info(self):
        user_id = self.get_user_id()
        return self._client.api.get_user_info(user_id)


def ensure_user_exist():
    def wrapper(func):
        def find_or_create_user(message, *args, **kw):
            ext_message = ExtendedMessage(message)
            user_id = ext_message.get_user_id()
            repo = UserRepository()
            user = repo.find_user(user_id)

            if user is None:
                info = ext_message.get_user_info()
                user = User(user_id=user_id, email=info['email'],
                            username=info['username'], first_name=info['first_name'],
                            last_name=info['last_name'])
                repo.add_user(user)

            return func(ext_message, user, *args, **kw)
        return find_or_create_user
    return wrapper
