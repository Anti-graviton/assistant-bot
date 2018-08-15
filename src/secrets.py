import yaml
from os import path

dir = path.dirname(__file__)

__secrets = yaml.load(open(path.join(dir, './secrets.yml'), 'r'))

app_id = __secrets['app-id']
bot_token = __secrets['bot-token']
test_bot_token = __secrets['test-bot-token']