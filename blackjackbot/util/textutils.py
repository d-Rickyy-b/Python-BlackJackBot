# -*- coding: utf-8 -*-
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def html_mention(user_id, first_name):
    """Generate HTML code that will mention a user in a group"""
    # TODO escape user's name
    return '<a href="tg://user?id={}">{}</a>'.format(user_id, first_name)


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu
