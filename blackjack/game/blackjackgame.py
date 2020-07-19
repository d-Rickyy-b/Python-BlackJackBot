# -*- coding: utf-8 -*-
import logging

from blackjack.errors import PlayerBustedException, GameAlreadyRunningException, GameNotRunningException, MaxPlayersReachedException, \
    PlayerAlreadyExistingException, NotEnoughPlayersException
from blackjack.game import Player, Dealer, Deck, GameType


class BlackJackGame(object):
    MAX_PLAYERS = 5

    def __init__(self, gametype=None, lang_id="en"):
        self.logger = logging.getLogger(__name__)
        self.players = []
        self._current_player = 0
        self.running = False
        self.lang_id = lang_id
        self.deck = Deck(lang_id)
        self.type = gametype or GameType.SINGLEPLAYER
        self.dealer = Dealer("Dealer")

    def start(self):
        """
        Sets up the player's and the dealer's hands
        :return:
        """
        if self.running:
            raise GameAlreadyRunningException

        self.running = True

        # Give every player and the dealer 2 cards
        for player in self.players * 2:
            card = self.deck.pick_one_card()
            player.give_card(card)

    def get_current_player(self):
        return self.players[self._current_player]

    def get_next_player(self):
        return self.players[self._current_player + 1]

    def add_player(self, user_id, first_name, message_id):
        """
        Add a new player to the game as long as it didn't start yet
        :param user_id: The user_id of the player
        :param first_name: The player's first_name
        :param message_id: The id of the message where the user joined
        :return:
        """
        if self.running:
            raise GameAlreadyRunningException("Not adding player, the game is already on!")

        if len(self.players) >= self.MAX_PLAYERS:
            raise MaxPlayersReachedException

        if user_id in [player.user_id for player in self.players]:
            raise PlayerAlreadyExistingException

        # TODO Check if join_id is still needed
        player = Player(user_id, first_name, join_id=message_id)
        self.logger.debug("Adding new player: {}!".format(player))
        self.players.append(player)

    def draw_card(self):
        """
        Draw one card and add it to the player's hand
        :return:
        """
        if not self.running:
            raise GameNotRunningException("The game must be started before you can draw cards")

        player = self.get_current_player()
        card = self.deck.pick_one_card()

        try:
            player.give_card(card)
        except PlayerBustedException:
            self.logger.debug("While giving user {} the card {}, they busted.".format(player.first_name, card))
            raise

    def next_player(self):
        """
        Marks the next player as active player. If all players are finished, go to dealer's turn
        :return:
        """
        if not self.running:
            raise GameNotRunningException("The game must be started before it's the next player's turn")

        if self._current_player != -1 and self._current_player < (len(self.players) - 1):
            pass
        else:
            self.logger.debug("Dealer's turn")
            self._current_player = -1
            #self.dealers_turn()

    def dealers_turn(self):
        if not self.running:
            raise GameNotRunningException("The game must be started before it's the dealer's turn")

        while self.dealer.cardvalue <= 16:
            card = self.deck.pick_one_card()
            self.dealer.give_card(card)

