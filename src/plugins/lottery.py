# -*- coding: utf-8 -*-

import re
from mmpy_bot.bot import respond_to
from mmpy_bot.utils import allow_only_direct_message, allowed_users
from .utils import ensure_user_exist
from db.repository import UserRepository, EventRepository
from db.models import Activity
from settings.settings import ADMINS


@respond_to(r'^reg\s*$', re.IGNORECASE)
@allow_only_direct_message()
@ensure_user_exist()
def register(message, user):
    active_event = EventRepository().find_active_event()
    if active_event is None:
        return message.send("در حال حاضر قرعه کشی فعالی وجود ندارد")

    if user.car is None:
        return message.send("لطفا یک ماشین تعریف کنید")
    
    state_for_active_event = list(filter(lambda c: c['event_id'] == active_event.event_id and c['action'] == Activity.REGISTERED.name, user.user_state)) if user.user_state is not None else []

    if  (len(state_for_active_event) <1 ):
        UserRepository().participate(user.user_id,active_event.event_id)
        message.react(":+1:")
    else:
        message.send("خیالت راحت، ثبت‌نام کردی!")


@respond_to(r'^unreg\s*$', re.IGNORECASE)
@allow_only_direct_message()
@ensure_user_exist()
def withdraw(message, user):
    
    active_event = EventRepository().find_active_event()
    if active_event is None:
        return message.send("در حال حاضر رویداد فعالی وجود ندارد")
        
    state_for_active_event = list(filter(lambda c: c['event_id'] == active_event.event_id and c['action'] == Activity.REGISTERED.name, user.user_state))

    if len( state_for_active_event) > 0 :
        UserRepository().withdraw(user.user_id,active_event.event_id)
        message.send("انصراف از قرعه‌کشی ثبت شد")
    else:
        message.send("گرفتی ما رو؟! اصلا ثبت‌نام نکردی که")


@respond_to(r'^mycar\s*$', re.IGNORECASE)
@allow_only_direct_message()
@ensure_user_exist()
def mycar(message, user):
    message.send(user.car.__repr__() if user.car is not None else 'پوچ!')


@respond_to(r'^rmcar\s*$', re.IGNORECASE)
@allow_only_direct_message()
@ensure_user_exist()
def remove_car(message, user):
    UserRepository().remove_car(user.user_id)
    message.send("اطلاعات ماشین حذف شد")


@respond_to(r'^addcar ([\w\s\d]+) - ((?:ایران|ايران|iran|ir)[\s]*[\d]{2} '
            r'[\d]{2}[\w]{1}[\d]{3})$', re.IGNORECASE)
@allow_only_direct_message()
@ensure_user_exist()
def add_car(message, user, model, plate_number, *args, **kwargs):
    UserRepository().add_car(user.user_id, model, plate_number)
    message.send("اطلاعات ماشین ثبت شد")

@respond_to(r'^ls\s*$', re.IGNORECASE)
@allow_only_direct_message()
@allowed_users(*ADMINS)
def list_participants(message):
    active_event_id=EventRepository().find_active_event()
    users = UserRepository().find_participants(active_event_id)
    usernames = '\n'.join(map(lambda u: "%s, %s" % (u.username, u.car.plate_number), users))
    message.send(usernames)


@respond_to(r'^la\s*$', re.IGNORECASE)
@allow_only_direct_message()
@allowed_users(*ADMINS)
def list_users(message):
    users = UserRepository().get_users()
    usernames = '\n'.join(map(lambda u: u.username, users))
    message.send(usernames)


@respond_to(r'^lopen\s+(\d{1,2})(h|d)\s*$', re.IGNORECASE)
@allow_only_direct_message()
@allowed_users(*ADMINS)
def add_event(message, duration, unit):
    active_event = EventRepository().find_active_event()
    if active_event is None:
        duration = int(duration)
        if unit == "d":
            duration = 24 * duration
        EventRepository().add_event(duration)
        message.send("قرعه کشی جدید ثبت گردید")
    else:
        message.send("در حال حاضر قرعه کشی فعال وجود دارد و شما نمی توانید قرعه کشی دیگری ثبت نمایید")


@respond_to(r'^lshow\s*$', re.IGNORECASE)
@allow_only_direct_message()
@allowed_users(*ADMINS)
def get_events(message):
    event = EventRepository().find_active_event()
    if event is not None:      
       message.send(event.__repr__())
    else:
        message.send('قرعه کشی فعالی وجود ندارد')


@respond_to(r'^lclose\s*$', re.IGNORECASE)
@allow_only_direct_message()
@allowed_users(*ADMINS)
def delete_event(message):
    event = EventRepository().deactive_event()
    if event is True:
        message.send('قرعه کشی با موفقیت غیرفعال شد')
    else:
        message.send('قرعه کشی فعالی وجود ندارد')
