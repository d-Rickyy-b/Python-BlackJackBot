# -*- coding: utf-8 -*-

import logging
import re

from blackjackbot.commands.admin import notify_admins
from blackjackbot.commands.util.decorators import admin_method
from blackjackbot.lang import reload_strings, Translator
from database import Database

logger = logging.getLogger(__name__)


@admin_method
def reload_languages_cmd(update, context):
    reload_strings()


@admin_method
def answer_comment_cmd(update, context):
    # Answer to admins only in English, because we don't save admin languages yet
    text = update.effective_message.text
    reply_to_message = update.message.reply_to_message
    text = text.replace("/answer ", "")

    # Error handling
    if reply_to_message is None or update.message.reply_to_message.from_user.id != context.bot.id:
        update.message.reply_text("⚠ You need to reply to the user's comment!")
        return
    if update.message.reply_to_message.text is None:
        update.message.reply_text("⚠ You replied to a non text message!")
        return

    try:
        # Parse user data from the message
        user_info = reply_to_message.text.split("\n")[-1]
    except Exception as e:
        update.message.reply_text("⚠ An unexpected error occurred!")
        logger.error("While parsing user data, the following exception occurred: {}".format(e))
        return

    user = user_info.split(" | ")

    if type(user) != list or len(user) != 6:
        update.message.reply_text("⚠ Can't parse user data from the message you replied to! Please reply to a comment!")
        logger.warning("Can't parse user data from message: {}".format(reply_to_message.text))
        return

    chat_id = user[0]

    if not re.match(r"^\d+$", chat_id):
        update.message.reply_text("⚠ Malformed chat_id!")
        logger.error("Malformed chat_id: {}".format(chat_id))
        return

    translator = Translator(chat_id)
    user_reply = translator("reply_from_maintainer").format(text)

    # The following errors can easily happen here:
    # Have no rights to send a message -> Missing permissions
    # Forbidden: bot was blocked by the user -> User blocked the bot
    context.bot.send_message(chat_id=chat_id, text=user_reply)
    update.message.reply_text(text="I sent your comment to the user!")

    notify_admins("An admin replied to the comment by\n\n{}\n\nwith:\n\n{}".format(user_info, text), context)


@admin_method
def users_cmd(update, context):
    """Returns the amount of players in the last 24 hours"""
    db = Database()
    players = db.get_recent_players()

    text = "Last 24 hours: {}".format(len(players))

    update.message.reply_text(text=text)
