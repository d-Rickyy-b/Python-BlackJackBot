# -*- coding: utf-8 -*-
"""Utility functions for performing chat related tasks"""
import html

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from blackjack.game import BlackJackGame
from blackjackbot.lang import Translator


def remove_inline_keyboard(update, context):
    """
    Removes the inline keyboard for a given message
    :param update: PTB update object
    :param context: PTB context object
    :return:
    """
    if update.effective_message.from_user.id == context.bot.id:
        try:
            update.effective_message.edit_reply_markup(reply_markup=None)
        except Exception:
            # When the message already has no reply markup, simply ignore the exception
            # We can't check for message.reply_markup, because it might have been removed earlier
            pass


def html_mention(user_id, first_name):
    """Generate HTML code that will mention a user in a group"""
    first_name = html.escape(first_name)
    return '<a href="tg://user?id={}">{}</a>'.format(user_id, first_name)


def _get_player_list_string(player_list, dealer_name):
    """
    Generate a string containing a newline separated list of players in the passed list
    :param player_list: A list of players
    :param dealer_name: The localized name of the dealer
    :return:
    """
    players = []
    name_value_template = "{} - {}"

    for player in player_list:
        if player.is_dealer:
            players.append(name_value_template.format(dealer_name, player.cardvalue))
        else:
            players.append(name_value_template.format(player.first_name, player.cardvalue))

    return "\n".join(players)


def _generate_evaluation_string_mp(game, lang_id):
    list_won, list_tie, list_losses = game.evaluation()
    message = ""
    translator = Translator(lang_id)
    dealer_name = translator("dealer_name")

    if len(list_won) > 0:
        message += translator("eval_heading_wins") + "\n"
        message += _get_player_list_string(list_won, dealer_name)

    # 🔃
    if len(list_tie) > 0:
        message += "\n\n{}\n".format(translator("eval_heading_ties"))
        message += _get_player_list_string(list_tie, dealer_name)

    if len(list_losses) > 0:
        message += "\n\n{}\n".format(translator("eval_heading_losses"))
        message += _get_player_list_string(list_losses, dealer_name)

    return message


def _generate_evaluation_string_sp(game, lang_id):
    list_won, list_tie, list_losses = game.evaluation()
    message = ""
    join_str = "\n{} - {}"
    player = game.players[0]
    translator = Translator(lang_id)

    if len(list_won) == 1:
        if game.dealer.busted:
            # Dealer busted, you won
            message += translator("dealer_busted")
        else:
            # Closer to 21
            message += translator("closer_to_21")

        message += "\n"
        message += join_str.format(player.first_name, player.cardvalue)
        message += join_str.format(translator("dealer_name"), game.dealer.cardvalue)
    elif len(list_tie) == 1:
        # Same value as dealer
        message += translator("tied_with_dealer")
        message += "\n"
        message += join_str.format(player.first_name, player.cardvalue)
        message += join_str.format(translator("dealer_name"), game.dealer.cardvalue)
    elif len(list_losses) == 1:
        if player.busted:
            # busted
            message += translator("you_busted")
        elif game.dealer.has_blackjack():
            message += translator("dealer_got_blackjack")
        else:
            message += translator("dealer_got_21")

        message += "\n"
        message += join_str.format(translator("dealer_name"), game.dealer.cardvalue)
        message += join_str.format(player.first_name, player.cardvalue)

    return message


def generate_evaluation_string(game, lang_id):
    if game.type == BlackJackGame.Type.SINGLEPLAYER:
        return _generate_evaluation_string_sp(game, lang_id)
    else:
        return _generate_evaluation_string_mp(game, lang_id)


def get_game_keyboard(game_id, lang_id):
    """Generates a game keyboard translated into the given language
    :param game_id: A unique identifier for each game
    :param lang_id: The language identifier for a specific chat
    :return:
    """
    translator = Translator(lang_id)
    one_more_button = InlineKeyboardButton(text=translator("inline_keyboard_hit"), callback_data="hit_{}".format(game_id))
    no_more_button = InlineKeyboardButton(text=translator("inline_keyboard_stand"), callback_data="stand_{}".format(game_id))
    stop_button = InlineKeyboardButton(text="Stop", callback_data="stop_{}".format(game_id))
    return InlineKeyboardMarkup(inline_keyboard=[[one_more_button, no_more_button]])


def get_join_keyboard(game_id, lang_id):
    """
    Generates a join keyboard translated into the given language
    :param game_id: A unique identifier for each game
    :param lang_id: The language identifier for a specific chat
    :return:
    """
    translator = Translator(lang_id)
    join_button = InlineKeyboardButton(text=translator("inline_keyboard_join"), callback_data="join_{}".format(game_id))
    start_button = InlineKeyboardButton(text=translator("inline_keyboard_start"), callback_data="start_{}".format(game_id))
    return InlineKeyboardMarkup(inline_keyboard=[[join_button, start_button]])


def get_start_keyboard(lang_id):
    translator = Translator(lang_id)
    start_button = InlineKeyboardButton(text=translator("inline_keyboard_start"), callback_data="start")
    return InlineKeyboardMarkup(inline_keyboard=[[start_button]])
