# -*- coding: utf-8 -*-
from enum import Enum


class Card(object):

    class Type(Enum):
        NUMBER = "card_number"
        JACK = "card_jack"
        QUEEN = "card_queen"
        KING = "card_king"
        ACE = "card_ace"

    symbols = ["♥", "♦", "♣", "♠"]
    value_str = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]

    def __init__(self, card_id):
        self.card_id = card_id

    def is_ace(self):
        return self.value == 11

    @property
    def symbol(self):
        return self.symbols[self.card_id // 13]

    @property
    def value(self):
        values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
        return values[self.card_id % 13]

    @property
    def face(self):
        return self.value_str[self.card_id % 13]

    @property
    def type(self):
        if (self.card_id % 13) in range(0, 9):
            return Card.Type.NUMBER
        elif (self.card_id % 13) == 9:
            return Card.Type.JACK
        elif (self.card_id % 13) == 10:
            return Card.Type.QUEEN
        elif (self.card_id % 13) == 11:
            return Card.Type.KING
        elif (self.card_id % 13) == 12:
            return Card.Type.ACE
        else:
            raise ValueError("card_id '{}' can't be mapped to card type!".format(self.card_id))

    @property
    def str_id(self):
        str_ids = ["card_2", "card_3", "card_4", "card_5", "card_6",
                   "card_7", "card_8", "card_9", "card_10",
                   "card_jack", "card_queen", "card_king", "card_ace"]
        return str_ids[self.card_id % 13]

    def __str__(self):
        return "{} {}".format(self.symbol, self.face)

    def __repr__(self):
        return self.__str__()
