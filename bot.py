# -*- coding: utf-8 -*-

import logging
import logging.handlers
import pathlib

from telegram.ext import Updater

import config
from blackjackbot import handlers, error_handler

logdir_path = pathlib.Path(__file__).parent.joinpath("logs").absolute()
logfile_path = logdir_path.joinpath("bot.log")

if not logdir_path.exists():
    logdir_path.mkdir()

logfile_handler = logging.handlers.WatchedFileHandler(logfile_path, "a", "utf-8")

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logging.getLogger("telegram").setLevel(logging.ERROR)
logging.getLogger("apscheduler").setLevel(logging.ERROR)

updater = Updater(token=config.BOT_TOKEN, use_context=True)

for handler in handlers:
    updater.dispatcher.add_handler(handler)

updater.dispatcher.add_error_handler(error_handler)

if config.USE_WEBHOOK:
    updater.start_webhook(listen=config.WEBHOOK_IP, port=config.WEBHOOK_PORT, url_path=config.BOT_TOKEN, cert=config.CERTPATH, webhook_url=config.WEBHOOK_URL)
    updater.bot.set_webhook(config.WEBHOOK_URL)
    logger.info("Started webhook server!")
else:
    updater.start_polling()
    logger.info("Started polling!")

logger.info("Bot started as @{}".format(updater.bot.username))
updater.idle()
