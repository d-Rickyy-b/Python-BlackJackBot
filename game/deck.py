# -*- coding: utf-8 -*-

from lang.language import translate

__author__ = 'Rico'


class CardDeck(object):
    symbols = ["♥", "♦", "♣", "♠"]
    valueInt = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

    @staticmethod
    def create_deck():
        from random import shuffle
        deck = list(range(1, 52))
        shuffle(deck)
        return deck[:]

    def pick_one_card(self):
        card = self.deck[0]
        self.deck.pop(0)
        return card

    def get_card_name(self, card):
        symbol = self.symbols[card // 13]
        value = self.value_str[card % 13]
        card_name = "|" + symbol + " " + value + "|"
        return card_name

    def get_card_value(self, card):
        return self.valueInt[card % 13]

    def __init__(self, lang_id):
        self.deck = self.create_deck()
        self.value_str = [translate("ace", lang_id), "2", "3", "4", "5", "6", "7", "8", "9", "10",
                          translate("jack", lang_id), translate("queen", lang_id), translate("king", lang_id)]
