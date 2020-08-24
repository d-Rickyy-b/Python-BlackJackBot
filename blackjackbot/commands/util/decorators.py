# -*- coding: utf-8 -*-
import functools
import logging

from blackjackbot.commands.util import remove_inline_keyboard
from blackjackbot.errors import NoActiveGameException
from blackjackbot.gamestore import GameStore
from blackjackbot.lang import Translator
from database import Database


def admin_method(func):
    """Decorator for marking methods as admin-only methods, so that strangers can't use them"""

    def admin_check(update, context):
        user = update.effective_user
        chat = update.effective_chat
        lang_id = Database().get_lang_id(chat.id)
        translator = Translator(lang_id=lang_id)

        if user.id in Database().get_admins():
            return func(update, context)
        else:
            update.message.reply_text(translator("no_permission"))
            logging.warning("User {} ({}, @{}) tried to use admin function '{}'!".format(user.id, user.first_name, user.username, func.__name__))

    return admin_check


def needs_active_game(func):
    """Decorator for making sure a game exists for a certain chat"""

    @functools.wraps(func)
    def wrapper(update, context, *args, **kwargs):
        chat = update.effective_chat
        lang_id = Database().get_lang_id(chat.id)
        translator = Translator(lang_id=lang_id)

        try:
            game = GameStore().get_game(chat.id)
        except NoActiveGameException:
            remove_inline_keyboard(update, context)
            update.effective_message.reply_text(translator("mp_no_created_game_callback"))
            return

        return func(update, context)

    return wrapper
