from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
from telegram import ParseMode
from .db import UserRepository, BidsRepository, Bid


class States:
    BID = 0
    END = -1


def bidding(bot, update, args):
    user_id = update.effective_user.id
    user = UserRepository().get_by_id(user_id)
    if user is None:
        update.message.reply_text("""یاد نمیاد کی هستی :( لطفا از اول بیا تو! /start""")
        return States.END

    if not len(args) == 1:
        message = "قیمت مد نظرت؟ (به *هزار تومان*)"
        update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
        return States.BID
    else:
        update.message.text = args[0]
        return commit_bid(bot, update)


def unknown_bid(bot, update):
    update.message.reply_text("""
الآن باید قیمت مد نظرت رو بگی.

قیمت باید حداکثر ۳ رقم اصلی و ۲ رقم اعشار داشته باشه.
یادت هم باشه قیمت به *هزار تومن* ثبت میشه! بدبخت نکنی خودتو!

اگر هم کلا بی‌خیال شدی بزن /cancel""", parse_mode=ParseMode.MARKDOWN)


def cancel(bot, update):
    return States.END


def commit_bid(bot, update):
    price = update.message.text
    user_id = update.effective_user.id
    bid = None
    try:
        bid = Bid(user_id, price)
    except ValueError:
        bot.send_message(update.message.chat_id,
                         "قیمت باید حداکثر ۳ رقم اصلی و ۲ رقم اعشار داشته باشه.\n"
                         "یادت هم باشه قیمت به *هزار تومن* ثبت میشه! بدبخت نکنی خودتو!",
                         parse_mode=ParseMode.MARKDOWN)
        return States.BID

    BidsRepository().create(bid)
    message = "قیمت پیشنهادی شما ({:.2f} هزار تومان) ذخیره شد.".format(float(price))
    update.message.reply_text(message)
    return States.END


def list_bidders(bot, update):
    bidders = BidsRepository().get_bidders()
    if not len(bidders) == 0:
        bidders_names = map(lambda b: b.name(), bidders)
        message = "\n".join(bidders_names)
        update.message.reply_text(message)
    else:
        update.message.reply_text("گشتم نبود، نگرد، نیست!")


bidders_handler = CommandHandler('bidders', list_bidders)
bid_handler = ConversationHandler(
    entry_points=[CommandHandler('bid', bidding, pass_args=True)],
    states={
        States.BID: [
            RegexHandler(Bid.price_pattern, commit_bid),
            CommandHandler('cancel', cancel)
        ]
    },
    fallbacks=[MessageHandler(Filters.all, unknown_bid)]
)
