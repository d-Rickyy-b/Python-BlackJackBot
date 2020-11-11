# -*- coding: utf-8 -*-
import unittest
from unittest.mock import Mock

from blackjackbot.util import build_menu


class TextutilsTest(unittest.TestCase):

    def test_build_menu_1b_1c(self):
        """Test if splitting up one buttons in one column works as intended"""
        button1 = Mock()
        b = [button1]
        m = build_menu(b, 1)

        # Assert there is a single row
        self.assertEqual(1, len(m))

        # Assert that there is only a single button
        self.assertEqual(1, len(m[0]))

    def test_build_menu_2b_1c(self):
        """Test if splitting up two buttons in one column works as intended"""
        button1 = Mock()
        b = [button1, button1]
        m = build_menu(b, 1)  # Menu has 1 column => 2 rows

        # We have two rows (one button per row)
        self.assertEqual(2, len(m))

    def test_build_menu_2b_2c(self):
        """Test if splitting up two buttons in two columns works as intended"""
        button1 = Mock()
        b = [button1, button1]
        m = build_menu(b, 2)

        # Assert that there is only one row
        self.assertEqual(1, len(m))

        # Assert that first row has 2 buttons
        self.assertEqual(2, len(m[0]))

    def test_build_menu_2b_3c(self):
        """Test if splitting up two buttons in three columns works as intended"""
        button1 = Mock()
        b = [button1, button1]
        m = build_menu(b, 3)  # Menu has 3 columns => 2 rows

        # We have two rows (one button per row)
        self.assertEqual(1, len(m))

        # Assert that first row has 2 buttons
        self.assertEqual(2, len(m[0]))

    def test_build_menu_3(self):
        """Test if splitting up the buttons in several rows works as intended"""
        button1 = Mock()
        b = [button1, button1, button1, button1, button1]
        m = build_menu(b, 2)

        # We have 3 rows
        self.assertEqual(3, len(m))

        # First row has 2 buttons
        self.assertEqual(2, len(m[0]))
        # Second row has 2 buttons
        self.assertEqual(2, len(m[1]))
        # Third row has one button
        self.assertEqual(1, len(m[2]))

    def test_header(self):
        """Test if adding a header button works as intended"""
        button1 = Mock()
        button2 = Mock()
        b = [button1, button1, button1, button1, button1]

        header = button2
        m = build_menu(b, 2, header_buttons=header)

        # Make sure there is only a single header button
        self.assertEqual(1, len(m[0]))

        # Check that this header button is actually the first button of the menu
        self.assertEqual(button2, m[0][0])

    def test_footer(self):
        button1 = Mock()
        button2 = Mock()
        b = [button1, button1, button1, button1, button1]

        footer = button2
        m = build_menu(b, 2, footer_buttons=footer)

        # Make sure there is only a single footer button
        self.assertEqual(1, len(m[-1]))

        # Check that this footer button is actually the last button of the menu
        self.assertEqual(button2, m[-1][0])


if __name__ == '__main__':
    unittest.main()
