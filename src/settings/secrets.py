import yaml
from os import path

base_dir = path.dirname(__file__)
__secrets = yaml.load(open(path.join(base_dir, './secrets.yml'), 'r'))

email = __secrets['email']
password = __secrets['password']
