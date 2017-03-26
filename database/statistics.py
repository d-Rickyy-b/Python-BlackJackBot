# -*- coding: utf-8 -*-
from time import time
from datetime import datetime
from database.db_wrapper import DBwrapper
import logging

__author__ = 'Rico'
logger = logging.getLogger(__name__)


def set_game_won(user_id):
    if user_id > 0:
        db = DBwrapper.get_instance()
        games_won = int(db.get_user(user_id)[6]) + 1
        logger.debug("Add game won for userID: " + str(user_id))
        db.insert("gamesWon", str(games_won), user_id)


def add_game_played(user_id):
    db = DBwrapper.get_instance()
    games_played = int(db.get_played_games(user_id))
    games_played = games_played + 1
    logger.debug("Add game played for userID: " + str(user_id))
    db.insert("gamesPlayed", str(games_played), user_id)
    db.insert("lastPlayed", int(time()), user_id)


def get_stats(percentage):
    text = ""
    perc = int(percentage//10+1)
    for x in range(perc):
        text += "🏆"
    for x in range(10-perc):
        text += "🔴"
    return text


def get_user_stats(user_id):
    db = DBwrapper.get_instance()
    user = db.get_user(user_id)

    played_games = int(user[5])
    if played_games == 0:
        played_games = 1
    statistics_string = "Here are your statistics  📊:\n\nPlayed Games: " + str(played_games) + "\nWon Games : " + str(user[6]) + \
                        "\nLast Played: " + datetime.fromtimestamp(int(user[8])).strftime('%d.%m.%y %H:%M') + " CET" + \
                        "\n\n" + get_stats(round(float(user[6]) / float(played_games), 4) * 100) + "\n\nWinning rate: " + \
                        '{percent:.2%}'.format(percent=float(user[6]) / float(played_games))
    return statistics_string
