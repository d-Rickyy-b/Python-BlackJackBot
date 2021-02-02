# -*- coding: utf-8 -*-
from database import Database


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
