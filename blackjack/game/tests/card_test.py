# -*- coding: utf-8 -*-
import unittest

from blackjack.game.card import Card


class CardTest(unittest.TestCase):

    @staticmethod
    def _generate_card(value):
        card = Card(value)
        return card

    def test_creation(self):
        """
        Check that the card is properly created
        :return:
        """
        for multiplier in range(4):
            offset = multiplier * 13
            # Numbers
            for i in range(offset, offset + 9):
                card = self._generate_card(i)
                self.assertEqual(i + 2 - offset, card.value)
                self.assertEqual(i, card.card_id)

            # Jack, Queen, King
            for i in range(offset + 9, offset + 12):
                card = self._generate_card(i)
                self.assertEqual(10, card.value)
                self.assertEqual(i, card.card_id)

            # Ace
            card = self._generate_card(offset + 12)
            self.assertEqual(11, card.value)
            self.assertEqual(offset + 12, card.card_id)

    def test_is_ace(self):
        """
        Check if cards return correct values when they are aces
        :return:
        """
        for i in range(52):
            card = self._generate_card(i)
            if card.value == 11:
                self.assertTrue(card.is_ace())
            else:
                self.assertFalse(card.is_ace())


if __name__ == '__main__':
    unittest.main()
