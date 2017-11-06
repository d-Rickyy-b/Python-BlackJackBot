# -*- coding: utf-8 -*-

from game.card import Card

__author__ = 'Rico'


class Player(object):
    def give_card(self, card: Card):
        self.cards.append(card)
        self.__cardvalue += card.value

        # if value == 1 and self.cardvalue <= 10:
        #     value = 11
        #     self.give_ace()

    def give_ace(self):
        self.has_ace = True

    def remove_ace(self):
        self.has_ace = False
        self.__cardvalue -= 10

    def has_busted(self):
        return self.__cardvalue > 21

    def has_cards(self):
        return len(self.cards) > 0

    def get_cards_string(self):
        cards_string = ""
        for i, card in enumerate(self.cards):
            cards_string += str(card)
            if i + 1 < len(self.cards):
                cards_string += ", "
        return cards_string

    def get_number_of_cards(self):
        return len(self.cards)

    def get_cardvalue(self):
        return self.__cardvalue

    @property
    def first_name(self):
        return self.__first_name

    @property
    def user_id(self):
        return self.__user_id

    @property
    def join_id(self):
        return self.__join_id

    @property
    def lang_id(self):
        return self.__lang_id

    def __init__(self, user_id, first_name, deck, join_id, lang_id="en"):
        self.__user_id = user_id
        self.__first_name = first_name
        self.__join_id = join_id
        self.__lang_id = lang_id
        self.deck = deck
        self.__cardvalue = 0
        self.has_ace = False
        self.cards = []
