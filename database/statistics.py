# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from time import time

from blackjackbot.lang import translate
from database import Database

logger = logging.getLogger(__name__)


def set_game_won(user_id):
    if user_id > 0:
        db = Database()
        user = db.get_user(user_id)
        if user is None:
            logger.warning("User '{}' is None - can't set won games!".format(user))
            return
        games_won = int(user[5]) + 1
        logger.debug("Add game won for user: {}".format(user_id))
        db.set_games_won(games_won, user_id)


def add_game_played(user_id):
    db = Database()
    games_played = db.get_played_games(user_id)
    games_played = games_played + 1
    logger.debug("Add game played for user: {}".format(user_id))
    db.set_games_played(games_played, user_id)
    db.set_last_played(str(int(time())), user_id)


def generate_bar_chart(win_percentage):
    """
    Generate a string of emojis representing a bar (10 chars) that indicates wins vs. losses
    :param win_percentage: The percentage of wins
    :return: Example (55.0%-64.9%) '🏆🏆🏆🏆🏆🏆🔴🔴🔴🔴'
    """
    win_portion = round(win_percentage / 10)
    loss_portion = 10 - win_portion
    return "🏆" * win_portion + "🔴" * loss_portion


def get_user_stats(user_id):
    """
    Generates and returns a string displaying the statistics of a user
    :param user_id: The user_id of a specific user
    :return:
    """
    user = Database().get_user(user_id)

    if user is None:
        logger.warning("User '{}' is not stored in the database!".format(user_id))
        return "No statistics found!"

    lang_id = Database().get_lang_id(user_id)

    try:
        played_games, won_games, _, last_played = user[4:8]
    except ValueError as e:
        logger.warning("Cannot unpack user - {}".format(e))
        raise

    if played_games == 0:
        # prevent division by zero errors
        return translate("no_stats")

    last_played_formatted = datetime.utcfromtimestamp(last_played).strftime('%d.%m.%y %H:%M')
    win_percentage = round(float(won_games) / float(played_games), 4)
    bar = generate_bar_chart(win_percentage * 100)
    template = translate("statistic_template", lang_id)
    statistics_string = template.format(played_games, won_games, last_played_formatted, bar, win_percentage)
    return statistics_string
