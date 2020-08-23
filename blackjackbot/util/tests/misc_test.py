import unittest
from unittest.mock import Mock
from blackjack.game import Card
from blackjackbot.util import get_cards_string


class MiscTest(unittest.TestCase):

    def test_get_cards_string_dealer(self):
        player = Mock()
        player.is_dealer = True
        player.turn_over = False
        card = Card(12)  # Heart Ace
        card2 = Card(6)  # Heart eight
        player.cards = [card, card2]

        self.assertEqual("♥ Ace  •  [❔]", get_cards_string(player, "en"))
        self.assertEqual("♥ Ass  •  [❔]", get_cards_string(player, "de"))

        player.cards = [card2, card]

        self.assertEqual("♥ 8  •  [❔]", get_cards_string(player, "en"))
        self.assertEqual("♥ 8  •  [❔]", get_cards_string(player, "de"))

    def test_get_cards_string_dealer_turn_over(self):
        player = Mock()
        player.is_dealer = True
        player.turn_over = True
        card = Card(12)  # Heart Ace
        card2 = Card(6)  # Heart eight
        player.cards = [card, card2]

        self.assertEqual("♥ Ace  •  ♥ 8", get_cards_string(player, "en"))
        self.assertEqual("♥ Ass  •  ♥ 8", get_cards_string(player, "de"))

        player.cards = [card2, card]

        self.assertEqual("♥ 8  •  ♥ Ace", get_cards_string(player, "en"))
        self.assertEqual("♥ 8  •  ♥ Ass", get_cards_string(player, "de"))

    def test_get_cards_string_player(self):
        player = Mock()
        player.is_dealer = False
        player.turn_over = False
        card = Card(11)  # Heart King
        card2 = Card(6)  # Heart eight
        player.cards = [card, card2]

        self.assertEqual("♥ King  •  ♥ 8", get_cards_string(player, "en"))
        self.assertEqual("♥ König  •  ♥ 8", get_cards_string(player, "de"))

        # Changing the turn_over value shouldn't have any effect
        player.turn_over = True
        self.assertEqual("♥ King  •  ♥ 8", get_cards_string(player, "en"))
        self.assertEqual("♥ König  •  ♥ 8", get_cards_string(player, "de"))

    def test_get_cards_string_player_multiple(self):
        player = Mock()
        player.is_dealer = False
        player.turn_over = False
        card = Card(10)  # Heart Queen
        card2 = Card(6)  # Heart eight
        card3 = Card(22)  # Diamond Jack
        player.cards = [card, card2, card3]

        self.assertEqual("♥ Queen  •  ♥ 8  •  ♦ Jack", get_cards_string(player, "en"))
        self.assertEqual("♥ Dame  •  ♥ 8  •  ♦ Bube", get_cards_string(player, "de"))

    def test_get_card_string(self):
        pass


if __name__ == '__main__':
    unittest.main()
