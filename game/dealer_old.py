# -*- coding: utf-8 -*-

from game.player_old import Player


class Dealer(Player):
    credits = 0

    def __init__(self, first_name, join_id=None):
        super(Dealer, self).__init__(user_id=-1, first_name=first_name, join_id=join_id)
