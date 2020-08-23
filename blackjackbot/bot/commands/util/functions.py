# -*- coding: utf-8 -*-
"""Utility functions for performing chat related tasks"""
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
        update.effective_message.edit_reply_markup(reply_markup=None)


def html_mention(user_id, first_name):
    """Generate HTML code that will mention a user in a group"""
    # TODO escape user's name
    return '<a href="tg://user?id={}">{}</a>'.format(user_id, first_name)


def _generate_evaluation_string_mp(game, translator):
    list_won, list_tie, list_losses = game.evaluation()
    message = ""
    join_str = "{} - {}"

    # TODO maybe only display categories with users in it
    if len(list_won) > 0:
        message += translator("eval_heading_wins") + "\n"
        message += "\n".join([join_str.format(p.first_name, p.cardvalue) for p in list_won])

    #🔃
    if len(list_tie) > 0:
        message += "\n\n{}\n".format(translator("eval_heading_ties"))
        message += "\n".join([join_str.format(p.first_name, p.cardvalue) for p in list_tie])

    if len(list_losses) > 0:
        message += "\n\n{}\n".format(translator("eval_heading_losses"))
        message += "\n".join([join_str.format(p.first_name, p.cardvalue) for p in list_losses])

    return message


def _generate_evaluation_string_sp(game, translator):
    list_won, list_tie, list_losses = game.evaluation()
    message = ""
    player_str = ""
    join_str = "\n{} - {}"
    player = game.players[0]

    if len(list_won) == 1:
        if game.dealer.busted:
            # Dealer busted, you won
            message += translator("dealer_busted")
        else:
            # Closer to 21
            message += translator("closer_to_21")

        message += "\n"
        message += join_str.format(player.first_name, player.cardvalue)
        message += join_str.format(game.dealer.first_name, game.dealer.cardvalue)
    elif len(list_tie) == 1:
        # Same value as dealer
        message += translator("tied_with_dealer")
        message += "\n"
        message += join_str.format(player.first_name, player.cardvalue)
        message += join_str.format(game.dealer.first_name, game.dealer.cardvalue)
    elif len(list_losses) == 1:
        if player.busted:
            # busted
            message += translator("you_busted")
        elif game.dealer.has_blackjack():
            message += translator("dealer_got_blackjack")
        else:
            message += translator("dealer_got_21")

        message += "\n"
        message += join_str.format(game.dealer.first_name, game.dealer.cardvalue)
        message += join_str.format(player.first_name, player.cardvalue)

    return message


def generate_evaluation_string(game, translator):
    if game.type == BlackJackGame.Type.SINGLEPLAYER:
        return _generate_evaluation_string_sp(game, translator)
    else:
        return _generate_evaluation_string_mp(game, translator)


def get_game_keyboard(lang_id=None):
    """Generates a game keyboard translated into the given language
    :param lang_id:
    :return:
    """
    translator = Translator(lang_id)
    one_more_button = InlineKeyboardButton(text=translator("inline_keyboard_hit"), callback_data="hit")
    no_more_button = InlineKeyboardButton(text=translator("inline_keyboard_stand"), callback_data="stand")
    stop_button = InlineKeyboardButton(text="Stop", callback_data="stop")
    return InlineKeyboardMarkup(inline_keyboard=[[one_more_button, no_more_button]])


def get_join_keyboard():
    join_button = InlineKeyboardButton(text="Join", callback_data="join")
    start_button = InlineKeyboardButton(text="Start", callback_data="start")
    return InlineKeyboardMarkup(inline_keyboard=[[join_button, start_button]])


def get_start_keyboard():
    start_button = InlineKeyboardButton(text="Start", callback_data="start")
    return InlineKeyboardMarkup(inline_keyboard=[[start_button]])
