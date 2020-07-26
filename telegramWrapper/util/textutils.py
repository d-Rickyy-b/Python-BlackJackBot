# -*- coding: utf-8 -*-


def html_mention(user_id, first_name):
    """Generate HTML code that will mention a user in a group"""
    return '<a href="tg://user?id={}">{}</a>'.format(user_id, first_name)
