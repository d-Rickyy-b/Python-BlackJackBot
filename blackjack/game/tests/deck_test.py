import unittest

from blackjack.game.card import Card
from blackjack.game.deck import Deck


class DeckTest(unittest.TestCase):

    def test_creation(self):
        """
        Check that the deck is properly created
        :return:
        """
        self.deck = Deck()
        self.assertEqual("en", self.deck.lang_id)
        self.assertEqual(52, len(self.deck._deck))

    def test_shuffle(self):
        """
        Check that shuffeling actually changes order of cards
        :return:
        """
        self.deck = Deck()
        d1 = self.deck._deck.copy()

        d2 = self.deck._deck.copy()
        # We check that our two decks we copied are the same
        # This is to proof that the assertNotEqual later on works correctly
        self.assertEqual(d1, d2)

        self.deck._shuffle()
        d3 = self.deck._deck.copy()

        # Just check that we did not lose any cards through shuffeling
        self.assertEqual(52, len(d1))
        self.assertEqual(52, len(d2))
        self.assertEqual(52, len(d3))

        # Our first and third deck should now differ
        # There is a veeeeeery tiny rest probability that after shuffeling the deck is exactly the same as before
        # But we are ignoring that here!
        self.assertNotEqual(d1, d3)

    def test_set_up_deck(self):
        """
        Check if the set up method creates a new sorted deck of cards
        :return:
        """
        self.deck = Deck()
        self.deck._set_up_deck()

        # Check if the deck is sorted (linear ascending numbers)
        for counter in range(52):
            self.assertEqual(counter, self.deck._deck[counter].card_id)

    def test_draw(self):
        """
        Check if drawing cards works as intended
        :return:
        """
        self.deck = Deck()
        self.assertEqual(52, len(self.deck._deck))

        card = self.deck.pick_one_card()

        self.assertEqual(51, len(self.deck._deck))
        self.assertEqual(Card, type(card))

    def test_draw_empty(self):
        """
        Check if drawing works as intended when the deck is empty
        :return:
        """
        pass


if __name__ == '__main__':
    unittest.main()
