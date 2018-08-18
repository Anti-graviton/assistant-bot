# -*- coding: utf-8 -*-

import re
from mmpy_bot.bot import respond_to
from mmpy_bot.utils import allow_only_direct_message
from .utils import ensure_user_exist


@respond_to('^reg$', re.IGNORECASE)
@allow_only_direct_message()
@ensure_user_exist()
def register(message, user):
    if user.car is None:
        return message.send("لطفا یک ماشین تعریف کنید")
    # if has car, add activity record + set "has_participated"
    message.send("Registering %s" % user.car is not None)


@respond_to('^unreg$', re.IGNORECASE)
@allow_only_direct_message()
@ensure_user_exist()
def withdraw(message, user):
    # create user if not exist (using mm data)
    # if has_participated
    message.send("Unregister")


@respond_to('^rmcar$', re.IGNORECASE)
@allow_only_direct_message()
@ensure_user_exist()
def remove_car(message, user):
    message.send("Removing Car")


@respond_to('^addcar [\w\d], [\w\d]', re.IGNORECASE)
@allow_only_direct_message()
@ensure_user_exist()
def add_car(message, user):
    message.send("Adding Car")
