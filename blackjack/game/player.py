# -*- coding: utf-8 -*-

from game.card import Card

__author__ = 'Rico'


class Player(object):

    def __init__(self, user_id, first_name, join_id, lang_id="en"):
        self.user_id = user_id
        self.first_name = first_name
        self.join_id = join_id
        self.lang_id = lang_id
        self.cardvalue = 0
        self.has_ace = False
        self.cards = []

    def give_card(self, card: Card):
        self.cards.append(card)

        if card.value == 11 and self.cardvalue <= 10:
            self.give_ace()
        elif card.value == 11 and (self.cardvalue + 11) > 21:
            self.cardvalue += 1
            return

        self.cardvalue += card.value

    def give_ace(self):
        self.has_ace = True

    def remove_ace(self):
        self.has_ace = False
        self.cardvalue -= 10

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

    def __repr__(self):
        return "Player: {}, '{}'".format(self.user_id, self.first_name)
