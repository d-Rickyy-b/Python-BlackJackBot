# -*- coding: utf-8 -*-
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from blackjackbot.errors import error_handler

from blackjackbot.commands import game, admin, settings, util

# User commands
start_command_handler = CommandHandler("start", game.start_cmd)
stop_command_handler = CommandHandler("stop", game.stop_cmd)
language_command_handler = CommandHandler("language", settings.language_cmd)
stats_command_handler = CommandHandler("stats", util.stats_cmd)
comment_command_handler = CommandHandler("comment", util.comment_cmd)
comment_text_command_handler = MessageHandler(Filters.text & ~(Filters.forwarded | Filters.command), util.comment_text)

# Admin methods
reload_lang_command_handler = CommandHandler("reload_lang", admin.reload_languages_cmd)
users_command_handler = CommandHandler("users", admin.users_cmd)
answer_command_handler = CommandHandler("answer", admin.answer_comment_cmd, Filters.reply)

# Callback handlers
hit_callback_handler = CallbackQueryHandler(game.hit_callback, pattern=r"^hit$")
stand_callback_handler = CallbackQueryHandler(game.stand_callback, pattern=r"^stand$")
join_callback_handler = CallbackQueryHandler(game.join_callback, pattern=r"^join$")
start_callback_handler = CallbackQueryHandler(game.start_callback, pattern=r"^start$")
newgame_callback_handler = CallbackQueryHandler(game.newgame_callback, pattern=r"^newgame$")
language_callback_handler = CallbackQueryHandler(settings.language_callback, pattern=r"^lang_([a-z]{2}(?:-[a-z]{2})?)$")

handlers = [start_command_handler, stop_command_handler, join_callback_handler, hit_callback_handler, stand_callback_handler, start_callback_handler,
            language_command_handler, stats_command_handler, newgame_callback_handler, reload_lang_command_handler, language_callback_handler,
            users_command_handler, comment_command_handler, comment_text_command_handler, answer_command_handler]

__all__ = ['handlers', 'error_handler']
