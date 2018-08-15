from telegram.ext import CommandHandler
from db import UserRepository, LotsRepository, Lot


def lottery(bot, update):
    user_id = update.effective_user.id
    user = UserRepository().get_by_id(user_id)
    if user is None:
        return update.message.reply_text("""یادم نمیاد کی هستی :( لطفا از اول بیا تو! /start""")

    if 'cars' not in user or len(user['cars']) == 0:
        return update.message.reply_text("""حداقل باید یک ماشین معرفی کنی. از دستور /mycars کمک بگیر""")

    lot = LotsRepository().get_by_user(user_id)

    if lot is None:
        LotsRepository().create(Lot(user_id))

    update.message.reply_text("ثبت نام انجام شد")


def players(bot, update):
    lot_players = LotsRepository().get_players()
    if not len(lot_players) == 0:
        players_names = map(lambda b: b.name(), lot_players)
        message = "\n".join(players_names)
        update.message.reply_text(message)
    else:
        update.message.reply_text("گشتم نبود، نگرد، نیست!")


def withdraw(bot, update):
    user_id = update.effective_user.id
    LotsRepository().delete_by_user(user_id)
    update.message.reply_text("انصراف از قرعه‌کشی ثبت شد.")


withdraw_handler = CommandHandler('withdraw', withdraw)
players_handler = CommandHandler('players', players)
lottery_handler = CommandHandler('lottery', lottery)
