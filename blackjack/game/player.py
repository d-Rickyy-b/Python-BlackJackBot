# -*- coding: utf-8 -*-

from .card import Card

__author__ = 'Rico'


class Player(object):

    def __init__(self, user_id, first_name, lang_id="en"):
        """

        """
        self.is_dealer = False
        self._cards = []
        self.turn_over = False

        self.user_id = user_id
        self.first_name = first_name
        self.lang_id = lang_id
        self.has_ace = False

    def give_card(self, card: Card):
        self._cards.append(card)

    @property
    def busted(self):
        return self.cardvalue > 21

    @property
    def cardvalue(self):
        """
        Calculate the current value of the cards on the hand
        :return: Current value of the cards on the hand
        """
        value = 0
        ace_counter = 0

        for card in self._cards:
            if card.is_ace():
                # if we encounter an ace, we don't calculate it yet
                ace_counter += 1
            else:
                # If no ace we simply add the value to the total
                value += card.value

        if ace_counter == 0:
            return value

        possible_values = set()

        # We now calculate all the possible values combinations of the cards + aces
        for i in range(ace_counter + 1):
            possible_values.add(value + (i * 11) + ((ace_counter - i) * 1))

        possible_values_list = list(possible_values)
        # Sort the list so that we can later on work with returning the first/last element of a list without checking actual values again
        possible_values_list.sort()

        # Split up the results into two list for easier handling
        lower_21 = [i for i in possible_values_list if i <= 21]
        bigger_21 = [i for i in possible_values_list if i > 21]

        # If we have an ace, we want to return the biggest value below 21 (is possible).
        if len(lower_21) >= 1:
            return lower_21[-1]

        # If there is no such value we want to return the lowest value above 21
        if len(bigger_21) >= 1:
            return bigger_21[0]

        raise ValueError

    def get_cards_string(self):
        return '  •  '.join(str(card) for card in self._cards)

    @property
    def amount_of_cards(self):
        return len(self._cards)

    def has_blackjack(self):
        return self.cardvalue == 21 and self.amount_of_cards == 2

    def has_21(self):
        return self.cardvalue == 21

    def __repr__(self):
        return "Player: {}, '{}'".format(self.user_id, self.first_name)
