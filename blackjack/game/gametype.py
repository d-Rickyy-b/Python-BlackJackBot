# -*- coding: utf-8 -*-
from enum import Enum


class GameType(Enum):
    """
    Enum describing the type of a game
    """
    SINGLEPLAYER = 1
    MULTIPLAYER_GROUP = 2
    MULTIPLAYER_DIRECT = 3
