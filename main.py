# -*- coding: utf-8 -*-
import json
import logging.handlers
import os
import re
import sys
from threading import Thread

from telegram import ReplyKeyboardRemove
from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup

import config
from database.db_wrapper import DBwrapper
from database.statistics import get_user_stats
from game.blackJackGame import BlackJackGame
from gamehandler import GameHandler
from lang.language import translate
from statehandler import StateHandler
from userstate import UserState

__author__ = 'Rico'

logdir_path = os.path.dirname(os.path.abspath(__file__))
logfile_path = os.path.join(logdir_path, "logs", "bot.log")

if not os.path.exists(os.path.join(logdir_path, "logs")):
    os.makedirs(os.path.join(logdir_path, "logs"))

logfile_handler = logging.handlers.WatchedFileHandler(logfile_path, 'a', 'utf-8')

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO,
                    handlers=[logfile_handler])

if not re.match(r"[0-9]+:[a-zA-Z0-9\-_]+", config.BOT_TOKEN):
    logging.error("Bot token not correct - please check.")
    exit(1)

updater = Updater(token=config.BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

game_handler = GameHandler().get_instance()


# -----------------
# Internal methods
# -----------------
def change_language(bot, update, lang_id):
    logger.info("Language changed to '{}' for user {}".format(lang_id, update.effective_user.id))
    bot.editMessageText(chat_id=update.callback_query.message.chat_id, text=translate("langChanged", lang_id),
                        message_id=update.callback_query.message.message_id, reply_markup=None)
    db = DBwrapper.get_instance()
    db.insert("languageID", lang_id, update.callback_query.from_user.id)


def callback_eval(update, context):
    bot = context.bot
    query_data = update.callback_query.data

    # For changing the language:
    if query_data.startswith("ch_lang"):
        lang_id = re.search("ch_lang_([a-z]{2})", query_data).group(1)
        change_language(bot=bot, update=update, lang_id=lang_id)

    elif query_data == "com_ch_lang":
        language_cmd(update, context)

    elif query_data == "cancel_comment":
        cancel_cmd(update, context)

    elif query_data == "new_game" or query_data == "start_game":
        bot.answerCallbackQuery(callback_query_id=update.callback_query.id)
        start_cmd(update, context)

    elif query_data == "join_game":
        bot.answerCallbackQuery(callback_query_id=update.callback_query.id)
        join_cmd(update, context)


def send_message(chat_id, text, message_id=None, parse_mode=None, reply_markup=None, game_id=None):
    updater.bot.sendMessage(chat_id=chat_id, text=text, reply_to_message_id=message_id, parse_mode=parse_mode,
                            reply_markup=reply_markup)


def send_mp_message(chat_id, text, message_id=None, parse_mode=None, reply_markup=None, game_id=None):
    game = game_handler.get_game_by_id(game_id)

    if game is not None:
        for player in game.players:
            user_id = player.user_id
            send_message(chat_id=user_id, text=text, parse_mode=parse_mode, reply_markup=reply_markup)
    else:
        print("Game is None")


def game_commands(update, context):
    bot = context.bot
    if update.message is None:
        logger.warning("game_commands error happened again! Update: {}".format(update))

    text = update.effective_message.text
    chat_id = update.effective_message.chat_id
    user = update.effective_user
    user_id = user.id
    first_name = user.first_name
    last_name = user.last_name
    username = user.username
    db = DBwrapper.get_instance()
    lang_id = db.get_lang_id(user_id)

    state_handler = StateHandler.get_instance()
    user = state_handler.get_user(user_id)

    if user.get_state() == UserState.COMMENTING:
        # User wants to comment!
        update.message.reply_text(text=translate("userComment", lang_id))
        for admin_id in db.get_admins():
            admin_message = "New comment:\n\n{}\n\n{} | {} | {} | @{} | {}".format(text, user_id, first_name, last_name,
                                                                                   username, lang_id)
            bot.sendMessage(admin_id, text=admin_message)

        user.set_state(UserState.IDLE)
        return

    if not db.is_user_saved(user_id):
        logger.info("New user - {}".format(user_id))
        db.add_user(user_id, "en", first_name, last_name, username)

        if chat_id > 0:
            # ask user for language if it's a private chat:
            language_cmd(update, context)

        return

    # check if user already has got a game (in the same chat):
    # TODO multiplayer games
    game = game_handler.get_game_by_chatid(chat_id)
    if game is not None:
        logger.debug("Game already existing. Forwarding text '{}' to game".format(text))
        game.analyze_message(update)


def error_callback(update, context):
    """Log Errors caused by Updates."""
    error = context.error
    logger.error('Update "%s" caused error "%s"', update, error)
    try:
        raise error
    except Unauthorized as e:
        logger.error(e.message)  # remove update.message.chat_id from conversation list
        logger.error(update)
        # TODO the unauthorized error indicates that a user blocked the bot.
        return
    except BadRequest as e:
        logger.error(e.message)  # handle malformed requests
        return
    except TimedOut:
        pass  # connection issues are ignored for now
        return
    except NetworkError as e:
        logger.error(e.message)  # handle other connection problems
    except ChatMigrated as e:
        logger.error(e.message)  # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError as e:
        logger.error(e.message)  # handle all other telegram related errors

    db = DBwrapper.get_instance()
    for admin_id in db.get_admins():
        send_message(admin_id, "Update '{0}' caused error '{1}'".format(json.dumps(update.to_dict(), indent=2), error))


def stop_and_restart():
    """Gracefully stops the Updater and replaces the current process with a new one"""
    updater.stop()
    os.execl(sys.executable, sys.executable, *sys.argv)


def admin_method(func):
    """Decorator for marking methods as admin-only methods, so that strangers can't use them"""

    def admin_check(update, context):
        db = DBwrapper.get_instance()
        user = update.message.from_user
        if user.id in db.get_admins():
            return func(update, context)
        else:
            update.message.reply_text('You have not the required permissions to do that!')
            logger.warning(
                "User {} ({}, @{}) tried to use admin function '{}'!".format(user.id, user.first_name, user.username,
                                                                             func.__name__))

    return admin_check


# -----------------
# User commands
# -----------------
def start_cmd(update, context):
    message = update.effective_message
    chat_id = message.chat_id
    eff_user = update.effective_user
    user_id = eff_user.id
    message_id = message.message_id
    first_name = eff_user.first_name
    last_name = eff_user.last_name
    username = eff_user.username
    db = DBwrapper.get_instance()

    state_handler = StateHandler.get_instance()
    user = state_handler.get_user(user_id)

    if not db.is_user_saved(user_id):
        logger.info("New user: {}".format(user_id))
        db.add_user(user_id, "en", first_name, last_name, username)
        if chat_id > 0:
            # ask user for language:
            language_cmd(update, context)
            return

    # check if user already has got a game (in the same chat):
    game_index = game_handler.get_index_by_chatid(chat_id)
    if game_index is None:
        user.set_state(UserState.PLAYING)
        logger.debug("Creating a game")
        lang_id = db.get_lang_id(user_id)
        bj = BlackJackGame(chat_id, user_id, lang_id, first_name, game_handler, message_id, send_message)
        game_handler.add_game(bj)
    else:
        logger.debug("Game already existing. Starting game!")
        game = game_handler.get_game_by_index(game_index)

        if game.players[0].user_id == user_id:
            game.start_game()
        else:
            message.reply_text("Only the creator ({}) can start the game".format(game.players[0].first_name))


def stop_cmd(update, context):
    user_id = update.message.from_user.id
    state_handler = StateHandler.get_instance()
    user = state_handler.get_user(user_id)

    user.set_state(UserState.IDLE)

    chat_id = update.message.chat_id
    game_handler.gl_remove(chat_id)


def help_cmd(update, context):
    # Explains commands to user
    db = DBwrapper.get_instance()
    lang_id = db.get_lang_id(update.message.from_user.id)

    start_description = translate("start_description", lang_id)
    stop_description = translate("stop_description", lang_id)
    help_description = translate("help_description", lang_id)
    language_description = translate("language_description", lang_id)
    stats_description = translate("stats_description", lang_id)
    hide_description = translate("hide_description", lang_id)
    text = "/start - {}\n" \
           "/stop - {}\n" \
           "/help - {}\n" \
           "/language - {}\n" \
           "/stats - {}\n" \
           "/hide - {}" \
        .format(start_description,
                stop_description,
                help_description,
                language_description,
                stats_description,
                hide_description
                )

    update.message.reply_text(text)


def join_cmd(update, context):
    message = update.effective_message
    user = update.effective_user
    game = game_handler.get_game_by_chatid(message.chat_id)

    if game is not None:
        game.add_player(user.id, user.first_name, message.message_id)


def stats_cmd(update, context):
    update.message.reply_text(get_user_stats(update.message.from_user.id))


def language_cmd(update, context):
    lang_de_button = InlineKeyboardButton(text="Deutsch \U0001F1E9\U0001F1EA", callback_data="ch_lang_de")
    lang_en_button = InlineKeyboardButton(text="English \U0001F1FA\U0001F1F8", callback_data="ch_lang_en")
    lang_nl_button = InlineKeyboardButton(text="Nederlands \U0001F1F3\U0001F1F1", callback_data="ch_lang_nl")
    lang_eo_button = InlineKeyboardButton(text="Esperanto \U0001F30D", callback_data="ch_lang_eo")
    lang_br_button = InlineKeyboardButton(text="Português \U0001F1E7\U0001F1F7", callback_data="ch_lang_br")
    lang_es_button = InlineKeyboardButton(text="Español \U0001F1EA\U0001F1F8", callback_data="ch_lang_es")
    lang_ru_button = InlineKeyboardButton(text="Русский \U0001F1F7\U0001F1FA", callback_data="ch_lang_ru")
    lang_fa_button = InlineKeyboardButton(text="فارسی \U0001F1EE\U0001F1F7", callback_data="ch_lang_fa")

    lang_keyboard = InlineKeyboardMarkup(
        [[lang_de_button, lang_en_button], [lang_br_button, lang_ru_button, lang_nl_button],
         [lang_es_button, lang_eo_button, lang_fa_button]])
    db = DBwrapper.get_instance()

    if update.callback_query:
        # TODO maybe text user in private instead of group!
        lang_id = db.get_lang_id(update.callback_query.from_user.id)
        bot.editMessageText(chat_id=update.callback_query.message.chat_id, text=translate("langSelect", lang_id),
                            reply_markup=lang_keyboard, message_id=update.callback_query.message.message_id)
    else:
        lang_id = db.get_lang_id(update.message.from_user.id)
        bot.sendMessage(chat_id=update.message.chat_id, text=translate("langSelect", lang_id),
                        reply_markup=lang_keyboard, message_id=update.message.message_id)


def comment_cmd(update, context):
    bot = context.bot
    args = context.args
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    username = update.message.from_user.username
    db = DBwrapper.get_instance()
    lang_id = db.get_lang_id(user_id)

    state_handler = StateHandler.get_instance()
    user = state_handler.get_user(user_id)

    if user.get_state() == UserState.IDLE:
        if len(args) > 1:
            text = " ".join(args)
            logger.debug("New comment! {}!".format(user_id))

            update.message.reply_text(text=translate("userComment", lang_id))
            for admin_id in db.get_admins():
                bot.sendMessage(admin_id,
                                "New comment:\n\n{}\n\n{} | {} | {} | @{} | {}".format(text, user_id, first_name,
                                                                                       last_name, username,
                                                                                       lang_id))
            user.set_state(UserState.IDLE)
        else:
            # The user just wrote "/comment" -> Ask him to send a message
            logger.debug("Add {} to comment_list!".format(user_id))

            keyboard = [[InlineKeyboardButton(text=translate("cancel", lang_id), callback_data="cancel_comment")]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            update.message.reply_text(text=translate("sendCommentNow", lang_id), reply_markup=reply_markup)
            user.set_state(UserState.COMMENTING)


def cancel_cmd(update, context):
    user_id = update.effective_user.id
    cbq = update.callback_query

    state_handler = StateHandler.get_instance()
    user = state_handler.get_user(user_id)

    if user.get_state() == UserState.COMMENTING:
        db = DBwrapper.get_instance()
        lang_id = db.get_lang_id(user_id)

        user.set_state(UserState.IDLE)
        cbq.edit_message_text(text=translate("cancelledMessage", lang_id))
        cbq.answer(text=translate("cancelledMessage", lang_id))


def hide_cmd(update, context):
    """Hides the keyboard in the specified chat."""
    update.message.reply_text("\U0001F44D", reply_markup=ReplyKeyboardRemove())


def mentions_cmd(update, context):
    # TODO mention users which helped (translations, etc.)
    pass


def multiplayer(update, context):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    message_id = update.message.message_id
    msg = update.message
    first_name = update.message.from_user.first_name
    # last_name = update.message.from_user.last_name
    # username = update.message.from_user.username
    db = DBwrapper.get_instance()

    game_index = game_handler.get_index_by_chatid(chat_id)
    if game_index is None:
        logger.debug("Creating a game")
        lang_id = db.get_lang_id(user_id)
        game_id = game_handler.generate_id()
        bj = BlackJackGame(chat_id, user_id, lang_id, first_name, game_handler, message_id, send_mp_message,
                           multiplayer=True, game_id=game_id)
        game_handler.add_game(bj)
        msg.reply_text("Your game_id: {}".format(bj.game_id))
    else:
        logger.debug("Game already existing")


def join_secret(update, context):
    user_id = update.message.from_user.id
    message_id = update.message.message_id
    first_name = update.message.from_user.first_name
    text = update.message.text
    game_id = text.split(' ')[1]

    print("ID: " + game_id)
    game = game_handler.get_game_by_id(game_id)
    game.add_player(user_id, first_name, message_id)
    # TODO send message that user joined


def leave_chat(update, context):
    logger.info("Leave channel")
    context.bot.leaveChat(update.effective_message.chat.id)


# -----------------
# Admin commands
# -----------------
@admin_method
def answer(update, context):
    msg = update.message
    reply_to_message = update.message.reply_to_message
    sender_id = update.message.from_user.id
    text = str(update.message.text[8:])
    db = DBwrapper.get_instance()

    if reply_to_message is None:
        msg.reply_text(text="⚠ You need to reply to the user's comment!")
        return

    try:
        last_line = reply_to_message.text.split("\n")
        ll_list = last_line[-1].split(" | ")
        receiver_id = ll_list[0]
    except ValueError:
        return

    if not re.match("[0-9]+", receiver_id):
        msg.reply_text("⚠ The user_id is not valid. Are you sure you replied to a user comment?")
        return

    answer_text = "{}\n\n{}".format(translate("answerFromDev", db.get_lang_id(receiver_id)), text)
    context.bot.sendMessage(chat_id=receiver_id, text=answer_text)
    msg.reply_text(text="Message sent!")


@admin_method
def users(update, context):
    db = DBwrapper.get_instance()
    players = db.get_recent_players()

    text = "Last 24 hours: {}".format(len(players))

    update.message.reply_text(text=text)


@admin_method
def restart(update, context):
    update.message.reply_text('Bot is restarting...')
    Thread(target=stop_and_restart).start()


channel_handler = MessageHandler(Filters.update.channel_posts, leave_chat)
start_handler = CommandHandler("start", start_cmd)
stop_handler = CommandHandler("stop", stop_cmd)
join_handler = CommandHandler("join", join_cmd)
help_handler = CommandHandler('help', help_cmd)
hide_handler = CommandHandler('hide', hide_cmd)
stats_handler = CommandHandler('stats', stats_cmd)
language_handler = CommandHandler('language', language_cmd)
comment_handler = CommandHandler('comment', comment_cmd, pass_args=True)
callback_handler = CallbackQueryHandler(callback_eval)
users_handler = CommandHandler('users', users)
answer_handler = CommandHandler('answer', answer)
restart_handler = CommandHandler('restart', restart)

game_command_handler = MessageHandler(Filters.text, game_commands)

mp_handler = CommandHandler('multiplayer', multiplayer)
join_sec = CommandHandler('join_secret', join_secret)

handlers = [channel_handler, start_handler, stop_handler, join_handler, help_handler,
            hide_handler, stats_handler, language_handler, comment_handler,
            callback_handler, users_handler, answer_handler, restart_handler,
            mp_handler, join_sec, game_command_handler]

for handler in handlers:
    dispatcher.add_handler(handler)

dispatcher.add_error_handler(error_callback)

if config.USE_WEBHOOK:
    updater.start_webhook(listen="127.0.0.1", port=config.WEBHOOK_PORT, url_path=config.BOT_TOKEN, cert=config.CERTPATH, webhook_url=config.WEBHOOK_URL)
    updater.bot.set_webhook(config.WEBHOOK_URL)
    logger.info("Started webhook server!")
else:
    updater.start_polling()
    logger.info("Started polling!")

logger.info("Bot started as @{}".format(updater.bot.username))
updater.idle()
