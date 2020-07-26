import unittest
from unittest.mock import Mock

from blackjack.game import Player


class PlayerTest(unittest.TestCase):

    def setUp(self):
        self.player = Player(1, "Test", 1)

    @staticmethod
    def _generate_mock_card(value):
        mock_card = Mock()
        mock_card.value = value
        mock_card.is_ace.return_value = (value == 11)
        return mock_card

    def test_player_init(self):
        self.assertEqual(0, self.player.cardvalue)
        self.assertEqual(1, self.player.user_id)
        self.assertEqual("Test", self.player.first_name)
        self.assertEqual(1, self.player.join_id)
        self.assertEqual("en", self.player.lang_id)

    def test_give_card(self):
        """
        Check if giving a player a card will store the card in the player object
        :return:
        """
        self.player.give_card(self._generate_mock_card(10))
        self.assertEqual(1, len(self.player.cards))

        self.player.give_card(self._generate_mock_card(11))
        self.assertEqual(2, len(self.player.cards))

        self.player.give_card(self._generate_mock_card(10))
        self.assertEqual(3, len(self.player.cards))

    def test_set_cardvalue(self):
        """
        Check if trying to set the cardvalue will raise an AttributeError
        :return:
        """
        with self.assertRaises(AttributeError):
            self.player.cardvalue = 2

    def test_cardvalue(self):
        """
        Check if the cardvalue method returns a correct results for regular (non ace/K/Q/J) card values
        :return:
        """
        self.player.give_card(self._generate_mock_card(10))
        self.assertEqual(10, self.player.cardvalue)

        self.player.give_card(self._generate_mock_card(9))
        self.assertEqual(19, self.player.cardvalue)

    def test_cardvalue_ace(self):
        """
        Check if several aces will be calculated correctly (A+A+A+A+5+2 = 21)
        :return:
        """
        self.player.give_card(self._generate_mock_card(11))
        self.assertEqual(11, self.player.cardvalue)

        self.player.give_card(self._generate_mock_card(11))
        self.assertEqual(12, self.player.cardvalue)

        self.player.give_card(self._generate_mock_card(11))
        self.assertEqual(13, self.player.cardvalue)

        self.player.give_card(self._generate_mock_card(11))
        self.assertEqual(14, self.player.cardvalue)

        self.player.give_card(self._generate_mock_card(5))
        self.assertEqual(19, self.player.cardvalue)

        self.player.give_card(self._generate_mock_card(2))
        self.assertEqual(21, self.player.cardvalue)

    def test_cardvalue_ace2(self):
        """
        Check if several aces will be calculated correctly (A+A+A+5 = 18)
        :return:
        """
        self.player.give_card(self._generate_mock_card(11))
        self.assertEqual(11, self.player.cardvalue)

        self.player.give_card(self._generate_mock_card(11))
        self.assertEqual(12, self.player.cardvalue)

        self.player.give_card(self._generate_mock_card(11))
        self.assertEqual(13, self.player.cardvalue)

        self.player.give_card(self._generate_mock_card(5))
        self.assertEqual(18, self.player.cardvalue)

    def test_cardvalue_soft_hand(self):
        """
        Check if aces are correctly calculated in soft hands (5+A+3 = 19)
        :return:
        """
        self.player.give_card(self._generate_mock_card(5))
        self.assertEqual(5, self.player.cardvalue)

        self.player.give_card(self._generate_mock_card(11))
        self.assertEqual(16, self.player.cardvalue)

        self.player.give_card(self._generate_mock_card(3))
        self.assertEqual(19, self.player.cardvalue)

    def test_cardvalue_soft_hand_bj(self):
        """
        Check if black jacks are calculated correctly (10+A = 21/BJ)
        :return:
        """
        self.player.give_card(self._generate_mock_card(10))
        self.assertEqual(10, self.player.cardvalue)

        self.player.give_card(self._generate_mock_card(11))
        self.assertEqual(21, self.player.cardvalue)

    def test_cardvalue_hard_hand(self):
        """
        Check if a hard hand gets calculated correctly (8+A+2 == 21 hard hand)
        :return:
        """
        self.player.give_card(self._generate_mock_card(8))
        self.assertEqual(8, self.player.cardvalue)

        self.player.give_card(self._generate_mock_card(11))
        self.assertEqual(19, self.player.cardvalue)

        self.player.give_card(self._generate_mock_card(2))
        self.assertEqual(21, self.player.cardvalue)

    def test_cardvalue_hard_hand2(self):
        """
        Check if a hard hand gets calculated correctly (8+5+A == 14 hard hand)
        :return:
        """
        self.player.give_card(self._generate_mock_card(8))
        self.assertEqual(8, self.player.cardvalue)

        self.player.give_card(self._generate_mock_card(5))
        self.assertEqual(13, self.player.cardvalue)

        self.player.give_card(self._generate_mock_card(11))
        self.assertEqual(14, self.player.cardvalue)

    def test_cardvalue_busted_wo_ace(self):
        """
        Check if a correct value will be returned if the player busted without an ace
        :return:
        """
        self.player.give_card(self._generate_mock_card(8))
        self.assertEqual(8, self.player.cardvalue)

        self.player.give_card(self._generate_mock_card(5))
        self.assertEqual(13, self.player.cardvalue)

        self.player.give_card(self._generate_mock_card(10))
        self.assertEqual(23, self.player.cardvalue)

    def test_cardvalue_busted_w_ace(self):
        """
        Check if a correct value will be returned if the player busted with an ace
        :return:
        """
        self.player.give_card(self._generate_mock_card(8))
        self.assertEqual(8, self.player.cardvalue)

        self.player.give_card(self._generate_mock_card(11))
        self.assertEqual(19, self.player.cardvalue)

        self.player.give_card(self._generate_mock_card(10))
        self.assertEqual(19, self.player.cardvalue)

        self.player.give_card(self._generate_mock_card(5))
        self.assertEqual(24, self.player.cardvalue)

    def test_get_cards_string(self):
        pass
        # mock = self._generate_mock_card(8)
        # mock.__str__.return_value = ""
        # self.player.give_card()
        # print(self.player.get_cards_string())

    def test_amount_of_cards(self):
        """
        Check if the number of cards is calculated correctly
        :return:
        """
        self.assertEqual(0, self.player.amount_of_cards)

        self.player.give_card(self._generate_mock_card(10))
        self.assertEqual(10, self.player.cardvalue)

        self.assertEqual(1, self.player.amount_of_cards)

        self.player.give_card(self._generate_mock_card(9))
        self.assertEqual(19, self.player.cardvalue)

        self.assertEqual(2, self.player.amount_of_cards)


if __name__ == '__main__':
    unittest.main()
