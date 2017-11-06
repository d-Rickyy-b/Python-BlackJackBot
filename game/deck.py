# -*- coding: utf-8 -*-

from random import shuffle

from game.card import Card

__author__ = 'Rico'


class CardDeck(object):
    def create_deck(self) -> list:
        deck = []

        for card_id in range(1, 52):
            deck.append(Card(card_id, self.lang_id))

        shuffle(deck)
        return deck[:]

    def pick_one_card(self) -> Card:
        return self.deck.pop(0)

    def __init__(self, lang_id: str) -> None:
        self.lang_id = lang_id
        self.deck = self.create_deck()
