# -*- coding: utf-8 -*-
import unittest

from blackjack.game.card import Card


class CardTest(unittest.TestCase):

    @staticmethod
    def _generate_card(value):
        val_str = []
        card = Card(value, val_str)
        return card

    def test_creation(self):
        """
        Check that the card is properly created
        :return:
        """
        card = self._generate_card(1)

        self.assertEqual(1, card.value)

    def test_is_ace(self):
        """
        Check that shuffeling actually changes order of cards
        :return:
        """
        pass


if __name__ == '__main__':
    unittest.main()
