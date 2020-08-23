# -*- coding: utf-8 -*-
import logging

from blackjackbot.lang import translate, reload_strings, Translator
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


def notify_admins(text, context):
    """
    Sends a message to all stored admins
    :param text: The text that is sent
    :param context: python-telegram-bot context object
    :return:
    """
    db = Database()
    for admin_id in db.get_admins():
        context.bot.sendMessage(admin_id, text=text)


@admin_method
def reload_languages_cmd(update, context):
    reload_strings()


@admin_method
def answer_comment_cmd(upate, context):
    pass


@admin_method
def users_cmd(update, context):
    db = Database()
    players = db.get_recent_players()

    text = "Last 24 hours: {}".format(len(players))

    update.message.reply_text(text=text)
