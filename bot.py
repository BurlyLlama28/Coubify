#!/usr/bin/env python3

import logging
from coub import Coub

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


# Telegram API secret token
TOKEN = "2117949123:AAGotS7kIWxxqKcAm695lHY773cdZ2cNOOU"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
coub = Coub()


def start_message(update, context):
    update.message.reply_text('Hi! I download coubs. Try /help to learn more.')


def help_message(update, context):
    update.message.reply_text("""Send me link to a coub""")


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def find_coub(update, context):

    link = update.message.text
    update.message.reply_text("Detected coub, downloading image...")
    try:
        coub.download_video(link, "./coubs/")
        update.message.reply_text("Coub has been found!")
    except:
        update.message.reply_text("Ohh, coub has'nt been found")


def main():
    # Updater is a simple Bot frontend, enough for our purposes (for now)
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_message))
    dp.add_handler(CommandHandler("help", help_message))
    dp.add_handler(MessageHandler(Filters.text, find_coub))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()