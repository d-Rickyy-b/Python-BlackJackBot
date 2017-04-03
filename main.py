# -*- coding: utf-8 -*-

import logging

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram.inlinekeyboardbutton import InlineKeyboardButton
from telegram.inlinekeyboardmarkup import InlineKeyboardMarkup

from database.db_wrapper import DBwrapper
from database.statistics import get_user_stats
from game.blackJack import BlackJack
from gamehandler import GameHandler
from lang.language import translate

__author__ = 'Rico'

BOT_TOKEN = "<your_bot_token>"

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
updater = Updater(token=BOT_TOKEN)
dispatcher = updater.dispatcher

game_handler = GameHandler()
tg_bot = updater.bot


def start(bot, update):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    message_id = update.message.message_id
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    username = update.message.from_user.username
    db = DBwrapper.get_instance()

    if not (db.is_user_saved(user_id)):
        # ask user for language:
        logger.info("New user")
        db.add_user(user_id, "en", first_name, last_name, username)
        language(bot, update)
        return

    # check if user already has got a game (in the same chat):
    game_index = game_handler.get_index_by_chatid(chat_id)
    if game_index == -1:
        logger.debug("Creating a game")
        lang_id = db.get_lang_id(user_id)
        bj = BlackJack(chat_id, user_id, lang_id, first_name, game_handler, message_id, send_message)
        game_handler.add_game(bj)
    else:
        logger.debug("Game already existing. Starting game!")
        game = game_handler.get_game_by_index(game_index)
        game.start_game()


def stop(bot, update):
    pass


def help_def(bot, update):
    pass


def stats(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=get_user_stats(update.message.from_user.id))


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
    db = DBwrapper.get_instance()

    if update.callback_query:
        # TODO maybe text user in private instead of group!
        lang_id = db.get_lang_id(update.callback_query.from_user.id)
        bot.editMessageText(chat_id=update.callback_query.message.chat_id, text=translate("langSelect", lang_id), reply_markup=lang_keyboard, message_id=update.callback_query.message.message_id)
    else:
        lang_id = db.get_lang_id(update.message.from_user.id)
        bot.sendMessage(chat_id=update.message.chat_id, text=translate("langSelect", lang_id), reply_markup=lang_keyboard, message_id=update.message.message_id)


def comment(bot, update):
    # TODO add comment functionality
    pass


def mentions(bot, update):
    # TODO mention users which helped (translations, etc.)
    pass


def change_language(bot, update, lang_id):
    bot.editMessageText(chat_id=update.callback_query.message.chat_id, text=translate("langChanged", lang_id), message_id=update.callback_query.message.message_id, reply_markup=None)
    db = DBwrapper.get_instance()
    db.insert("languageID", lang_id, update.callback_query.from_user.id)


def callback_eval(bot, update):
    query_data = update.callback_query.data

    # For changing the language:
    if query_data.startswith("ch_lang"):
        if query_data == "ch_lang_de":
            lang_id = "de"
        elif query_data == "ch_lang_en":
            lang_id = "en"
        elif query_data == "ch_lang_nl":
            lang_id = "nl"
        elif query_data == "ch_lang_eo":
            lang_id = "eo"
        elif query_data == "ch_lang_br":
            lang_id = "br"
        elif query_data == "ch_lang_es":
            lang_id = "es"
        elif query_data == "ch_lang_ru":
            lang_id = "ru"
        elif query_data == "ch_lang_fa":
            lang_id = "fa"
        else:
            lang_id = "en"

        change_language(bot=bot, update=update, lang_id=lang_id)

    elif query_data == "com_ch_lang":
        language(bot, update)

    print(query_data)


def send_message(chat_id, text, message_id=None, parse_mode=None, reply_markup=None, game_id=None):
    tg_bot.sendMessage(chat_id=chat_id, text=text, reply_to_message_id=message_id, parse_mode=parse_mode, reply_markup=reply_markup)


def game_commands(bot, update):
    text = update.message.text
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    username = update.message.from_user.username
    db = DBwrapper.get_instance()

    if not (db.is_user_saved(user_id)):
        # ask user for language:
        logger.info("New user")
        db.add_user(user_id, "en", first_name, last_name, username)
        language(bot, update)
        return

    # check if user already has got a game (in the same chat):
    game_index = game_handler.get_index_by_chatid(chat_id)
    if game_index != -1:
        logger.debug("Game already existing. Forwarding text '" + text + "' to game")
        game = game_handler.get_game_by_index(game_index)
        game.analyze_message(update)


start_handler = CommandHandler('start', start)
stats_handler = CommandHandler('stats', stats)
language_handler = CommandHandler('language', language)
callback_handler = CallbackQueryHandler(callback_eval)
game_command_handler = MessageHandler(Filters.all, game_commands)

dispatcher.add_handler(callback_handler)
dispatcher.add_handler(language_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(stats_handler)
dispatcher.add_handler(game_command_handler)

updater.start_polling()
