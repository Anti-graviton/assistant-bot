# -*- coding: utf-8 -*-

import re
from mmpy_bot.bot import respond_to
from mmpy_bot.utils import allow_only_direct_message
from .utils import ensure_user_exist
from db.repository import UserRepository


@respond_to('^(?!(reg|unreg|addcar|rmcar|lscar)).*$', re.IGNORECASE)
@allow_only_direct_message()
@ensure_user_exist()
def uknown(message, *args, **kwargs):
    text = '''
### نمی‌فهمم چی می‌گی!
من یه ربات دون‌پایه‌ام! لطفا عین همین شیوه‌ای که این پایین نوشته با من صحبت کن.

|command|معنی|
|------|-----------------|
|reg  ‌ |‌ثبت‌نام در قرعه‌کشی|
|unreg |انصراف از قرعه‌کشی|
|addcar| اضافه کردن ماشین|
|rmcar |حذف ماشین        |
|lscar |اطلاعات ماشین     |

برای اضافه کردن ماشین یکم باید تمرکز کنی.
بعد از دستور باید دو تا مقدار بهم بدی که با خط تیره (-) از هم جدا شده‌ان.
اولی مدل ماشین و دومی شماره پلاکه.
مثال:
addcar pride - iran99 99b999
addcar پراید - ایران۹۹ ۹۹ب۹۹۹

اگر هم مشکلی داشتی، به حسین یا ابوالفضل بگو:
[@hossein.t](http://fanype.fanap.plus/fanap/messages/@hossein.t)
[@abolfazl](http://fanype.fanap.plus/fanap/messages/@abolfazl)
'''
    message.send(text)


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


@respond_to('^lscar\s*$', re.IGNORECASE)
@allow_only_direct_message()
@ensure_user_exist()
def remove_car(message, user):
    message.send(user.car.__repr__() if user.car is not None else 'پوچ!')


@respond_to('^rmcar\s*$', re.IGNORECASE)
@allow_only_direct_message()
@ensure_user_exist()
def remove_car(message, user):
    UserRepository().remove_car(user.user_id)
    message.send("اطلاعات ماشین حذف شد")


@respond_to('^addcar [\w\d], [\w\d]$', re.IGNORECASE)
@allow_only_direct_message()
@ensure_user_exist()
def add_car(message, user):
    UserRepository().add_car(user.user_id, "toyota", "iran44")
    message.send("اطلاعات ماشین ثبت شد")


def default_reply(message):
    message.send("default")