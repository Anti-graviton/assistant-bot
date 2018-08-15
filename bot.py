from mattermostdriver import Driver
from tools import utils, driver


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


if __name__ == '__main__':
    main()
