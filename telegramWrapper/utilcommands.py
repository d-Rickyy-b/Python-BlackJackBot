# -*- coding: utf-8 -*-
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from database import Database
from database.statistics import get_user_stats


def stats_cmd(update, context):
    update.message.reply_text(get_user_stats(update.effective_user.id))


def language_cmd(update, context):
    lang_de_button = InlineKeyboardButton(text="Deutsch \U0001F1E9\U0001F1EA", callback_data="lang_de")
    lang_en_button = InlineKeyboardButton(text="English \U0001F1FA\U0001F1F8", callback_data="lang_en")
    lang_nl_button = InlineKeyboardButton(text="Nederlands \U0001F1F3\U0001F1F1", callback_data="lang_nl")
    lang_eo_button = InlineKeyboardButton(text="Esperanto \U0001F30D", callback_data="lang_eo")
    lang_br_button = InlineKeyboardButton(text="Português \U0001F1E7\U0001F1F7", callback_data="lang_br")
    lang_es_button = InlineKeyboardButton(text="Español \U0001F1EA\U0001F1F8", callback_data="lang_es")
    lang_ru_button = InlineKeyboardButton(text="Русский \U0001F1F7\U0001F1FA", callback_data="lang_ru")
    lang_fa_button = InlineKeyboardButton(text="فارسی \U0001F1EE\U0001F1F7", callback_data="lang_fa")

    lang_keyboard = InlineKeyboardMarkup(
        [[lang_de_button, lang_en_button], [lang_br_button, lang_ru_button, lang_nl_button],
         [lang_es_button, lang_eo_button, lang_fa_button]])
    db = Database()

    lang_id = db.get_lang_id(update.effective_user.id)

    if update.callback_query:
        # TODO maybe text user in private instead of group!
        context.bot.editMessageText(chat_id=update.callback_query.message.chat_id, text=translate("langSelect", lang_id),
                                    reply_markup=lang_keyboard, message_id=update.callback_query.message.message_id)
    else:
        update.message.reply_text(text=translate("langSelect", lang_id), reply_markup=lang_keyboard)


def translate(string_id, lang_id="en"):
    translations = {
        "your_cards_are": "{} - <b>Value: {}</b>\n\n{}",
        "asdf": ""
    }

    return translations.get(string_id, "!Not translated yet!")
