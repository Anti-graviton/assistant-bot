import random
import pymongo
from pymongo import MongoClient
from . import db, user_collection, driver
from . import models
from datetime import datetime
import json


def get_channel(driver, team_name, channel_name):
    """
    Retrieve a channel given a team and channel name.
    Returns the JSON response from the Mattermost API.
    """
    response = driver.channels.get_channel_by_name_and_team_name(
        team_name, channel_name)
    return response


def get_channel_members(driver, team_name, channel_name):
    """
    Retrieve all of the members from a channel given a team and channel name.
    Returns a list of user IDs sorted alphabetically.
    """
    channel = get_channel(driver, team_name, channel_name)
    channel_id = channel['id']

    # By default, the Mattermost API will return only 60 members. Set this to
    # an amount that is at least the number of members in the channel to get
    # all members
    params = {
        'per_page': '10000'
    }
    response = driver.channels.get_channel_members(channel_id, params=params)

    bot = driver.users.get_user('me')
    bot_id = bot['id']

    # Return all of the user IDs excluding the bot's user ID (don't want to
    # count the bot as a user in pairings)
    members = [
        member['user_id'] for member in response if (
            member['user_id'] != bot_id)]

    # Sort the member list alphabetically so that when we create pairs in the
    # database using the list, we won't create duplicate pairs (A <-> B is the
    # same as B <-> A)
    members.sort()

    return members


def create_users(members):

    #     """
    #     Create a User object in the database representing each Mattermost user
    #     given a list of current users in the channel.
    #     """
    #     # Set only the users that exist in the input list as active

    team = driver.teams.get_team_by_name('ITTest')
    channel = driver.channels.get_channel_by_name(
        team['id'], 'town-square')

    mattermost_users = driver.users.get_users(params={
        'in_team': team['id'],
        'in_channel': channel['id']
    })

    users = user_collection.find()
    existing_user_ids = list(map(lambda x: x['user_id'], users))

    for mattermost_user in mattermost_users:
        if mattermost_user['id'] in existing_user_ids:
            continue
        user = models.User()
        user.user_id = mattermost_user['id']
        user.active = True
        user.date_created = datetime.now()
        user.username = mattermost_user['username']
        user.nickname = mattermost_user['nickname']
        user.first_name = mattermost_user['first_name']
        user.last_name = mattermost_user['last_name']
        user.email = mattermost_user['email']

        user_collection.insert_one(user.__dict__)


def send_message(username, message):
    bot = driver.users.get_user('me')
    bot_id = bot['id']

    target = user_collection.find_one(filter={'username': username})

    direct_channel = driver.channels.create_direct_message_channel(
        [bot_id, target['user_id']])

    driver.posts.create_post(options={
        'channel_id': direct_channel['id'],
        'message': message
    })

