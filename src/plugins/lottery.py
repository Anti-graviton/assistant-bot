# -*- coding: utf-8 -*-

import re
from mmpy_bot.bot import respond_to
from mmpy_bot.utils import allow_only_direct_message, allowed_users
from .utils import ensure_user_exist,ensure_event_exist
from db.repository import UserRepository, EventRepository, ActivityLogRepository
from db.models import ActivityLog
from shared import State, Action
from settings.settings import ADMINS
from .messages import Strings
from datetime import datetime


@respond_to(r'^reg\s*$', re.IGNORECASE)
@allow_only_direct_message()
@ensure_event_exist()
@ensure_user_exist()
def register(message, user, active_event):

    if user.car is None:
        return message.send(Strings.DEFINE_CAR)
    
    state_for_active_event = list(filter(lambda c: c['event_id'] == active_event.event_id and c['state'] == State.REGISTERED.name, user.user_state))

    if  (len(state_for_active_event) <1 ):
        UserRepository().participate(user.user_id,active_event.event_id)
        message.react(Strings.SUCCESSFUL_REGISTERATION)
    else:
        message.send(Strings.ALREADY_REGISTERED)


@respond_to(r'^unreg\s*$', re.IGNORECASE)
@allow_only_direct_message()
@ensure_event_exist()
@ensure_user_exist()
def withdraw(message, user, active_event):
           
    state_for_active_event = list(filter(lambda c: c['event_id'] == active_event.event_id and c['state'] == State.REGISTERED.name, user.user_state))

    if len( state_for_active_event) > 0 :
        UserRepository().withdraw(user.user_id,active_event.event_id)
        message.send(Strings.UNDO_REGISTERATION)
    else:
        message.send(Strings.NOT_YET_REGISTERED)


@respond_to(r'^mycar\s*$', re.IGNORECASE)
@allow_only_direct_message()
@ensure_user_exist()
def mycar(message, user):
    message.send(user.car.__repr__() if user.car is not None else Strings.NO_CAR_EXISTS)


@respond_to(r'^rmcar\s*$', re.IGNORECASE)
@allow_only_direct_message()
@ensure_event_exist()
@ensure_user_exist()
def remove_car(message, user, active_event):
    UserRepository().remove_car(user.user_id)
    UserRepository().withdraw(user.user_id,active_event.event_id)
    activity_log=ActivityLog(Action.RMCAR.name, datetime.now(),active_event.event_id,user.user_id )
    ActivityLogRepository().log_action(activity_log)
    message.send(Strings.CAR_REMOVED)


@respond_to(r'^addcar ([\w\s\d]+) - ((?:ایران|ايران|iran|ir)[\s]*[\d]{2} '
            r'[\d]{2}[\w]{1}[\d]{3})$', re.IGNORECASE)
@allow_only_direct_message()
@ensure_event_exist()
@ensure_user_exist()
def add_car(message, user, active_event, model, plate_number, *args, **kwargs):
    UserRepository().add_car(user.user_id, model, plate_number)
    activity_log=ActivityLog(Action.ADDCAR.name, datetime.now(),active_event.event_id,user.user_id )
    ActivityLogRepository().log_action(activity_log)
    UserRepository().participate(user.user_id,active_event.event_id)
    message.send(Strings.CAR_REGISTERED)

@respond_to(r'^ls\s*$', re.IGNORECASE)
@allow_only_direct_message()
@ensure_event_exist()
@allowed_users(*ADMINS)
def list_participants(message, active_event):
    users = UserRepository().find_participants(active_event.event_id)
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
        message.send(Strings.NEW_EVENT_REGISTERED)
    else:
        message.send(Strings.EVENT_ALREADY_EXISTS)


@respond_to(r'^lshow\s*$', re.IGNORECASE)
@allow_only_direct_message()
@allowed_users(*ADMINS)
def get_events(message):
    event = EventRepository().find_active_event()
    if event is not None:      
       message.send(event.__repr__())
    else:
        message.send(Strings.NOT_VALID_EVENT)


@respond_to(r'^lclose\s*$', re.IGNORECASE)
@allow_only_direct_message()
@allowed_users(*ADMINS)
def delete_event(message):
    event = EventRepository().deactive_event()
    if event is True:
        message.send(Strings.EVENT_DEACTIVED)
    else:
        message.send(Strings.NOT_VALID_EVENT)
