# -*- coding: utf-8 -*-
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from blackjackbot.lang import translate
from database import Database
from database.statistics import get_user_stats


def stats_cmd(update, context):
    update.message.reply_text(get_user_stats(update.effective_user.id))


def rules_cmd(update, context):
    update.effective_message.reply_text("Rules:\n\n- Black Jack pays 3 to 2\n- Dealer must stand on 17 and must draw to 16\n- Insurance pays 2 to 1")
