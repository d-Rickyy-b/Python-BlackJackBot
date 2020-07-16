# -*- coding: utf-8 -*-
from enum import Enum


class GameType(Enum):
    """
    Enum describing the type of a game
    """
    SINGLEPLAYER = 1
    MULTIPLAYER = 2
