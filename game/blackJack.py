# -*- coding: utf-8 -*-
import logging

from telegram.keyboardbutton import KeyboardButton
from telegram.replykeyboardhide import ReplyKeyboardHide
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup

from database.statistics import add_game_played, set_game_won
from game.cardDeck import CardDeck
from game.dealer import Dealer
from game.player import Player
from lang.language import translate

__author__ = 'Rico & Julian'


class BlackJack(object):
    PRIVATE_CHAT = 0
    GROUP_CHAT = 1
    MULTIPLAYER_GAME = 2
    MAX_PLAYERS = 5

    # Adds Player to the Game
    def add_player(self, user_id, first_name, message_id, silent=None):
        if not self.game_running:
            if self.get_index_by_user_id(user_id) is None and len(self.players) < self.MAX_PLAYERS:
                self.logger.debug("Adding user '" + first_name + "' to players.")
                player = Player(user_id, first_name, self.deck)
                self.players.append(player)
                self.join_message_ids.append(message_id)

                if silent is None or silent is False:
                    # TODO When game is multiplayer then print current players?
                    self.send_message(self.chat_id, translate("playerJoined", self.lang_id).format(first_name), message_id=message_id, game_id=self.__game_id)
            else:
                self.logger.debug("User '" + first_name + "' already in player list. Or max players reached")

    def get_index_by_user_id(self, user_id):
        for index, user in enumerate(self.players):
            if user.get_userid() == user_id:
                return index

        return None

    def get_user_by_user_id(self, user_id):
        for user in self.players:
            if user.get_userid() == user_id:
                return user
        return None

    def next_player(self):
        if self.game_running:
            if self.current_player is not None and self.current_player < (len(self.players) - 1):
                self.logger.debug("Next Player!")
                self.current_player += 1
                self.send_message(self.chat_id, translate("overview", self.lang_id) + "\n\n" + self.get_player_overview(show_points=True) + "\n" +
                                  translate("nextPlayer", self.lang_id).format(self.players[self.current_player].get_first_name()),
                                  message_id=self.join_message_ids[self.current_player], reply_markup=self.keyboard_running, game_id=self.__game_id)

                self.give_player_one()
            else:
                self.logger.debug("Dealer's turn")
                self.current_player = None
                self.dealers_turn()

    # gives player one card
    def give_player_one(self):
        if self.game_running:
            player_index = self.current_player
            user = self.players[player_index]
            self.logger.debug("Giving player one card | chatID: " + str(self.chat_id) + " | player: " + user.get_first_name())

            if user.get_number_of_cards() == 0:
                # give user 2 cards at beginning
                for i in range(2):
                    card = self.deck.pick_one_card()
                    cardvalue = self.deck.get_card_value(card)

                    user.give_card(card, cardvalue)

                # TODO check if cardvalue = 21. If yes, mention it in the message
                cards_string = "\n" + user.get_cards_string() + "\n"
                self.send_message(self.chat_id, str(translate("yourCardsAre", self.lang_id).format(
                    user.first_name, cards_string, str(user.cardvalue))), reply_markup=self.keyboard_running,
                                  message_id=self.join_message_ids[self.current_player], game_id=self.__game_id)
            else:
                card = self.deck.pick_one_card()
                cardvalue = self.deck.get_card_value(card)

                if user.has_ace and (user.cardvalue + cardvalue > 21):
                    # user got an ace
                    cardvalue = 1
                    user.remove_ace()
                    self.send_message(self.chat_id, translate("softHandLater", self.lang_id), game_id=self.__game_id)

                if self.game_type == self.PRIVATE_CHAT:
                    player_drew = translate("playerDraws1", self.lang_id).format(str(self.deck.get_card_name(card)))
                else:
                    player_drew = translate("playerDrew", self.lang_id).format(user.first_name, str(self.deck.get_card_name(card)))

                user.give_card(card, cardvalue)

                player_drew += "\n" + translate("cardvalue", self.lang_id).format(str(user.cardvalue))

                if user.cardvalue >= 21:
                    if user.cardvalue > 21:
                        if self.game_type == self.GROUP_CHAT:
                            player_drew += "\n\n" + translate("playerBusted", self.lang_id).format(user.first_name)

                    elif user.cardvalue == 21:
                        player_drew += "\n\n" + user.first_name + " " + translate("got21", self.lang_id)

                    self.send_message(self.chat_id, text=player_drew, game_id=self.__game_id)
                    self.next_player()
                else:
                    self.send_message(self.chat_id, text=player_drew, reply_markup=self.keyboard_running, game_id=self.__game_id)

    # Gives the dealer cards
    def dealers_turn(self):
        if self.dealer.get_number_of_cards() < 2:
            for i in range(2):
                card = self.deck.pick_one_card()
                cardvalue = self.deck.get_card_value(card)
                self.dealer.give_card(card, cardvalue)

            text = ""
            if self.game_type == self.PRIVATE_CHAT:
                text += translate("gameBegins", self.lang_id) + "\n"

            text += "\n*" + translate("dealersCards", self.lang_id) + "*\n\n" + self.deck.get_card_name(card) + ", | -- |"
            self.send_message(self.chat_id, text, parse_mode="Markdown", reply_markup=self.keyboard_running)
        else:
            output_text = translate("croupierDrew", self.lang_id) + "\n\n"

            while self.dealer.get_cardvalue() <= 16:
                card = self.deck.pick_one_card()
                cardvalue = self.deck.get_card_value(card)
                self.dealer.give_card(card, cardvalue)

            i = 0
            for card in self.dealer.cards:
                if i == 0:
                    output_text += self.deck.get_card_name(card)
                else:
                    output_text += " , " + self.deck.get_card_name(card)
                i += 1

            output_text += "\n\n" + translate("cardvalueDealer", self.lang_id) + " " + str(self.dealer.get_cardvalue())
            self.send_message(self.chat_id, output_text, parse_mode="Markdown", reply_markup=self.keyboard_running)
            self.evaluation()

    def start_game(self, message_id=None):
        if ((self.game_type == self.GROUP_CHAT or self.game_type == self.MULTIPLAYER_GAME) and len(self.players) >= 1) or self.game_type == self.PRIVATE_CHAT:
            if not self.game_running:
                self.game_running = True

                for player in self.players:
                    add_game_played(player.user_id)

                if self.game_type == self.GROUP_CHAT or self.game_type == self.MULTIPLAYER_GAME:
                    self.send_message(self.chat_id, translate("gameBegins", self.lang_id) + "\n" + translate("gameBegins2", self.lang_id) + "\n\n" + self.get_player_overview(), game_id=self.__game_id)

                self.dealers_turn()
                self.give_player_one()
        else:
            self.send_message(self.chat_id, translate("notEnoughPlayers", self.lang_id), message_id=message_id, game_id=self.__game_id)

    def evaluation(self):
        list_21 = []
        list_busted = []
        list_lower_21 = []

        for user in self.players:
            cv = user.get_cardvalue()

            if cv > 21:
                list_busted.append(user)
            elif cv == 21:
                list_21.append(user)
            elif cv < 21:
                list_lower_21.append(user)

        if self.dealer.get_cardvalue() > 21:
            list_busted.append(self.dealer)
        elif self.dealer.get_cardvalue() == 21:
            list_21.append(self.dealer)
        elif self.dealer.get_cardvalue() < 21:
            list_lower_21.append(self.dealer)

        list_21 = sorted(list_21, key=lambda x: x.get_cardvalue(), reverse=True)
        list_lower_21 = sorted(list_lower_21, key=lambda x: x.get_cardvalue(), reverse=True)
        list_busted = sorted(list_busted, key=lambda x: x.get_cardvalue(), reverse=True)

        if self.dealer.get_cardvalue() > 21:
            for user in list_21:
                set_game_won(user.get_userid())
            for user in list_lower_21:
                set_game_won(user.get_userid())
                # Alle mit 21 > Punkte >= 0 haben Einsatz x 1,5 gewonnen.
                # Alle mit 21 haben Einsatz mal 2 gewonnen
                # Alle mit 21 und Kartenanzahl = 2 haben Einsatz mal 3 gewonnen
        elif self.dealer.get_cardvalue() == 21:  # todo differentiate between blackjack and 21
            for user in list_21:
                if user.get_first_name() != translate("dealerName", self.lang_id):
                    set_game_won(user.get_userid())
                    # Alle mit 21 > Punkte >= 0 haben verloren . || Alle mit 21 haben Einsatz gewonnen || Alle mit 21 und Kartenanzahl = 2 haben Einsatz mal 2 gewonnen
                    # todo if dealer got Blackjack: || Everyone with BlackJack won their bet back. || Everone else lost
        elif self.dealer.get_cardvalue() < 21:
            for user in list_21:
                set_game_won(user.get_userid())
            for user in list_lower_21:
                if user.get_cardvalue() > self.dealer.get_cardvalue():
                    set_game_won(user.get_userid())
                    # print(str(user.get_userid()) + " you've got " + )
                    # Alle mit Dealer > Punkte haben verloren.
                    # Alle mit Dealer = Punkte erhalten Einsatz
                    # Alle mit 21 > Punkte > Dealer haben Einsatz x 1,5 gewonnen.
                    # Alle mit 21 haben Einsatz mal 2 gewonnen
                    # Alle mit 21 und Kartenanzahl = 2 haben Einsatz mal 3 gewonnen
                    # 7er Drilling 3/2 Gewinn (Einsatz x 1,5)

        final_message = translate("playerWith21", self.lang_id) + "\n"
        for user in list_21:
            final_message += str(user.get_cardvalue()) + " - " + user.get_first_name() + "\n"

        final_message += "\n" + translate("playerLess21", self.lang_id) + "\n"
        for user in list_lower_21:
            final_message += str(user.get_cardvalue()) + " - " + user.get_first_name() + "\n"

        final_message += "\n" + translate("playerOver21", self.lang_id) + "\n"
        for user in list_busted:
            final_message += str(user.get_cardvalue()) + " - " + user.get_first_name() + "\n"

        self.send_message(self.chat_id, final_message, game_id=self.__game_id)
        self.game_handler.gl_remove(self.chat_id)

    def get_player_overview(self, show_points=False, text="", i=0, dealer=False):
        if self.game_running:
            for user in self.players:
                if i == self.current_player:
                    text += "▶️"
                else:
                    text += "👤"
                if show_points is True and (i < self.current_player or self.current_player == -1):
                    text += (user.first_name + " - [" + str(user.get_cardvalue()) + "]\n")
                else:
                    text += (user.first_name + "\n")
                i += 1
            if dealer is True:
                text += ("🎩" + translate("dealerName", self.lang_id) + " - [" + str(self.dealer.get_cardvalue()) + "]")
            return text
        else:
            return ""

    # Messages are analyzed here. Most function calls come from here
    def analyze_message(self, update):
        text = update.message.text
        user_id = update.message.from_user.id
        first_name = update.message.from_user.first_name
        message_id = update.message.message_id

        # Remove leading slash from command
        if text.startswith("/"):
            command = str(text[1:]).lower()
        else:
            command = text.lower()

        # TODO following "or self.game_type == self.MULTIPLAYER_GAME" is not neccessary
        if self.game_type == self.GROUP_CHAT or self.game_type == self.MULTIPLAYER_GAME:
            if command.startswith(translate("join", self.lang_id)):
                self.add_player(user_id, first_name, message_id)
            elif command.startswith(translate("startCmd", self.lang_id)):
                self.start_game()
        if self.game_running:
            if command.startswith(translate("oneMore", self.lang_id)):
                current_player = self.players[self.current_player]
                if self.current_player >= 0 and user_id == current_player.user_id:
                    self.give_player_one()
                else:
                    self.send_message(self.chat_id, translate("notYourTurn", self.lang_id).format(first_name), game_id=self.__game_id)

            elif command.startswith(translate("noMore", self.lang_id)):
                current_player = self.players[self.current_player]
                if self.current_player >= 0 and user_id == current_player.user_id:
                    self.logger.debug("User doesn't want another card")
                    self.next_player()
            elif command.startswith(translate("stopCmd", self.lang_id)):
                if user_id == self.players[0].user_id:
                    self.game_handler.gl_remove(self.chat_id)

    def get_game_id(self):
        return self.__game_id

    # When game is being initialized
    def __init__(self, chat_id, user_id, lang_id, first_name, game_handler, message_id, send_message, multiplayer=None, game_id=None):
        # declare variables and set initial values
        self.players = []
        self.join_message_ids = []
        self.chat_id = chat_id
        self.__game_id = game_id
        self.lang_id = lang_id
        self.deck = CardDeck(lang_id)
        # TODO language of the cards & dealer cannot be changed
        # TODO especially with new multiplayer important!
        self.dealer = Dealer(translate("dealerName", lang_id), self.deck)
        self.game_running = False
        self.current_player = 0
        self.game_handler = game_handler
        self.send_message = send_message
        self.logger = logging.getLogger(__name__)

        if multiplayer:
            self.game_type = self.MULTIPLAYER_GAME
            chat_id = 0
        elif chat_id >= 0:
            self.game_type = self.PRIVATE_CHAT
        else:
            self.game_type = self.GROUP_CHAT

        one_more_button = KeyboardButton(translate("keyboardItemOneMore", lang_id))
        no_more_button = KeyboardButton(translate("keyboardItemNoMore", lang_id))
        stop_button = KeyboardButton(translate("keyboardItemStop", lang_id))
        self.keyboard_running = ReplyKeyboardMarkup(keyboard=[[one_more_button, no_more_button], [stop_button]], selective=True)

        self.add_player(user_id, first_name, message_id, silent=True)

        # Only send a "Please join the game" message, when it's a group chat
        if self.game_type == self.GROUP_CHAT:
            send_message(chat_id, translate("newRound", lang_id), message_id=message_id)  # keyboard=self.keyboard_not_running
        elif self.game_type == self.MULTIPLAYER_GAME:
            pass
        else:
            self.start_game()
            # start game and send message to private chat

    # When game is being ended / object is destructed
    def __del__(self):
        self.send_message(self.chat_id, translate("gameEnded", self.lang_id), reply_markup=ReplyKeyboardHide(), game_id=self.__game_id)
        pass
