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
        card = self._generate_card(0)
        self.assertEqual(11, card.value)
        self.assertEqual(0, card.card_id)

        card = self._generate_card(1)
        self.assertEqual(2, card.value)
        self.assertEqual(1, card.card_id)

        card = self._generate_card(2)
        self.assertEqual(3, card.value)
        self.assertEqual(2, card.card_id)

        card = self._generate_card(3)
        self.assertEqual(4, card.value)
        self.assertEqual(3, card.card_id)

        card = self._generate_card(4)
        self.assertEqual(5, card.value)
        self.assertEqual(4, card.card_id)

        card = self._generate_card(5)
        self.assertEqual(6, card.value)
        self.assertEqual(5, card.card_id)

        card = self._generate_card(6)
        self.assertEqual(7, card.value)
        self.assertEqual(6, card.card_id)

        card = self._generate_card(7)
        self.assertEqual(8, card.value)
        self.assertEqual(7, card.card_id)

        card = self._generate_card(8)
        self.assertEqual(9, card.value)
        self.assertEqual(8, card.card_id)

        card = self._generate_card(9)
        self.assertEqual(10, card.value)
        self.assertEqual(9, card.card_id)

        card = self._generate_card(10)
        self.assertEqual(10, card.value)
        self.assertEqual(10, card.card_id)

        card = self._generate_card(11)
        self.assertEqual(10, card.value)
        self.assertEqual(11, card.card_id)

        card = self._generate_card(12)
        self.assertEqual(10, card.value)
        self.assertEqual(12, card.card_id)

        card = self._generate_card(13)
        self.assertEqual(11, card.value)
        self.assertEqual(13, card.card_id)

        card = self._generate_card(14)
        self.assertEqual(2, card.value)
        self.assertEqual(14, card.card_id)

    def test_is_ace(self):
        """
        Check if cards return correct values when they are aces
        :return:
        """
        card = self._generate_card(0)
        self.assertEqual(11, card.value)
        self.assertTrue(card.is_ace())

        card = self._generate_card(1)
        self.assertFalse(card.is_ace())

        card = self._generate_card(2)
        self.assertFalse(card.is_ace())

        card = self._generate_card(3)
        self.assertFalse(card.is_ace())

        card = self._generate_card(4)
        self.assertFalse(card.is_ace())

        card = self._generate_card(5)
        self.assertFalse(card.is_ace())

        card = self._generate_card(6)
        self.assertFalse(card.is_ace())

        card = self._generate_card(7)
        self.assertFalse(card.is_ace())

        card = self._generate_card(8)
        self.assertFalse(card.is_ace())

        card = self._generate_card(9)
        self.assertFalse(card.is_ace())

        card = self._generate_card(10)
        self.assertFalse(card.is_ace())

        card = self._generate_card(11)
        self.assertFalse(card.is_ace())

        card = self._generate_card(12)
        self.assertFalse(card.is_ace())

        card = self._generate_card(13)
        self.assertTrue(card.is_ace())

        card = self._generate_card(14)
        self.assertFalse(card.is_ace())


if __name__ == '__main__':
    unittest.main()
