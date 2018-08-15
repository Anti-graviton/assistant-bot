#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler, RegexHandler
from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup,\
    ReplyKeyboardRemove, ParseMode
from db import UserRepository, User, BidsRepository, Bid
from secrets import bot_token, test_bot_token
from lottery import lottery_handler, withdraw_handler, players_handler
from cars import add_car_handler, delete_car_handler, manage_cars_handler
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


help_keyboard = InlineKeyboardMarkup([[
        # InlineKeyboardButton("مزایده پارکینگ", callback_data="help:bid"),
        # InlineKeyboardButton("شرکت‌کنندگان در مزایده", callback_data="help:bidders"),
        InlineKeyboardButton("قرعه‌کشی پارکینگ", callback_data="help:lottery"),
        InlineKeyboardButton("مدیریت ماشین‌ها", callback_data="help:mycars")
        # InlineKeyboardButton("ثبت نام", callback_data="help:register")
    ]])
help_message = """
چه کارهایی بلدم؟
/lottery شرکت در قرعه‌کشی پارکینگ
/mycars مدیریت ماشین‌ها
/withdraw انصراف از قرعه‌کشی

برای راهنمایی بیشتر رو دکمه‌های زیر بزن
"""


def start(bot, update):
    user_id = update.effective_user.id
    user = UserRepository().get_by_id(user_id)
    if user is not None:
        message = "با یکی از دستورات شروع کن %s جان.\nشاید /help شروع خوبی باشه" % user['first_name']
        update.message.reply_text(message)
    else:
        send_contact_button = KeyboardButton(text="من رو بشناس!", request_contact=True)
        reply_markup = ReplyKeyboardMarkup([[send_contact_button]])
        start_message = "سلام!\nمن دستیار فناپ+ هستم، و شما؟"
        update.message.reply_text(start_message, reply_markup=reply_markup)


def register(bot, update):
    contact = update.message.contact
    if contact.user_id != update.effective_user.id:
        return update.message.reply_text("زرنگ من، خودت باش!")

    user = User(contact.user_id, contact.phone_number, contact.first_name, contact.last_name)
    UserRepository().create(user)
    message = "با یکی از دستورات شروع کن %s جان.\nشاید /help شروع خوبی باشه" % user.first_name
    update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())


def uknown(bot, update):
    update.message.reply_text("چی میگی؟!\n\nکمک می‌خوای رو /help بزن.")


def help(bot, update):
    keyboard = help_keyboard
    message = help_message
    update.message.reply_text(message, reply_markup=keyboard)


def help_query(bot, update):
    query = update.callback_query
    keyword = query.data.split(':')[1]
    back_keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("« قبل", callback_data="help:back")
    ]])
    if keyword == "bid":
        keyboard = back_keyboard
        message = """
برای شرکت در مزایده‌ی پارکینگ، جلوی دستور، قیمت رو به *«هزار تومان»* بنویس. اینطوری:
/bid 30
/bid 12.5
/bid 999    
قیمت باید حداکثر ۳ رقم اصلی و ۲ رقم اعشار داشته باشه.
آخرین قیمتی که قبل از ساعت اتمام مزایده ثبت کنی، ملاک قرار می‌گیره.
اگر هم منصرف شدی کافیه قیمت 0 (صفر) رو ثبت کنی.

کاکو شیرازی! آمو شما /bid رو بزنی کافیه؛ خودم بقیه‌ش ازت می‌پرسم.

یادت هم باشه قیمت به *«هزار تومن»* ثبت میشه! بدبخت نکنی خودتو!
    """
    elif keyword == "bidders":
        message = "بگو /bidders تا بهت بگم کیا تو مزایده شرکت کردن.\nضمنا K.I.A رو جمع نبستم!"
        keyboard = back_keyboard
    elif keyword == "back":
        message = help_message
        keyboard = help_keyboard
    elif keyword == "register":
        keyboard = back_keyboard
        message = "\nبرای ثبت نام کافیه contactت رو برام بفرستی." \
                  "/start رو بزن، بقیه‌اش با من!"
    elif keyword == "lottery":
        keyboard = back_keyboard
        message = """
برای شرکت در قرعه‌کشی پارکینگ، باید اول دست کم یک شماره پلاک و مدل ماشین ثبت کرده باشی. برای این کار از /mycars کمک بگیر. 
اگر مطمئنی که بیشتر از ۶۰درصد روزها خودت از پارکینگ استفاده می‌کنی، روی /lottery بزن تا مراحل ثبت‌نام انجام بشه.

اگر بعد ثبت‌نام منصرف شدی، از دستور /withdraw استفاده کن.
وسط مراحل ثبت‌نام هم بی‌خیال شدی، /cancel بزن.

اگر هم کنجکاوی بدونی چه کسانی در قرعه‌کشی ثبت‌نام کردند، از دستور /players کمک بگیر.
"""
    elif keyword == "mycars":
        keyboard = back_keyboard
        message = """
برای اضافه‌کردن ماشین باید شماره پلاک و مدل ماشین‌ت رو به من بدی.
مدل ماشین رو برای چی می‌خوایم؟ خب باید بدونیم کدوم پارکینگ رو به کی بدیم!

اگر بخوای پارکینگ‌ت رو با کسی شریک بشی، می‌تونی دو تا ماشین معرفی کنی.
اگر اطلاعات ماشین رو اشتباه وارد کردی نگران نباش، می‌تونی اطلاعات ماشین رو حذف کنی و دوباره ثبت‌نام کنی.
"""
    else:
        keyboard = back_keyboard
        message = "همچین راهنمایی نداریم‌"

    bot.edit_message_text(text=message,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          reply_markup=keyboard,
                          parse_mode=ParseMode.MARKDOWN)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    updater = Updater(token=bot_token)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    register_handler = MessageHandler(Filters.contact, register)
    unknown_handler = MessageHandler(Filters.text, uknown)
    help_query_handler = CallbackQueryHandler(help_query, pattern=r'help:[\w]+')

    dispatcher.add_handler(start_handler)

    # Bid Handlers
    # dispatcher.add_handler(bid_handler)
    # dispatcher.add_handler(bidders_handler)

    # Lottery Handlers
    dispatcher.add_handler(lottery_handler)
    dispatcher.add_handler(withdraw_handler)
    dispatcher.add_handler(players_handler)

    # Cars Handlers
    dispatcher.add_handler(add_car_handler)
    dispatcher.add_handler(delete_car_handler)
    dispatcher.add_handler(manage_cars_handler)

    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(register_handler)
    dispatcher.add_handler(unknown_handler)
    dispatcher.add_handler(help_query_handler)

    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
