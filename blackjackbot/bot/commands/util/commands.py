# -*- coding: utf-8 -*-

from blackjackbot.lang import translate
from database.statistics import get_user_stats


def stats_cmd(update, context):
    update.message.reply_text(get_user_stats(update.effective_user.id))


