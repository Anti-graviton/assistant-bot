import yaml
from os import path

dir = path.dirname(__file__)
__secrets = yaml.load(open(path.join(dir, './secrets.yml'), 'r'))

email = __secrets['email']
password = __secrets['password']