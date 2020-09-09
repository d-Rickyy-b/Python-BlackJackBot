# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from time import time

from database import Database

__author__ = 'Rico'
logger = logging.getLogger(__name__)


def set_game_won(user_id):
    if user_id > 0:
        db = Database()
        games_won = int(db.get_user(user_id)[6]) + 1
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
    db = Database()
    user = db.get_user(user_id)

    played_games = int(user[5])
    if played_games == 0:
        played_games = 1
    statistics_string = "Here are your statistics  📊:\n\nPlayed Games: " + str(played_games) + "\nWon Games : " + str(user[6]) + \
                        "\nLast Played: " + datetime.fromtimestamp(int(user[8])).strftime('%d.%m.%y %H:%M') + " CET" + \
                        "\n\n" + get_stats(round(float(user[6]) / float(played_games), 4) * 100) + "\n\nWinning rate: " + \
                        '{percent:.2%}'.format(percent=float(user[6]) / float(played_games))
    return statistics_string
