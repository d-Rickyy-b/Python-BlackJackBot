# -*- coding: utf-8 -*-

from database.statistics import add_game_played, set_game_won
from game.player import Player
from game.dealer import Dealer
from game.cardDeck import CardDeck
from lang.language import translate
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from telegram.keyboardbutton import KeyboardButton
import logging

__author__ = 'Rico & Julian'


class BlackJack(object):
    GROUP_CHAT = 1
    PRIVATE_CHAT = 0
    MAX_PLAYERS = 5

    # Adds Player to the Game
    def add_player(self, user_id, first_name, message_id, silent=None):
        if not self.game_running:
            if self.get_index_by_user_id(user_id) == -1 and len(self.players) <= self.MAX_PLAYERS:
                self.logger.debug("Adding user '" + first_name + "' to players.")
                player = Player(user_id, first_name, self.deck)
                self.players.append(player)

                if silent is None:
                    self.send_message(self.chat_id, translate("playerJoined", self.lang_id).format(first_name), message_id=message_id)
            else:
                self.logger.debug("User '" + first_name + "' already in player list.")

    def get_index_by_user_id(self, user_id):
        index = 0
        for user in self.players:
            if user.get_userid() == user_id:
                return index
            index += 1

        return -1

    def get_user_by_user_id(self, user_id):
        for user in self.players:
            if user.get_userid() == user_id:
                return user

        return None

    def next_player(self):
        if (self.current_player + 1) < len(self.players):
            # TODO send message next player
            self.logger.debug("Next Player!")
            self.current_player += 1
            self.give_player_one()
        else:
            self.logger.debug("Dealer's turn")
            self.current_player = -1
            self.dealers_turn()

    # gives player one card
    def give_player_one(self):
        if self.game_running:
            player_index = self.current_player
            user = self.players[player_index]
            self.logger.debug("Giving player one card | chatID: " + str(self.chat_id) + " | player: " + user.first_name)

            if user.get_number_of_cards() == 0:
                # give user 2 cards at beginning
                for i in range(2):
                    card = self.deck.pick_one_card()
                    cardvalue = self.deck.get_card_value(card)

                    user.give_card(card, cardvalue)

                cards_string = user.get_cards_string()
                self.send_message(self.chat_id, str(translate("yourCardsAre", self.lang_id).format(user.first_name, "\n" + cards_string + "\n", str(user.cardvalue))))
            else:
                card = self.deck.pick_one_card()
                cardvalue = self.deck.get_card_value(card)

                if user.has_ace and user.cardvalue + cardvalue > 21:
                    # user got an ace
                    cardvalue = 1
                    # TODO send message, that he got a soft hand now.

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

                    # TODO remove keyboard from user
                    self.send_message(self.chat_id, text=player_drew, reply_markup=None)
                    self.next_player()
                else:
                    self.send_message(self.chat_id, text=player_drew, reply_markup=self.keyboard_running)

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

            # TODO this displays only the second card, but not the first
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
            # TODO end game / evaluation

    def start_game(self, message_id=None):
        if not self.game_running:
            self.game_running = True

            for player in self.players:
                add_game_played(player.user_id)

            if self.game_type == self.GROUP_CHAT:
                self.send_message(self.chat_id, translate("gameBegins", self.lang_id) + "\n" + translate("gameBegins2", self.lang_id) + "\n\n" + self.get_player_overview())
            else:
                # Anything here
                pass

            self.dealers_turn()
            self.give_player_one()

    def evaluation(self):
        # TODO Evaluation
        pass

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
            text += ("🎩" + translate("dealerName", self.lang_id) + " - [" + str(self.dealer.get_cardvalue()) + "]")
        return text

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

        if self.game_type == self.GROUP_CHAT:
            if command.startswith(translate("join", self.lang_id)):
                self.add_player(user_id, first_name, message_id)
            elif command.startswith(translate("startCmd", self.lang_id)):
                # Check if there are at least 2 players joined
                if len(self.players) >= 2:
                    self.start_game()
                else:
                    self.send_message(self.chat_id, translate("notEnoughPlayers", self.lang_id, message_id=message_id))
        if self.game_running:
            if command.startswith(translate("oneMore", self.lang_id)):
                current_player = self.players[self.current_player]
                if self.current_player >= 0 and user_id == current_player.user_id:
                    self.give_player_one()
                else:
                    self.send_message(self.chat_id, translate("notYourTurn", self.lang_id).format(first_name))

            elif command.startswith(translate("noMore", self.lang_id)):
                current_player = self.players[self.current_player]
                if self.current_player >= 0 and user_id == current_player.user_id:
                    self.logger.debug("User doesn't want another card")
                    self.next_player()
            elif command.startswith(translate("stopCmd", self.lang_id)):
                if user_id == self.players[0].user_id:
                    self.game_handler.gl_remove(self.chat_id)
                    # TODO Send message after removing game
                pass

    # When game is being initialized
    def __init__(self, chat_id, user_id, lang_id, first_name, game_handler, message_id, send_message):
        # declare variables and set initial values
        self.players = []
        self.chat_id = chat_id
        self.lang_id = lang_id
        self.deck = CardDeck(lang_id)  # TODO language of the cards & dealer cannot be changed
        self.dealer = Dealer(translate("dealerName", lang_id), self.deck)
        self.game_running = False
        self.current_player = 0
        self.game_handler = game_handler
        self.send_message = send_message
        self.logger = logging.getLogger(__name__)

        if chat_id >= 0:
            self.game_type = self.PRIVATE_CHAT
        else:
            self.game_type = self.GROUP_CHAT

        one_more_button = KeyboardButton(translate("keyboardItemOneMore", self.lang_id))
        no_more_button = KeyboardButton(translate("keyboardItemNoMore", self.lang_id))
        stop_button = KeyboardButton(translate("keyboardItemStop", self.lang_id))

        self.keyboard_running = ReplyKeyboardMarkup([[one_more_button, no_more_button], [stop_button]])

        self.add_player(user_id, first_name, message_id, silent=True)

        # Only send a "Please join the game" message, when it's a group chat
        if self.game_type == self.GROUP_CHAT:
            send_message(chat_id, translate("newRound", lang_id), message_id=message_id)  # keyboard=self.keyboard_not_running
        else:
            self.start_game()
            # start game and send message to private chat

    # When game is being ended - single and multiplayer
    def __del__(self):
        # TODO Hide Keyboard
        pass
