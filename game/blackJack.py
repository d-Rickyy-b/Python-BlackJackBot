# -*- coding: utf-8 -*-

from database.statistics import add_game_played, set_game_won
from game.player import Player

__author__ = 'Rico'


class BlackJack(object):
    GROUP_CHAT = 1
    PRIVATE_CHAT = 0
    game_running = False
    current_player = 0

    # Adds Player to the Game
    def add_player(self, user_id, first_name, message_id, silent=None):
        player = Player(user_id, first_name, self.deck)
        self.players.append(player)

        # send a message with: self.translate("playerJoined").format(first_name)

    def get_index_by_user_id(self, user_id):
        pass

    def get_user_by_user_id(self, user_id):
        for user in self.players:
            if user.get_userid() == user_id:
                return user

        return None

    def next_player(self):
        pass

    # gives player one card
    def give_player_one(self):
        pass

    def players_first_turn(self):
        pass

    # Gives the dealer cards
    def dealers_turn(self, i=0):
        pass

    def dealers_first_turn(self):
        pass

    # Only in multiplayer
    def start_game(self, message_id):
        self.game_running = True

        self.dealers_first_turn()
        for p in self.players:
            add_game_played(p.user_id)
        self.players_first_turn()

        # ---------------------------------- Auswertung -----------------------------------------#

    def evaluation(self):
        pass

    # ---------------------------------- Get Player overview -----------------------------------------#

    def get_player_overview(self, show_points=False, text="", i=0, dealer=False):
        for user in self.players:
            if i == self.current_player:
                text += "▶️"
            else:
                text += "👤"
            if show_points is True and (i < self.current_player or self.current_player == -1):
                text += (user.first_name + " - [" + str(self.players[i].cardvalue) + "]\n")
            else:
                text += (user.first_name + "\n")
            i += 1
        if dealer is True:
            text += ("🎩" + self.translate("dealerName") + " - [" + str(self.dealer.get_cardvalue()) + "]")
        return text

    # Messages are analyzed here. Most function calls come from here
    def analyze_message(self, command, user_id, first_name, message_id):
        pass

    # When game is being initialized
    def __init__(self, chat_id, user_id, lang_id, game_type, first_name, gamehandler, message_id, bot):
        self.players = []

    # When game is being ended - single and multiplayer
    def __del__(self):
        pass
