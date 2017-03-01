# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram.inlinekeyboardmarkup import InlineKeyboardMarkup
from telegram.inlinekeyboardbutton import InlineKeyboardButton
from telegram.callbackquery import CallbackQuery

import logging

from gamehandler import GameHandler
from lang.language import translation
from database.db_wrapper import DBwrapper

__author__ = 'Rico'

CHANGE_LANG_DE = "ch_lang_de"
CHANGE_LANG_EN = "ch_lang_en"
CHANGE_LANG_NL = "ch_lang_nl"
CHANGE_LANG_EO = "ch_lang_eo"
CHANGE_LANG_BR = "ch_lang_br"
CHANGE_LANG_ES = "ch_lang_es"
CHANGE_LANG_RU = "ch_lang_ru"
CHANGE_LANG_FA = "ch_lang_fa"

BOT_TOKEN = "<your_bot_token>"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
updater = Updater(token=BOT_TOKEN)
dispatcher = updater.dispatcher

game_handler = GameHandler()
game_list = game_handler.GameList


def start(bot, update):
    startbutton = InlineKeyboardButton(text="Start", callback_data="com_start")
    stopbutton = InlineKeyboardButton(text="Stop", callback_data="com_stop")
    langbutton = InlineKeyboardButton(text="Language", callback_data="com_ch_lang")

    reply_keyboard = InlineKeyboardMarkup([[startbutton, stopbutton], [langbutton]])
    bot.sendMessage(chat_id=update.message.chat_id, text="Was möchtest du tun?", reply_markup=reply_keyboard)


def stop(bot, update):
    pass


def help(bot, update):
    pass


def stats(bot, update):
    pass


def language(bot, update):
    lang_de_button = InlineKeyboardButton(text="Deutsch \U0001F1E9\U0001F1EA", callback_data="ch_lang_de")
    lang_en_button = InlineKeyboardButton(text="Englisch \U0001F1FA\U0001F1F8", callback_data="ch_lang_en")
    lang_nl_button = InlineKeyboardButton(text="Nederlands \U0001F1F3\U0001F1F1", callback_data="ch_lang_nl")
    lang_eo_button = InlineKeyboardButton(text="Esperanto \U0001F30D", callback_data="ch_lang_eo")
    lang_br_button = InlineKeyboardButton(text="Português \U0001F1E7\U0001F1F7", callback_data="ch_lang_br")
    lang_es_button = InlineKeyboardButton(text="Español \U0001F1EA\U0001F1F8", callback_data="ch_lang_es")
    lang_ru_button = InlineKeyboardButton(text="Русский \U0001F1F7\U0001F1FA", callback_data="ch_lang_ru")
    lang_fa_button = InlineKeyboardButton(text="فارسی \U0001F1EE\U0001F1F7", callback_data="ch_lang_fa")

    lang_keyboard = InlineKeyboardMarkup([[lang_de_button, lang_en_button], [lang_br_button, lang_ru_button, lang_nl_button], [lang_es_button, lang_eo_button, lang_fa_button]])
    bot.editMessageText(chat_id=update.callback_query.message.chat_id, text="Wähle deine Sprache", reply_markup=lang_keyboard, message_id=update.callback_query.message.message_id)
    pass


def comment(bot, update):
    pass


def change_language(bot, update, lang_id):
    # TODO pass lang_id and translate string
    # TODO inline answer, no new message
    # bot.sendMessage(chat_id=update.callback_query.message.chat_id, text=translation("langChanged", lang_id))
    bot.editMessageText(chat_id=update.callback_query.message.chat_id, text=translation("langChanged", lang_id), message_id=update.callback_query.message.message_id, reply_markup=None)
    # sql insert
    # sql_insert("languageID", lang_id, user_id)  # TODO language setting for whole groups (low prio)


def callback_eval(bot, update):
    query_data = update.callback_query.data

    # For changing the language:
    if query_data.startswith("ch_lang"):
        if query_data == CHANGE_LANG_DE:
            lang_id = "de"
        elif query_data == CHANGE_LANG_EN:
            lang_id = "en"
        elif query_data == CHANGE_LANG_NL:
            lang_id = "nl"
        elif query_data == CHANGE_LANG_EO:
            lang_id = "eo"
        elif query_data == CHANGE_LANG_BR:
            lang_id = "br"
        elif query_data == CHANGE_LANG_ES:
            lang_id = "es"
        elif query_data == CHANGE_LANG_RU:
            lang_id = "ru"
        elif query_data == CHANGE_LANG_FA:
            lang_id = "fa"

        change_language(bot=bot, update=update, lang_id=lang_id)

    elif query_data == "com_ch_lang":
        language(bot, update)

    print(query_data)

start_handler = CommandHandler('start', start)
language_handler = CommandHandler('language', language)
callback_handler = CallbackQueryHandler(callback_eval)

dispatcher.add_handler(callback_handler)
dispatcher.add_handler(language_handler)
dispatcher.add_handler(start_handler)


updater.start_polling()
