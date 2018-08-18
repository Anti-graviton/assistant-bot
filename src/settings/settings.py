import os

BOT_URL = 'http://172.16.30.11:8065/api/v4'  # with 'http://' and with '/api/v3' path
BOT_LOGIN = email
BOT_PASSWORD = password
BOT_TEAM = 'ITTest'
BOT_TOKEN = None  # or '<bot-personal-access-token>' if you have set bot personal access token.
SSL_VERIFY = False
DEBUG = False
PLUGINS = ['plugins']

os.environ['MATTERMOST_BOT_SETTINGS_MODULE'] = 'settings.settings'
