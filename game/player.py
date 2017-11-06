# -*- coding: utf-8 -*-

__author__ = 'Rico'


class Player(object):
    def give_card(self, card, value):
        self.cards.append(card)

        if value == 1 and self.cardvalue <= 10:
            value = 11
            self.give_ace()

        self.cardvalue += value

    def give_ace(self):
        self.has_ace = True

    def remove_ace(self):
        self.has_ace = False
        self.cardvalue -= 10

    def has21(self):
        return self.cardvalue == 21

    def has_busted(self):
        return self.cardvalue > 21

    def has_cards(self):
        return len(self.cards) > 0

    def get_cards_string(self):
        cards_string = ""
        for i, card in enumerate(self.cards):
            cards_string += self.deck.get_card_name(card)
            if i + 1 < len(self.cards):
                cards_string += ", "
        return cards_string

    def get_number_of_cards(self):
        return len(self.cards)

    def get_cardvalue(self):
        return self.cardvalue

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
        self.cardvalue = 0
        self.has_ace = False
        self.cards = []
