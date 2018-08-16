from mattermostdriver import Driver
from tools import utils, driver, user_collection, models
import asyncio
import json
import re
from datetime import datetime

PLATE_NUMBER_PATTERN = r'(ایران|ايران)[\s]*[\d]{2} [\d]{2}[\w]{1}[\d]{3}'


def main():

    print("Authenticating...")
    driver.login()
    driver.users.get_user('me')
    print("Successfully authenticated.")

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

    if message_content.startswith('register'):  # register model plate_number
        items = message_content.split()

        if len(items) != 4:
            send_message(
                channel, "الگویی که وارد کردی درست نیست \r\n `مثال: register پژو ایران۱۱ ۱۱ب۱۱۱`")
            return

        command = items[0]
        model = items[1]
        plate_number = items[2]+" "+items[3]

        user = driver.users.get_user(post['user_id'])

        register(channel, user, model, plate_number)
        return

    send_message(channel, 'ببخشید، متوجه نشدم چی گفتی')


def register(channel, user, model, plate_number):

    valid_car_num = re.match(PLATE_NUMBER_PATTERN, plate_number)

    if not valid_car_num:
        send_message(channel, "شماره پلاک صحیح نیست! دوباره امتحان کن")
        return

    send_message(channel, '''
                            مدل ماشین: {}
                            پلاک ماشین: {}
                            '''.format(
        model, plate_number))

    found_user = user_collection.find_one(filter={'user_id': user['id']})

    if found_user == None:
        new_user = models.User(user['id'],
                               user['username'],
                               user['nickname'],
                               user['first_name'],
                               user['last_name'],
                               user['email'])

        new_car = models.Car(plate_number, model)

        new_user.cars.append(new_car)

        user_collection.insert_one(new_user.__dict__)
        return


def send_message(channel, message):
    driver.posts.create_post(options={
        'channel_id': channel['id'],
        'message': message
    })


if __name__ == '__main__':
    main()
