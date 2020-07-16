# -*- coding: utf-8 -*-
from .gametype import GameType
from .deck import CardDeck
from .dealer import Dealer
import logging
from .player import Player
from blackjack.errors import PlayerBustedException

class BlackJackGame(object):
    MAX_PLAYERS = 5

    def __init__(self, gametype=None, lang_id="en"):
        self.logger = logging.getLogger(__name__)
        self.players = []
        self._current_player = 0
        self.running = False
        self.lang_id = lang_id
        self.deck = CardDeck(lang_id)
        self.type = gametype or GameType.SINGLEPLAYER

    def start(self):
        """
        Sets up the player's and the dealer's hands
        :return:
        """
        # Give every player and the dealer 2 cards
        self.running = True

        pass

    def get_current_player(self):
        return self.players[self._current_player]

    def add_player(self, user_id, first_name, message_id, silent=False):
        if self.running:
            self.logger.debug("Not adding player - the game is already on!")
            return

        player = Player(user_id, first_name, join_id=message_id)
        self.logger.debug("Adding new player: {}!".format(player))
        self.players.append(player)

    def draw_card(self):
        """
        Draw one card and add it to the player's hand
        :return:
        """
        if not self.running:
            return

        player = self.get_current_player()
        card = self.deck.pick_one_card()

        try:
            player.give_card(card)
        except PlayerBustedException:
            self.logger.debug("While giving user {} the card {}, they busted.".format(player.first_name, card))

