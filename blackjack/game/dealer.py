# -*- coding: utf-8 -*-

from game.player import Player


class Dealer(Player):
    credits = 0

    def __init__(self, first_name, deck, join_id=None):
        user_id = -1
        super(Dealer, self).__init__(user_id, first_name, deck, join_id)
