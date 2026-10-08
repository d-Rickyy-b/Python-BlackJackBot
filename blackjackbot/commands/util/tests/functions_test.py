# -*- coding: utf-8 -*-
import unittest

from blackjackbot import start_callback_handler
from blackjackbot.commands.util import get_join_keyboard, get_start_keyboard


class CommandsUtilFunctionsTest(unittest.TestCase):

    def test_start_keyboard_matches_start_handler(self):
        """The start button shown when a lobby is full must be handled by the start callback handler"""
        game_id = 1234567
        keyboard = get_start_keyboard(game_id, "en")
        start_button = keyboard.inline_keyboard[0][0]

        self.assertEqual("start_{}".format(game_id), start_button.callback_data)
        self.assertTrue(start_callback_handler.pattern.match(start_button.callback_data))

    def test_join_keyboard_start_button_matches_start_handler(self):
        """The start button of the join keyboard must be handled by the start callback handler"""
        game_id = 7654321
        keyboard = get_join_keyboard(game_id, "en")
        start_button = keyboard.inline_keyboard[0][1]

        self.assertTrue(start_callback_handler.pattern.match(start_button.callback_data))


if __name__ == '__main__':
    unittest.main()
