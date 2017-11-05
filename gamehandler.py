# -*- coding: utf-8 -*-

import random
import string
from typing import Optional

from game.blackJackGame import BlackJackGame

__author__ = 'Rico'


# game_handler handles the blackJack-game-objects. When a new object is created, it is saved in "GameList"
# get_index_by_chatid returns the index of a running game in the list
class GameHandler(object):
    GameList = []  # List, where the running Games are stored in

    def gl_create(self) -> None:
        self.GameList = []

    def gl_remove(self, chat_id: int) -> None:
        index = self.get_index_by_chatid(chat_id)
        if index is None:
            return
        if not index < 0:
            self.GameList.pop(index)

    def add_game(self, blackjackgame) -> None:
        self.GameList.append(blackjackgame)

    def get_index_by_chatid(self, chat_id: int) -> Optional[int]:
        for index, game in enumerate(self.GameList):
            if game.chat_id == chat_id:
                return index
            else:
                for player in game.players:
                    if player.user_id == chat_id:
                        return index

        return None

    def get_game_by_chatid(self, chat_id: int) -> Optional[BlackJackGame]:
        index = self.get_index_by_chatid(chat_id)
        if index is None:
            return None
        return self.GameList[index]

    def get_game_by_index(self, index: int) -> BlackJackGame:
        return self.GameList[index]

    def get_game_by_id(self, game_id: int) -> Optional[BlackJackGame]:
        if game_id is None:
            return None
        for game in self.GameList:
            if game.get_game_id() == game_id:
                return game
        return None

    def generate_id(self) -> str:
        game_id = ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(8))

        while self.id_already_existing(game_id):
            print("ID already existing: " + str(game_id))
            game_id = ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(8))

        return game_id

    def id_already_existing(self, game_id: str) -> bool:
        for game in self.GameList:
            if game.get_game_id() == game_id:
                return True

        return False

    def __init__(self):
        self.GameList = []
