# -*- coding: utf-8 -*-
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def html_mention(user_id, first_name):
    """Generate HTML code that will mention a user in a group"""
    # TODO escape user's name
    return '<a href="tg://user?id={}">{}</a>'.format(user_id, first_name)


def generate_evaluation_string(game):
    list_won, list_tie, list_losses = game.evaluation()
    message = ""
    join_str = "{} - {}"

    # TODO maybe only display categories with users in it
    message += "🔰 Wins:\n"
    message += "\n".join([join_str.format(p.first_name, p.cardvalue) for p in list_won])

    #🔃
    message += "\n\n👌 Ties:\n"
    message += "\n".join([join_str.format(p.first_name, p.cardvalue) for p in list_tie])

    message += "\n\n✖️ Losses:\n"
    message += "\n".join([join_str.format(p.first_name, p.cardvalue) for p in list_losses])

    return message


def get_game_keyboard(lang_id=None):
    """Generates a game keyboard translated into the given language
    :param lang_id:
    :return:
    """
    one_more_button = InlineKeyboardButton(text="Hit", callback_data="hit")
    no_more_button = InlineKeyboardButton(text="Stand", callback_data="stand")
    stop_button = InlineKeyboardButton(text="Stop", callback_data="stop")
    return InlineKeyboardMarkup(inline_keyboard=[[one_more_button, no_more_button]])


def get_join_keyboard():
    join_button = InlineKeyboardButton(text="Join", callback_data="join")
    start_button = InlineKeyboardButton(text="Start", callback_data="start")
    return InlineKeyboardMarkup(inline_keyboard=[[join_button, start_button]])


def get_start_keyboard():
    start_button = InlineKeyboardButton(text="Start", callback_data="start")
    return InlineKeyboardMarkup(inline_keyboard=[[start_button]])


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu
