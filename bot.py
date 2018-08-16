from mattermostdriver import Driver
from tools import utils, driver
import asyncio
import json

PLATE_NUMBER_PATTERN = r'(ایران|ايران)[\s]*[\d]{2} [\d]{2}[\w]{1}[\d]{3}'


def main():

    print("Authenticating...")
    driver.login()
    driver.users.get_user('me')
    print("Successfully authenticated.")

    print("Retrieving Coffee Buddies participants...")
    team_name = 'ITTest'
    channel_name = 'town-square'
    members = utils.get_channel_members(driver, team_name, channel_name)
    print("Successfully retrieved Coffee Buddies participants.")

    print("Preparing participants database...")
    utils.create_users(members)

    driver.init_websocket(sample_handler)


@asyncio.coroutine
def sample_handler(message_string):

    message = json.loads(message_string)

    bot = driver.users.get_user('me')

    if 'event' not in message:
        return

    if message['event'] != 'posted':
        return

    if 'data' not in message:
        return

    team = driver.teams.get_team_by_name('ITTest')
    channel = driver.channels.get_channel_by_name(
        team['id'], message['data']['channel_name'])

    if message['data']['channel_type'] != 'D':
        return

    post = json.loads(message['data']['post'])

    if post['user_id'] == bot['id']:
        return

    message_content = post['message'].lower()

    if message_content == 'register':
        user = driver.users.get_user(post['user_id'])
        register(channel, user)
        return

    send_message(channel, 'sorry, I did not understand your command')


def register(channel, user):
    send_message(channel, 'we will do something here later')
    pass


def send_message(channel, message):
    driver.posts.create_post(options={
        'channel_id': channel['id'],
        'message': message
    })


if __name__ == '__main__':
    main()
