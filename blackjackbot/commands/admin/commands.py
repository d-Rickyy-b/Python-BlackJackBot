# -*- coding: utf-8 -*-

from blackjackbot.commands.util.decorators import admin_method
from blackjackbot.lang import reload_strings
from database import Database


@admin_method
def reload_languages_cmd(update, context):
    reload_strings()


@admin_method
def answer_comment_cmd(upate, context):
    pass


@admin_method
def users_cmd(update, context):
    """Returns the amount of players in the last 24 hours"""
    db = Database()
    players = db.get_recent_players()

    text = "Last 24 hours: {}".format(len(players))

    update.message.reply_text(text=text)
