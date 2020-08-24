# -*- coding: utf-8 -*-

from blackjackbot.lang import translate
from database.statistics import get_user_stats


def stats_cmd(update, context):
    update.message.reply_text(get_user_stats(update.effective_user.id))


def comment_cmd(update, context):
    """Handler for the /comment command"""
    # 1. check if a player is currently playing a game
    # 2. if yes: tell them that they can't send a comment at the moment & exit
    # 2.1 clear commenting state
    # 3. if no: request their comment + Inline cancel button + store message ID
    # 4. if game is started for that chat, edit message: "commenting during game is not possible" + remove keyboard + exit
    # 4.1 clear commenting state
    # 5. Wait for any kind of text and forward to the admins
    # 5.1 clear 'commenting' state
    update.message.reply_text(translate("send_comment"))
    pass


def comment_text(update, context):
    # Extract text
    # send it to the admins
    # reply user that we received the text
    pass
