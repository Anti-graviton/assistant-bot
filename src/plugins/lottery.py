# -*- coding: utf-8 -*-

import re
from mmpy_bot.bot import respond_to
from mmpy_bot.utils import allow_only_direct_message, allowed_users
from .utils import ensure_user_exist, ensure_event_exist
from db.repository import UserRepository, EventRepository, \
    ActivityLogRepository
from db.models import ActivityLog, Car
from shared import Action
from settings.settings import ADMINS
from .messages import Messages


@respond_to(r'^reg\s*$', re.IGNORECASE)
@allow_only_direct_message()
@ensure_event_exist()
@ensure_user_exist()
def register(message, user, active_event):
    if user.car is None:
        return message.send(Messages.DEFINE_CAR)

    if not user.is_registered_in_event(active_event.event_id):
        UserRepository().participate(user.user_id, active_event.event_id)
        message.react(Messages.SUCCESSFUL_REGISTERATION)
    else:
        message.send(Messages.ALREADY_REGISTERED)


@respond_to(r'^unreg\s*$', re.IGNORECASE)
@allow_only_direct_message()
@ensure_event_exist()
@ensure_user_exist()
def withdraw(message, user, active_event):
    if user.is_registered_in_event(active_event.event_id):
        UserRepository().withdraw(user.user_id, active_event.event_id)
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

    active_event = EventRepository().find_active_event()
    if active_event is not None:
        UserRepository().withdraw(user.user_id, active_event.event_id)
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

    active_event = EventRepository().find_active_event()
    if active_event is not None:
        UserRepository().participate(user.user_id, active_event.event_id)
        return message.send(Messages.CAR_AND_PARTICIPATION_REGISTERED)

    message.send(Messages.CAR_REGISTERED)


@respond_to(r'^lls\s*$', re.IGNORECASE)
@allow_only_direct_message()
@ensure_event_exist()
@allowed_users(*ADMINS)
def list_participants(message, active_event):
    users = UserRepository().find_participants(active_event.event_id)
    usernames = '\n'.join(map(lambda u: "%s, %s" %
                              (u.username, u.car.plate_number), users))
    message.send(usernames)


@respond_to(r'^lsuser\s*$', re.IGNORECASE)
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
        # ToDo move duration calculation to add_event method
        duration = int(duration)
        if unit == "d":
            duration = 24 * duration
        EventRepository().add_event(duration)
        message.send(Messages.NEW_EVENT_REGISTERED)
    else:
        message.send(Messages.EVENT_ALREADY_EXISTS)


@respond_to(r'^lshow\s*$', re.IGNORECASE)
@allow_only_direct_message()
def get_events(message):
    event = EventRepository().find_active_event()
    if event is not None:
        message.send(event.__repr__())
    else:
        message.send(Messages.NOT_VALID_EVENT)


@respond_to(r'^lclose\s*$', re.IGNORECASE)
@allow_only_direct_message()
@allowed_users(*ADMINS)
def delete_event(message):
    event = EventRepository().deactive_event()
    if event is True:
        message.send(Messages.EVENT_DEACTIVED)
    else:
        message.send(Messages.NOT_VALID_EVENT)
