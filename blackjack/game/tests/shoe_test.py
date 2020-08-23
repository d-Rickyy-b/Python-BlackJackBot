import unittest
from math import ceil
from unittest.mock import Mock

from blackjack.game import Shoe


class ShoeTest(unittest.TestCase):

    def setUp(self):
        self.shoe = Shoe()

    def test_init(self):
        # test explicit
        shoe = Shoe(decks=4)
        expected_amount = 4 * 52 - 20
        self.assertEqual(expected_amount, len(shoe._cards))

        # test generic
        for i in range(2, 9):
            shoe = Shoe(decks=i)
            expected_amount = ceil((i * 52) * 0.9)
            self.assertEqual(expected_amount, len(shoe._cards))

    def test_draw(self):
        mock_card = Mock()
        self.shoe._cards = [mock_card]
        card = self.shoe.draw()

        self.assertEqual(mock_card, card)

    def test_draw_empty(self):
        self.shoe._cards = []

        with self.assertRaises(IndexError):
            card = self.shoe.draw()


if __name__ == '__main__':
    unittest.main()
