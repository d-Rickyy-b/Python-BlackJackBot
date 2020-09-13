# -*- coding: utf-8 -*-
import unittest
from unittest.mock import Mock

from blackjackbot.commands.game.functions import is_button_affiliated


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


if __name__ == '__main__':
    unittest.main()
