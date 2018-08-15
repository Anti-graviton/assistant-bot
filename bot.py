from mattermostdriver import Driver


def main():
    print("Creating Mattermost Driver...")
    driver_options = {
        'url': '172.16.30.11',
        'login_id': 'kia',
        'password': '123456',
        'port': 8065,
        'scheme': 'http'
    }
    driver = Driver(driver_options)

    print("Authenticating...")
    driver.login()
    driver.users.get_user('me')
    print("Successfully authenticated.")


if __name__ == '__main__':
    main()
