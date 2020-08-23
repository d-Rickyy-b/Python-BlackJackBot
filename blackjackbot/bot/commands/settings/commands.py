# -*- coding: utf-8 -*-
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from blackjackbot.lang import translate, get_available_languages
from blackjackbot.util import build_menu
from database import Database


def language_cmd(update, context):
    buttons = []

    for lang in get_available_languages():
        display_name = lang.get("display_name")
        lang_code = lang.get("lang_code")
        buttons.append(InlineKeyboardButton(text=display_name, callback_data="lang_{}".format(lang_code)))

    lang_keyboard = InlineKeyboardMarkup(build_menu(buttons, n_cols=3))
    db = Database()

    lang_id = db.get_lang_id(update.effective_user.id)

    if update.callback_query:
        # TODO maybe text user in private instead of group!
        context.bot.editMessageText(chat_id=update.callback_query.message.chat_id, text=translate("select_lang", lang_id),
                                    reply_markup=lang_keyboard, message_id=update.callback_query.message.message_id)
    else:
        update.message.reply_text(text=translate("select_lang", lang_id), reply_markup=lang_keyboard)


def language_callback(update, context):
    pass
