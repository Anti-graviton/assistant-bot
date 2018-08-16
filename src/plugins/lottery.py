import re
from mmpy_bot.bot import respond_to
from mmpy_bot.utils import allow_only_direct_message

@respond_to('reg', re.IGNORECASE)
@allow_only_direct_message() 
def register(message):
    message.send("Register")