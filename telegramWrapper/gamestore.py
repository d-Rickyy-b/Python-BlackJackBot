# -*- coding: utf-8 -*-
from .errors.noactivegameexception import NoActiveGameException
import logging


class GameStore(object):
    _instance = None
    _initialized = False

    def __new__(cls):
        if GameStore._instance is None:
            GameStore._instance = super(GameStore, cls).__new__(cls)
        return GameStore._instance

    def __init__(self):
        if not self._initialized:
            self._chat_list = {}
            self.logger = logging.getLogger(__name__)
            self._initialized = True

    def add_game(self, chat_id, game):
        if self.has_game(chat_id):
            raise Exception

        game.register_on_stop_handler(self._game_stopped_callback)
        self._chat_list[chat_id] = game

    def get_game(self, chat_id):
        """

        :param chat_id:
        :return:
        """
        # TODO currently players can only have a single game! This should get fixed
        game = self._chat_list.get(chat_id)
        if game is None:
            raise NoActiveGameException
        return game

    def has_game(self, chat_id):
        return chat_id in self._chat_list

    def remove_game(self, chat_id):
        """
        Removes the game of a specific chat from the store
        :param chat_id:
        :return:
        """
        self.logger.debug("Removing game for {}".format(chat_id))
        if chat_id == -1:
            return
        self._chat_list.pop(chat_id)

    def _game_stopped_callback(self, game):
        """
        Callback to remove game from the GameStore
        :param game:
        :return:
        """
        #TODO how to solve this?
        for user in game.players:
            self.remove_game(user.user_id)

        self.logger.debug("Current games: {}".format(len(self._chat_list)))
