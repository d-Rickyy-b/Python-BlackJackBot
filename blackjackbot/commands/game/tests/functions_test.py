# -*- coding: utf-8 -*-
import unittest
from unittest.mock import Mock, patch

from blackjack.game import BlackJackGame, Card
from blackjackbot.commands.game.functions import is_button_affiliated, next_player
from blackjackbot.gamestore import GameStore


class GameCommandsFunctionsTest(unittest.TestCase):

    def test_is_button_affiliated_positive(self):
        """Check if button assignment is calculated correctly - game.id and data.id are equal"""
        game = Mock()
        game.id = 133769420
        update = Mock()
        update.callback_query = Mock()
        update.callback_query.answer = Mock()
        update.callback_query.data = "start_{}".format(game.id)

        result = is_button_affiliated(update, Mock(), game, "en")
        self.assertTrue(result)

    def test_is_button_affiliated_negative(self):
        """Check if button assignment is calculated correctly - game.id and data.id differ"""
        game = Mock()
        game.id = 420133769
        update = Mock()
        update.callback_query = Mock()
        update.callback_query.answer = Mock()
        update.callback_query.data = "start_133769420"

        result = is_button_affiliated(update, Mock(), game, "en")
        self.assertFalse(result)
        update.callback_query.answer.assert_called_once()

    @patch("blackjackbot.commands.util.decorators.Database")
    @patch("blackjackbot.commands.game.functions.Database")
    def test_next_player_skips_player_with_blackjack(self, db_mock, decorator_db_mock):
        """When the next player was dealt a blackjack, their turn must be skipped even though another user triggered the update"""
        db_mock.return_value.get_lang_id.return_value = "en"
        decorator_db_mock.return_value.get_lang_id.return_value = "en"
        chat_id = -1001234

        game = BlackJackGame(gametype=BlackJackGame.Type.MULTIPLAYER_GROUP)
        game.add_player(1, "A")
        game.add_player(2, "B")
        game.add_player(3, "C")
        game.running = True
        game.players[0]._cards = [Card(0), Card(1)]  # 2 + 3
        game.players[1]._cards = [Card(12), Card(9)]  # Ace + Jack -> blackjack
        game.players[2]._cards = [Card(2), Card(3)]  # 4 + 5
        game.dealer._cards = [Card(8), Card(7)]

        game_store = GameStore()
        game_store.add_game(chat_id, game)
        self.addCleanup(game_store.remove_game, chat_id)

        update = Mock()
        update.effective_chat.id = chat_id
        update.effective_user.id = 1  # Player A presses "stand"

        next_player(update, Mock())

        # B was skipped automatically, so it's now C's turn
        self.assertEqual(game.players[2], game.get_current_player())
        update.callback_query.answer.assert_not_called()


if __name__ == '__main__':
    unittest.main()
