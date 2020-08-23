# -*- coding: utf-8 -*-
from telegram.ext import CommandHandler, CallbackQueryHandler

from blackjackbot.bot.commands import start_cmd, stop_cmd, stats_cmd, language_cmd, \
    hit_callback, stand_callback, join_callback, start_callback, newgame_callback, language_callback, \
    reload_languages_cmd, users_cmd

start_command_handler = CommandHandler("start", start_cmd)
stop_command_handler = CommandHandler("stop", stop_cmd)
language_command_handler = CommandHandler("language", language_cmd)
stats_command_handler = CommandHandler("stats", stats_cmd)
reload_lang_command_handler = CommandHandler("reload_lang", reload_languages_cmd)
users_command_handler = CommandHandler("users", users_cmd)

hit_callback_handler = CallbackQueryHandler(hit_callback, pattern=r"^hit$")
stand_callback_handler = CallbackQueryHandler(stand_callback, pattern=r"^stand$")
join_callback_handler = CallbackQueryHandler(join_callback, pattern=r"^join$")
start_callback_handler = CallbackQueryHandler(start_callback, pattern=r"^start$")
newgame_callback_handler = CallbackQueryHandler(newgame_callback, pattern=r"^newgame$")
language_callback_handler = CallbackQueryHandler(language_callback, pattern=r"lang_[a-zA-Z\_]+")

handlers = [start_command_handler, stop_command_handler, join_callback_handler, hit_callback_handler, stand_callback_handler, start_callback_handler,
            language_command_handler, stats_command_handler, newgame_callback_handler, reload_lang_command_handler, language_callback_handler,
            users_command_handler]

__all__ = ['handlers']
