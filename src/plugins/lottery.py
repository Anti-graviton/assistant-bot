# -*- coding: utf-8 -*-

import re
from datetime import datetime
from mmpy_bot.bot import respond_to
from mmpy_bot.utils import allow_only_direct_message, allowed_users
from .utils import ensure_user_exist, ensure_event_exist
from db.repository import UserRepository, EventRepository, \
    ActivityLogRepository
from db.models import ActivityLog, Car
from shared import Action, EventType
from settings.settings import ADMINS
from .messages import Messages


@respond_to(r'^reg(\s+\w+|)\s*$', re.IGNORECASE)
@allow_only_direct_message()
@ensure_event_exist()
@ensure_user_exist()
def register(message, user, event):
    if event.event_type is EventType.LOTTERY.value and user.car is None:
        return message.send(Messages.DEFINE_CAR)
    elif event.event_type is EventType.PES.value:
        pass  # ToDo extract params after event_type in message

    if not user.is_registered_in_event(event.event_id):
        UserRepository().participate(user.user_id, event.event_id)
        message.send(Messages.SUCCESSFUL_REGISTERATION)
    else:
        message.send(Messages.ALREADY_REGISTERED)


@respond_to(r'^unreg(\s+\w+|)\s*$', re.IGNORECASE)
@allow_only_direct_message()
@ensure_event_exist()
@ensure_user_exist()
def withdraw(message, user, event):
    if user.is_registered_in_event(event.event_id):
        UserRepository().withdraw(user.user_id, event.event_id)
        message.send(Messages.UNDO_REGISTERATION)
    else:
        message.send(Messages.NOT_YET_REGISTERED)


@respond_to(r'^mycar\s*$', re.IGNORECASE)
@allow_only_direct_message()
@ensure_user_exist()
def mycar(message, user):
    message.send(user.car.__repr__()
                 if user.car is not None else Messages.NO_CAR_EXISTS)


@respond_to(r'^rmcar\s*$', re.IGNORECASE)
@allow_only_direct_message()
@ensure_user_exist()
def remove_car(message, user):
    if user.car is None:
        return message.send(Messages.NO_CAR_EXISTS)

    UserRepository().remove_car(user.user_id)

    activity_details = {"car": user.car}
    activity_log = ActivityLog(user.user_id, Action.RMCAR.name,
                               details=activity_details)
    ActivityLogRepository().log_action(activity_log)

    active_lottery = \
        EventRepository().find_active_event_by_type(EventType.LOTTERY.value)
    if active_lottery is not None:
        UserRepository().withdraw(user.user_id, active_lottery.event_id)
        return message.send(Messages.CAR_REMOVED_AND_WITHDRAWED)

    message.send(Messages.CAR_REMOVED)


@respond_to(r'^addcar ([\w\s\d]+) - ((?:ایران|ايران|iran|ir)[\s]*[\d]{2} '
            r'[\d]{2}[\w]{1}[\d]{3})$', re.IGNORECASE)
@allow_only_direct_message()
@ensure_user_exist()
def add_car(message, user, model, plate_number, *args, **kwargs):
    UserRepository().add_car(user.user_id, model, plate_number)

    activity_details = {"car": Car(plate_number, model)}
    activity_log = ActivityLog(user.user_id, Action.ADDCAR.name,
                               details=activity_details)
    ActivityLogRepository().log_action(activity_log)

    active_lottery = \
        EventRepository().find_active_event_by_type(EventType.LOTTERY.value)
    if active_lottery is not None:
        UserRepository().participate(user.user_id, active_lottery.event_id)
        return message.send(Messages.CAR_AND_PARTICIPATION_REGISTERED)

    message.send(Messages.CAR_REGISTERED)


@respond_to(r'^lls\s*$', re.IGNORECASE)
@allow_only_direct_message()
@allowed_users(*ADMINS)
def list_participants(message):
    latest_event = EventRepository().find_latest_event()
    if latest_event is None:
        return message.send(Messages.NO_EVENT_EXISTS)

    users = UserRepository().find_participants(latest_event.event_id)
    usernames = '\n'.join(map(lambda u: "%s, %s" %
                              (u.username, u.car.__repr__()), users))
    message.send(usernames)


@respond_to(r'^lsuser\s*$', re.IGNORECASE)
@allow_only_direct_message()
@allowed_users(*ADMINS)
def list_users(message):
    users = UserRepository().get_users()
    usernames = '\n'.join(map(lambda u: u.username, users))
    message.send(usernames)


@respond_to(r'^open\s+(\d{1,2})(h|d)(\s+\w+|)(\s+\w+|)\s*$', re.IGNORECASE)
@allow_only_direct_message()
@allowed_users(*ADMINS)
def add_event(message, duration, unit, event_type, event_id=None):
    active_event = EventRepository().find_active_event_by_type(event_type)
    if active_event is None:
        # ToDo move duration calculation to add_event method
        duration = int(duration)
        if unit == "d":
            duration = 24 * duration
        if event_id is None:
            now = datetime.now()
            event_id = "{}{}{}".format(event_type, now.year, now.month)

        EventRepository().add_event(event_type, event_id, duration)
        message.send(Messages.NEW_EVENT_REGISTERED)
    else:
        message.send(Messages.EVENT_ALREADY_EXISTS)


@respond_to(r'^lsevent\s*$', re.IGNORECASE)
@allow_only_direct_message()
def get_events(message):
    events = EventRepository().find_active_events()
    if len(events) is not 0:
        msg = '\n'.join(map(lambda e: e.__repr__(), events))
        message.send(msg)
    else:
        message.send(Messages.NOT_VALID_EVENT)


@respond_to(r'^close(\s+\w+|)\s*$', re.IGNORECASE)
@allow_only_direct_message()
@allowed_users(*ADMINS)
def delete_event(message, event_type):
    event = EventRepository().deactive_event_by_type(event_type)
    if event is True:
        message.send(Messages.EVENT_DEACTIVED)
    else:
        message.send(Messages.NOT_VALID_EVENT)
