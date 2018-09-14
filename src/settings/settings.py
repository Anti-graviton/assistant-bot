import os
from .secrets import email, password

BOT_URL = 'http://172.16.30.11:8065/api/v4'
BOT_LOGIN = email
BOT_PASSWORD = password
BOT_TEAM = 'ITTest'
BOT_TOKEN = None
SSL_VERIFY = False
DEBUG = False
PLUGINS = ['plugins']
ADMINS = ['hossein.t', 'abolfazl']
DEFAULT_REPLY = '''
### نمی‌فهمم چی می‌گی!
من یه ربات دون‌پایه‌ام! لطفا عین همین شیوه‌ای که این پایین نوشته با من صحبت کن.

|command|معنی|
|------|-----------------|
|reg  ‌ |‌ثبت‌نام در قرعه‌کشی|
|unreg |انصراف از قرعه‌کشی|
|addcar| اضافه کردن ماشین|
|rmcar |حذف ماشین        |
|mycar |اطلاعات ماشین     |

برای اضافه کردن ماشین یکم باید تمرکز کنی.
بعد از دستور باید دو تا مقدار بهم بدی که با خط تیره (-) از هم جدا شده‌ان.
اولی مدل ماشین و دومی شماره پلاکه.
مثال:
addcar pride - iran99 99b999
addcar پراید - ایران۹۹ ۹۹ب۹۹۹
'''

os.environ['MATTERMOST_BOT_SETTINGS_MODULE'] = 'settings.settings'
