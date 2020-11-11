# -*- coding: utf-8 -*-
# Reference: https://en.wikipedia.org/wiki/Shoe_(cards)
from random import shuffle
from math import floor

from .deck import Deck


class Shoe(object):
    # Represents a dealing shoe (holder of several decks)

    def __init__(self, decks=4):
        self._cards = []
        self.deck_amount = decks
        for _ in range(decks):
            deck = Deck()
            self._cards.extend(deck.cards)
        # Shuffle the full shoe again
        shuffle(self._cards)

        cut_amount = floor(len(self._cards) * 0.1)
        cut_card = len(self._cards) - cut_amount
        self._cards = self._cards[:cut_card]

    def draw(self):
        """
        Draw a card from the shoe
        :return:
        """
        try:
            card = self._cards.pop()
            return card
        except IndexError:
            # TODO implement custom error
            raise
