# -*- coding: utf-8 -*-
import unittest
from datetime import datetime, timedelta

from blackjack.game import BlackJackGame
from blackjackbot.gamestore import GameStore


class GameStoreTest(unittest.TestCase):

    def setUp(self):
        self.game_store = GameStore()

    def _add_game(self, chat_id):
        game = BlackJackGame(gametype=BlackJackGame.Type.MULTIPLAYER_GROUP)
        game.add_player(1, "A")
        game.add_player(2, "B")
        self.game_store.add_game(chat_id, game)
        self.addCleanup(self.game_store.remove_game, chat_id)
        return game

    def test_cleanup_removes_inactive_games(self):
        """Games without activity for longer than the timeout must be removed"""
        game = self._add_game(-1001)
        game.last_activity = datetime.now() - timedelta(minutes=11)

        removed = self.game_store.cleanup_stale_games(stale_timeout_min=10)

        self.assertEqual([-1001], removed)
        self.assertFalse(self.game_store.has_game(-1001))

    def test_cleanup_keeps_old_but_active_games(self):
        """Games that were created long ago but are still being played must not be removed"""
        game = self._add_game(-1002)
        game.datetime_started = datetime.now() - timedelta(minutes=30)
        game.last_activity = datetime.now() - timedelta(minutes=30)
        game.start(1)
        game.next_player()

        removed = self.game_store.cleanup_stale_games(stale_timeout_min=10)

        self.assertEqual([], removed)
        self.assertTrue(self.game_store.has_game(-1002))


if __name__ == '__main__':
    unittest.main()
