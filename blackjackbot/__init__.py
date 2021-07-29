# -*- coding: utf-8 -*-
from telegram import Update
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, Filters

from blackjackbot.commands import game, admin, settings, util
from blackjackbot.errors import error_handler
from util import BannedUserHandler, banned_user_callback

# Banned users
banned_user_handler = BannedUserHandler(callback=banned_user_callback, type=Update)

# User commands
start_command_handler = CommandHandler("start", game.start_cmd)
stop_command_handler = CommandHandler("stop", game.stop_cmd)
language_command_handler = CommandHandler("language", settings.language_cmd)
stats_command_handler = CommandHandler("stats", util.stats_cmd)
resetstats_command_handler = CommandHandler("resetstats", util.reset_stats_cmd)
comment_command_handler = CommandHandler("comment", util.comment_cmd)
comment_text_command_handler = MessageHandler(Filters.text & ~(Filters.forwarded | Filters.command), util.comment_text)

# Admin methods
reload_lang_command_handler = CommandHandler("reload_lang", admin.reload_languages_cmd)
users_command_handler = CommandHandler("users", admin.users_cmd)
answer_command_handler = CommandHandler("answer", admin.answer_comment_cmd, Filters.reply)
kill_command_handler = CommandHandler("kill", admin.kill_game_cmd, Filters.text)
ban_command_handler = CommandHandler("ban", admin.ban_user_cmd, pass_args=True)
unban_command_handler = CommandHandler("unban", admin.unban_user_cmd, pass_args=True)
bans_command_handler = CommandHandler("bans", admin.bans_cmd)

# Callback handlers
hit_callback_handler = CallbackQueryHandler(game.hit_callback, pattern=r"^hit_[0-9]{7}$")
stand_callback_handler = CallbackQueryHandler(game.stand_callback, pattern=r"^stand_[0-9]{7}$")
join_callback_handler = CallbackQueryHandler(game.join_callback, pattern=r"^join_[0-9]{7}$")
start_callback_handler = CallbackQueryHandler(game.start_callback, pattern=r"^start_[0-9]{7}$")
newgame_callback_handler = CallbackQueryHandler(game.newgame_callback, pattern=r"^newgame$")
language_callback_handler = CallbackQueryHandler(settings.language_callback, pattern=r"^lang_([a-z]{2}(?:-[a-z]{2})?)$")
reset_stats_callback_handler = CallbackQueryHandler(util.reset_stats_callback, pattern=r"^reset_stats_(confirm|cancel)$")

handlers = [banned_user_handler,
            start_command_handler, stop_command_handler, join_callback_handler, hit_callback_handler,
            stand_callback_handler, start_callback_handler, language_command_handler, stats_command_handler,
            newgame_callback_handler, reload_lang_command_handler, language_callback_handler, users_command_handler,
            comment_command_handler, comment_text_command_handler, answer_command_handler, ban_command_handler,
            unban_command_handler, bans_command_handler, resetstats_command_handler, reset_stats_callback_handler]

__all__ = ['handlers', 'error_handler']
