from mattermostdriver import Driver

foo = Driver({
    # """
    # Required options

    # Instead of the login/password, you can also use a personal access token.
    # If you have a token, you don't need to pass login/pass.
    # """

    'url': 'fanype.fanap.plus',
    'login_id': 'kia@fanap.plus',
    'password': 'imsherlocked',
    # 'token': 'YourPersonalAccessToken',
    'scheme': 'https',
    'port': 443,
    'basepath': '/api/v4',
    'verify': True,
    # 'mfa_token': 'YourMFAToken'

    # """
    # Optional options

    # These options already have useful defaults or are just not needed in every case.
    # In most cases, you won't need to modify these, especially the basepath.
    # If you can only use a self signed/insecure certificate, you should set
    # verify to False. Please double check this if you have any errors while
    # using a self signed certificate!
    # """

    # 'scheme': 'https',
    # 'port': 8065,
    # 'basepath': '/api/v4',
    # 'verify': True,
    # 'mfa_token': 'YourMFAToken'

    # """
    # If for some reasons you get regular timeouts after a while, try to decrease
    # this value. The websocket will ping the server in this interval to keep the connection
    # alive.
    # If you have access to your server configuration, you can of course increase the timeout
    # there.
    # """

    'timeout': 30,

    # """
    # Setting debug to True, will activate a very verbose logging.
    # This also activates the logging for the requests package,
    # so you can see every request you send.

    # Be careful. This SHOULD NOT be active in production, because this logs a lot!
    # Even the password for your account when doing driver.login()!
    # """
    'debug': True
})

login_result = foo.login()

print(login_result)
