# -*- coding: utf-8 -*-
import unittest
from unittest.mock import Mock, patch

from blackjack.game import BlackJackGame
from blackjackbot.commands.game.commands import join_callback, start_cmd
from blackjackbot.gamestore import GameStore


class GameCommandsTest(unittest.TestCase):

    @patch("blackjackbot.commands.util.decorators.Database")
    @patch("blackjackbot.commands.game.commands.Database")
    def test_join_callback_stores_user(self, db_mock, decorator_db_mock):
        """Players joining a group game via the join button must be stored in the database, so their stats are tracked"""
        db_mock.return_value.get_lang_id.return_value = "en"
        decorator_db_mock.return_value.get_lang_id.return_value = "en"
        chat_id = -1004321

        game = BlackJackGame(gametype=BlackJackGame.Type.MULTIPLAYER_GROUP)
        game.add_player(1, "A")

        game_store = GameStore()
        game_store.add_game(chat_id, game)
        self.addCleanup(game_store.remove_game, chat_id)

        update = Mock()
        update.effective_chat.id = chat_id
        update.effective_user.id = 2
        update.effective_user.first_name = "B"
        update.effective_user.last_name = "Bee"
        update.effective_user.username = "bbb"
        update.effective_user.language_code = "de"
        update.callback_query.data = "join_{}".format(game.id)

        join_callback(update, Mock())

        self.assertEqual(2, len(game.players))
        db_mock.return_value.add_user.assert_called_once_with(2, "de", "B", "Bee", "bbb")

    @patch("blackjackbot.commands.game.commands.create_game")
    @patch("blackjackbot.commands.game.commands.Database")
    def test_start_cmd_uses_telegram_language(self, db_mock, create_game_mock):
        """Starting a game must store the user's Telegram language for the chat before the game is created"""
        chat_id = -1001234

        update = Mock()
        update.effective_chat.id = chat_id
        update.effective_user.id = 2
        update.effective_user.first_name = "B"
        update.effective_user.last_name = "Bee"
        update.effective_user.username = "bbb"
        update.effective_user.language_code = "de"

        create_game_mock.side_effect = lambda *args: db_mock.return_value.set_default_lang_id.assert_called_once_with(chat_id, "de")
        start_cmd(update, Mock())

        create_game_mock.assert_called_once()


if __name__ == '__main__':
    unittest.main()
