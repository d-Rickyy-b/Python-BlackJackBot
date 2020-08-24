# -*- coding: utf-8 -*-
import logging
import re

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from blackjackbot.lang import translate, get_available_languages, get_language_info
from blackjackbot.util import build_menu
from database import Database

logger = logging.getLogger(__name__)


def language_cmd(update, context):
    """
    Handler for /language commands
    """
    buttons = []

    for lang in get_available_languages():
        display_name = lang.get("display_name")
        lang_code = lang.get("lang_code")
        buttons.append(InlineKeyboardButton(text=display_name, callback_data="lang_{}".format(lang_code)))

    lang_keyboard = InlineKeyboardMarkup(build_menu(buttons, n_cols=3))

    lang_id = Database().get_lang_id(update.effective_chat.id)
    update.message.reply_text(text=translate("select_lang", lang_id), reply_markup=lang_keyboard)


def language_callback(update, context):
    """
    Callback function to handle inline buttons of the /language menu for changing the language
    """
    query_data = update.callback_query.data
    lang_id = re.search(r"^lang_([a-z]{2}(?:-[a-z]{2})?)$", query_data).group(1)

    # Inform user about language change
    lang = get_language_info(lang_id)
    lang_changed_text = translate("lang_changed", lang_id).format(lang.get("display_name"))
    update.effective_message.edit_text(text=lang_changed_text, reply_markup=None)

    Database().set_lang_id(lang_id=lang_id, chat_id=update.effective_chat.id)
    logger.debug("Language changed to '{}' for user {}".format(lang_id, update.effective_user.id))
