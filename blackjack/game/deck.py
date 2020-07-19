# -*- coding: utf-8 -*-

from random import shuffle

from .card import Card
from lang.language import translate

__author__ = 'Rico'


class Deck(object):

    def __init__(self, lang_id="en"):
        self.lang_id = lang_id
        self.value_str = [translate("ace", lang_id), "2", "3", "4", "5", "6", "7", "8", "9", "10",
                          translate("jack", lang_id), translate("queen", lang_id), translate("king", lang_id)]
        self._deck = []
        self._set_up_deck()
        self._shuffle()

    def _set_up_deck(self):
        self._deck = []

        for card_id in range(52):
            card = Card(card_id, self.value_str)
            self._deck.append(card)

    def _shuffle(self):
        shuffle(self._deck)

    def pick_one_card(self):
        # TODO if len(self._deck) <= 0, then raise error
        return self._deck.pop(0)
