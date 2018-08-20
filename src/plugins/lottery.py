# -*- coding: utf-8 -*-

import re
from mmpy_bot.bot import respond_to
from mmpy_bot.utils import allow_only_direct_message, allowed_users
from .utils import ensure_user_exist
from db.repository import UserRepository


@respond_to('^reg\s*$', re.IGNORECASE)
@allow_only_direct_message()
@ensure_user_exist()
def register(message, user):
    if user.car is None:
        return message.send("لطفا یک ماشین تعریف کنید")

    if not user.participated:
        UserRepository().participate(user.user_id)
        message.react(":+1:")
    else:
        message.send("خیالت راحت، ثبت‌نام کردی!")


@respond_to('^unreg\s*$', re.IGNORECASE)
@allow_only_direct_message()
@ensure_user_exist()
def withdraw(message, user):
    if user.participated:
        UserRepository().withdraw(user.user_id)
    message.send("انصراف از قرعه‌کشی ثبت شد")


@respond_to('^mycar\s*$', re.IGNORECASE)
@allow_only_direct_message()
@ensure_user_exist()
def mycar(message, user):
    message.send(user.car.__repr__() if user.car is not None else 'پوچ!')


@respond_to('^rmcar\s*$', re.IGNORECASE)
@allow_only_direct_message()
@ensure_user_exist()
def remove_car(message, user):
    UserRepository().remove_car(user.user_id)
    message.send("اطلاعات ماشین حذف شد")


@respond_to('^addcar ([\w\s\d]+) - ((?:ایران|ايران|iran|ir)[\s]*[\d]{2} '
            '[\d]{2}[\w]{1}[\d]{3})$', re.IGNORECASE)
@allow_only_direct_message()
@ensure_user_exist()
def add_car(message, user, model, plate_number, *args, **kwargs):
    UserRepository().add_car(user.user_id, model, plate_number)
    message.send("اطلاعات ماشین ثبت شد")

@respond_to('^ls\s*$', re.IGNORECASE)
@allow_only_direct_message()
@allowed_users('hossein.t', 'abolfazl')
def list_participants(message):
    users = UserRepository().find_participants()
    usernames = '\n'.join(map(lambda u: u.username, users))
    message.send(usernames)
