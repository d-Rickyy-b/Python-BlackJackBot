# -*- coding: utf-8 -*-

import logging

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

import config
from blackjackbot.bot.commands import start_cmd, stop_cmd, stats_cmd, language_cmd, hit_callback, stand_callback, join_callback, start_callback, \
    newgame_callback

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logging.getLogger("telegram").setLevel(logging.ERROR)

updater = Updater(token=config.BOT_TOKEN, use_context=True)

start_command_handler = CommandHandler("start", start_cmd)
stop_command_handler = CommandHandler("stop", stop_cmd)
language_command_handler = CommandHandler("language", language_cmd)
stats_command_handler = CommandHandler("stats", stats_cmd)

hit_callback_handler = CallbackQueryHandler(hit_callback, pattern=r"^hit$")
stand_callback_handler = CallbackQueryHandler(stand_callback, pattern=r"^stand$")
join_callback_handler = CallbackQueryHandler(join_callback, pattern=r"^join$")
start_callback_handler = CallbackQueryHandler(start_callback, pattern=r"^start$")
newgame_callback_handler = CallbackQueryHandler(newgame_callback, pattern=r"^newgame$")

handlers = [start_command_handler, stop_command_handler, join_callback_handler, hit_callback_handler, stand_callback_handler, start_callback_handler,
            language_command_handler, stats_command_handler, newgame_callback_handler]

# TODO change lang commands

for handler in handlers:
    updater.dispatcher.add_handler(handler)

if config.USE_WEBHOOK:
    updater.start_webhook(listen="127.0.0.1", port=config.WEBHOOK_PORT, url_path=config.BOT_TOKEN, cert=config.CERTPATH, webhook_url=config.WEBHOOK_URL)
    updater.bot.set_webhook(config.WEBHOOK_URL)
    logger.info("Started webhook server!")
else:
    updater.start_polling()
    logger.info("Started polling!")

logger.info("Bot started as @{}".format(updater.bot.username))
updater.idle()
