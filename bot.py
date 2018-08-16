from mattermostdriver import Driver
from tools import utils, driver
import asyncio
import json


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

    if 'event' not in message:
        # print('passing cuz event was not in message')
        return

    if message['event'] != 'posted':
        # print('passing cuz event was not "posted"')
        return
        
    print(message)

if __name__ == '__main__':
    main()
