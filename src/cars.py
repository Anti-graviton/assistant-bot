from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from db import UserRepository
import re


CAR_NUM_PATTERN = r'(ایران|ايران)[\s]*[\d]{2} [\d]{2}[\w]{1}[\d]{3}'


class AddCarStates:
    End = -1
    CarNo, CarModel = range(0, 2)


def manage_cars(bot, update):
    user_id = update.effective_user.id
    user = UserRepository().get_by_id(user_id)
    if user is None:
        return update.message.reply_text("""یادم نمیاد کی هستی :( لطفا از اول بیا تو! /start""")

    cars = []
    if 'cars' in user:
        cars = user['cars']

    cars_buttons = []
    for car in cars:
        cars_buttons.append(InlineKeyboardButton("حذف %s" % car['car_model'], callback_data="cars:remove:%s" % car['id']))
    keyboard = InlineKeyboardMarkup([cars_buttons, [InlineKeyboardButton("افزودن ماشین", callback_data="cars:add")]])
    message = """
از منوی زیر برای حذف یا اضافه کردن ماشین استفاده کن.
برای تغییر مشخصات یک ماشین، باید اول حذف و دوباره اضافه‌اش کنی.
"""
    update.message.reply_text(message, reply_markup=keyboard)


def delete_car(bot, update):
    query = update.callback_query
    car_id = query.data.split(':')[2]
    user_id = update.effective_user.id
    UserRepository().delete_user_car(user_id, car_id)
    bot.send_message(chat_id=user_id, text="اطلاعات ماشین شما حذف شد. برای ثبت مجدد از منوی /mycars استفاده کنید")


def add_car(bot, update):
    user_id = update.effective_user.id
    user = UserRepository().get_by_id(user_id)
    if user is None:
        bot.send_message(chat_id=user_id, text="""یادم نمیاد کی هستی :( لطفا از اول بیا تو! /start""")
        return AddCarStates.End

    if 'cars' in user and len(user['cars']) > 1:
        bot.send_message(chat_id=user_id, text="بیشتر از ۲ تا ماشین نمی‌تونی معرفی کنی.")
        return AddCarStates.End

    if ('car_num' not in user) or (user['car_num'] is None):
        message = """پلاک ماشینت؟
اینطوری بنویس:
ایران۹۹ ۹۹ب۹۹۹

حواست به فاصله‌ی بین دو قسمت باشه.
"""
        bot.send_message(chat_id=user_id, text=message)
        return AddCarStates.CarNo

    if ('car_model' not in user) or (user['car_model'] is None):
        message = "مدل ماشین‌ت چیه؟ (مثل: پژو۲۰۶، هیوندا i20، ...)"
        bot.send_message(chat_id=user_id, text=message)
        return AddCarStates.CarModel

    save_car(bot, user_id)
    return AddCarStates.End


def save_car_num(bot, update):
    car_num = update.message.text
    user_id = update.effective_user.id
    valid_car_num = re.match(CAR_NUM_PATTERN, car_num)
    if not valid_car_num:
        update.message.reply_text("شماره پلاک صحیح نیست! دوباره امتحان کن")
        return None
    UserRepository().stash_car_num(user_id, car_num)

    message = "مدل ماشین‌ت چیه؟ (مثل: پژو۲۰۶، هیوندا i20، ...)"
    update.message.reply_text(message)
    return AddCarStates.CarModel


def save_car_model(bot, update):
    car_model = update.message.text
    user_id = update.effective_user.id
    UserRepository().stash_car_model(user_id, car_model)
    save_car(bot, user_id)
    return AddCarStates.End


def save_car(bot, user_id):
    UserRepository().save_car(user_id)
    bot.send_message(chat_id=user_id, text="اطلاعات ماشین با موفقیت ذخیره شد")


def unknown(bot, update):
    update.message.reply_text("نمی‌فهمم چی می‌گی!")


def cancel(bot, update):
    user_id = update.effective_user.id
    UserRepository().flush_car_stash(user_id)
    update.message.reply_text("باشه، بی‌خیال می‌شم!")
    return AddCarStates.End


add_car_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(add_car, pattern=r'cars:add')],
    states={
        AddCarStates.CarNo: [
            RegexHandler(CAR_NUM_PATTERN, save_car_num),
            CommandHandler('cancel', cancel)
        ],
        AddCarStates.CarModel: [
            MessageHandler(Filters.text, save_car_model),
            CommandHandler('cancel', cancel)
        ]
    },
    fallbacks=[
        MessageHandler(Filters.text, unknown)
    ],
    allow_reentry=True
)
delete_car_handler = CallbackQueryHandler(delete_car, pattern=r'cars:remove:[\w\d]+')
manage_cars_handler = CommandHandler('mycars', manage_cars)
