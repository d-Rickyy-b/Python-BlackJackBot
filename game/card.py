# -*- coding: utf-8 -*-


class Card(object):
    symbols = ["♥", "♦", "♣", "♠"]
    value_int = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

    @property
    def symbol(self):
        return self.symbols[self.card_id // 13]

    @property
    def value(self):
        return self.value_int[self.card_id % 13]

    @property
    def face(self):
        return self.value_str[self.card_id % 13]

    def __str__(self):
        return "|{} {}|".format(self.symbol, self.face)

    def __init__(self, card_id: int, value_str: list) -> None:
        self.card_id = card_id
        self.value_str = value_str
