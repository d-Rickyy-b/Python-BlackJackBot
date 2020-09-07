# -*- coding: utf-8 -*-

from telegram import ForceReply

from blackjackbot.commands.admin.functions import notify_admins
from blackjackbot.lang import translate
from blackjackbot.util.userstate import UserState
from database import Database
from database.statistics import get_user_stats


def stats_cmd(update, context):
    update.message.reply_text(get_user_stats(update.effective_user.id))


def comment_cmd(update, context):
    """MessageHandler callback for the /comment command"""
    if context.user_data.get("state", UserState.IDLE) != UserState.IDLE:
        return

    chat = update.effective_chat
    lang_id = Database().get_lang_id(chat.id)
    update.message.reply_text(translate("send_comment", lang_id), reply_markup=ForceReply())
    context.user_data["state"] = UserState.COMMENTING
    pass


def comment_text(update, context):
    """
    MessageHandler callback for processing comments sent by a user.
    Notifies the admins of the bot about the comment
    """
    # Only handle the message, if the user is currently in the "commenting" state
    if context.user_data.get("state", None) != UserState.COMMENTING:
        return

    user = update.effective_user
    chat = update.effective_chat
    lang_id = Database().get_lang_id(chat.id)

    data = [chat.id, user.id, user.first_name, user.last_name, "@" + user.username, user.language_code]

    userdata = " | ".join([str(item) for item in data])
    userdata = userdata.replace("\r", "").replace("\n", "")

    text = update.effective_message.text

    notify_admins("New comment from a user:\n\n{}\n\n{}".format(text, userdata), context)
    update.message.reply_text(translate("received_comment", lang_id))

    context.user_data["state"] = UserState.IDLE
