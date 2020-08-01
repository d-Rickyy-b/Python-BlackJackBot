# -*- coding: utf-8 -*-

from .player import Player


class Dealer(Player):
    credits = 0

    def __init__(self, first_name):
        super().__init__(user_id=-1, first_name=first_name)
        self.is_dealer = True

    def get_cards_string(self):
        if not self.turn_over:
            return "{}  •  [❔]". format(str(self._cards[0]))
        return super().get_cards_string()
