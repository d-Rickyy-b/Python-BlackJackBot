# -*- coding: utf-8 -*-

import blackjack.errors as errors
from blackjack.game import BlackJackGame
from blackjackbot.commands.util import html_mention, get_game_keyboard, get_join_keyboard, get_start_keyboard, remove_inline_keyboard
from blackjackbot.commands.util.decorators import needs_active_game
from blackjackbot.errors import NoActiveGameException
from blackjackbot.gamestore import GameStore
from blackjackbot.lang import Translator
from blackjackbot.util import get_cards_string
from database import Database
from .functions import create_game, players_turn, next_player


def start_cmd(update, context):
    """Handles messages contianing the /start command. Starts a game for a specific user"""
    user = update.effective_user
    chat = update.effective_chat
    lang_id = Database().get_lang_id(chat.id)
    translator = Translator(lang_id=lang_id)

    Database().add_user(user.id, user.language_code, user.first_name, user.last_name, user.username)

    try:
        GameStore().get_game(update.effective_chat.id)
        # TODO notify user that there is a running game already?
    except NoActiveGameException:
        # If there is no game, we create one
        create_game(update, context)


def start_callback(update, context):
    """Starts a game that has been created already"""
    user = update.effective_user
    chat = update.effective_chat
    lang_id = Database().get_lang_id(chat.id)
    translator = Translator(lang_id=lang_id)

    try:
        game = GameStore().get_game(update.effective_chat.id)
    except NoActiveGameException:
        update.callback_query.answer(translator("mp_no_created_game_callback"))
        remove_inline_keyboard(update, context)
        return

    try:
        game.start(user.id)
        update.callback_query.answer(translator("mp_starting_game_callback"))
    except errors.GameAlreadyRunningException:
        update.callback_query.answer(translator("mp_game_already_begun_callback"))
        return
    except errors.NotEnoughPlayersException:
        update.callback_query.answer(translator("mp_not_enough_players_callback"))
        return
    except errors.InsufficientPermissionsException:
        update.callback_query.answer(translator("mp_only_creator_start_callback").format(user.first_name))
        return

    if game.type != BlackJackGame.Type.SINGLEPLAYER:
        players_are = translator("mp_players_are")
        for player in game.players:
            players_are += "👤{}\n".format(player.first_name)
        players_are += "\n"
    else:
        players_are = ""

    update.effective_message.edit_text(translator("game_starts_now").format(players_are, get_cards_string(game.dealer, lang_id)))
    players_turn(update, context)


@needs_active_game
def stop_cmd(update, context):
    """Stops a game for a specific user"""
    user = update.effective_user
    chat = update.effective_chat
    lang_id = Database().get_lang_id(chat.id)
    translator = Translator(lang_id=lang_id)

    game = GameStore().get_game(chat.id)

    try:
        game.stop(user.id)
        update.effective_message.reply_text(translator("game_ended"))
    except errors.InsufficientPermissionsException:
        update.effective_message.reply_text(translator("mp_only_creator_can_end"))


@needs_active_game
def join_callback(update, context):
    """
    CallbackQueryHandler callback for the 'join' inline button. Adds the executing player to the game of the specific chat
    """
    user = update.effective_user
    chat = update.effective_chat
    lang_id = Database().get_lang_id(chat.id)
    translator = Translator(lang_id=lang_id)

    game = GameStore().get_game(chat.id)

    try:
        game.add_player(user.id, user.first_name)
        update.effective_message.edit_text(text=translator("mp_request_join").format(game.get_player_list()),
                                           reply_markup=get_join_keyboard(lang_id))
        update.callback_query.answer(translator("mp_join_callback").format(user.first_name))

        # If players are full, replace join keyboard with start keyboard
        if len(game.players) >= game.MAX_PLAYERS:
            update.effective_message.edit_reply_markup(reply_markup=get_start_keyboard(lang_id))
    except errors.GameAlreadyRunningException:
        remove_inline_keyboard(update, context)
        update.callback_query.answer(translator("mp_game_already_begun_callback"))
    except errors.MaxPlayersReachedException:
        update.effective_message.edit_reply_markup(reply_markup=get_start_keyboard(lang_id))
        update.callback_query.answer(translator("mp_max_players_callback"))
    except errors.PlayerAlreadyExistingException:
        update.callback_query.answer(translator("mp_already_joined_callback"))


@needs_active_game
def hit_callback(update, context):
    """
    CallbackQueryHandler callback for the 'hit' inline button. Draws a card for you.
    """
    user = update.effective_user
    chat = update.effective_chat
    lang_id = Database().get_lang_id(chat.id)
    translator = Translator(lang_id=lang_id)

    game = GameStore().get_game(chat.id)
    player = game.get_current_player()
    user_mention = html_mention(user_id=player.user_id, first_name=player.first_name)

    try:
        if user.id != player.user_id:
            update.callback_query.answer(translator("mp_not_your_turn_callback").format(user.first_name))
            return

        game.draw_card()
        player_cards = get_cards_string(player, lang_id)
        text = translator("your_cards_are").format(user_mention, player.cardvalue, player_cards)
        update.effective_message.edit_text(text=text, parse_mode="HTML", reply_markup=get_game_keyboard())
    except errors.PlayerBustedException:
        player_cards = get_cards_string(player, lang_id)
        text = (translator("your_cards_are") + "\n\n" + translator("you_busted")).format(user_mention, player.cardvalue, player_cards)
        update.effective_message.edit_text(text=text, parse_mode="HTML", reply_markup=None)
        next_player(update, context)
    except errors.PlayerGot21Exception:
        player_cards = get_cards_string(player, lang_id)
        if player.has_blackjack():
            text = (translator("your_cards_are") + "\n\n" + translator("got_blackjack")).format(user_mention, player.cardvalue, player_cards)
            update.effective_message.edit_text(text=text, parse_mode="HTML", reply_markup=None)
            next_player(update, context)
        elif player.cardvalue == 21:
            text = (translator("your_cards_are") + "\n\n" + translator("got_21")).format(user_mention, player.cardvalue, player_cards)
            update.effective_message.edit_text(text=text, parse_mode="HTML", reply_markup=None)
            next_player(update, context)


@needs_active_game
def stand_callback(update, context):
    """
    CallbackQueryHandler callback for the 'stand' inline button. Prepares round for the next player.
    """
    remove_inline_keyboard(update, context)

    next_player(update, context)


def newgame_callback(update, context):
    remove_inline_keyboard(update, context)
    start_cmd(update, context)


def rules_cmd(update, context):
    update.effective_message.reply_text("Rules:\n\n- Black Jack pays 3 to 2\n- Dealer must stand on 17 and must draw to 16\n- Insurance pays 2 to 1")
