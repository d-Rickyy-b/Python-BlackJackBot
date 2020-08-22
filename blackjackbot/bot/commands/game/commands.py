# -*- coding: utf-8 -*-

import blackjack.errors as errors
from blackjack.game import BlackJackGame
from blackjackbot.bot.commands.util import html_mention, get_game_keyboard, get_join_keyboard, get_start_keyboard, remove_inline_keyboard
from blackjackbot.bot.commands.util.commands import translate
from blackjackbot.errors import NoActiveGameException
from blackjackbot.gamestore import GameStore
from database import Database
from .functions import create_game, needs_active_game, players_turn, next_player


def start_cmd(update, context):
    """Handles messages contianing the /start command. Starts a game for a specific user"""
    user = update.effective_user

    Database().add_user(user.id, user.language_code, user.first_name, user.last_name, user.username)

    try:
        GameStore().get_game(update.effective_chat.id)
        # TODO notify user that there is a running game already?
    except NoActiveGameException:
        # If there is no game, we create one
        create_game(update, context)


def start_callback(update, context):
    """Starts a game that has been created already"""
    # TODO only useful for groups & starting games that already exist
    user = update.effective_user

    try:
        game = GameStore().get_game(update.effective_chat.id)
    except NoActiveGameException:
        update.callback_query.answer(translate("mp_no_created_game_callback"))
        remove_inline_keyboard(update, context)
        return

    try:
        game.start(user.id)
        update.callback_query.answer(translate("mp_starting_game_callback"))
    except errors.GameAlreadyRunningException:
        update.callback_query.answer(translate("mp_game_already_begun_callback"))
        return
    except errors.NotEnoughPlayersException:
        update.callback_query.answer(translate("mp_not_enough_players_callback"))
        return
    except errors.InsufficientPermissionsException:
        update.callback_query.answer(translate("mp_only_creator_start_callback").format(user.first_name))
        return

    if game.type != BlackJackGame.Type.SINGLEPLAYER:
        players_are = translate("mp_players_are")
        for player in game.players:
            players_are += "👤{}\n".format(player.first_name)
        players_are += "\n"
    else:
        players_are = ""

    update.effective_message.edit_text(translate("game_starts_now").format(players_are, game.dealer.get_cards_string()))
    players_turn(update, context)


@needs_active_game
def stop_cmd(update, context):
    """Stops a game for a specific user"""
    user = update.effective_user
    chat = update.effective_chat

    game = GameStore().get_game(chat.id)

    try:
        game.stop(user.id)
        update.effective_message.reply_text(translate("game_ended"))
    except errors.InsufficientPermissionsException:
        update.effective_message.reply_text(translate("mp_only_creator_can_end"))


@needs_active_game
def join_callback(update, context):
    """Join the game via inline button"""
    user = update.effective_user
    chat = update.effective_chat

    game = GameStore().get_game(chat.id)

    try:
        game.add_player(user.id, user.first_name)
        update.effective_message.edit_text(text=translate("mp_request_join").format(game.get_player_list()),
                                           reply_markup=get_join_keyboard())
        update.callback_query.answer(translate("mp_join_callback").format(user.first_name))

        # If players are full, replace join keyboard with start keyboard
        if len(game.players) >= game.MAX_PLAYERS:
            update.effective_message.edit_reply_markup(reply_markup=get_start_keyboard())
    except errors.GameAlreadyRunningException:
        remove_inline_keyboard(update, context)
        update.callback_query.answer(translate("mp_game_already_begun_callback"))
    except errors.MaxPlayersReachedException:
        update.effective_message.edit_reply_markup(reply_markup=get_start_keyboard())
        update.callback_query.answer(translate("mp_max_players_callback"))
    except errors.PlayerAlreadyExistingException:
        update.callback_query.answer(translate("mp_already_joined_callback"))


@needs_active_game
def hit_callback(update, context):
    user = update.effective_user
    chat = update.effective_chat

    game = GameStore().get_game(chat.id)
    player = game.get_current_player()
    user_mention = html_mention(user_id=player.user_id, first_name=player.first_name)

    try:
        if user.id != player.user_id:
            update.callback_query.answer(translate("mp_not_your_turn_callback").format(user.first_name))
            return

        game.draw_card()
        text = translate("your_cards_are").format(user_mention, player.cardvalue, player.get_cards_string())
        update.effective_message.edit_text(text=text, parse_mode="HTML", reply_markup=get_game_keyboard())
    except errors.PlayerBustedException:
        text = (translate("your_cards_are") + "\n\n" + translate("you_busted")).format(user_mention, player.cardvalue, player.get_cards_string())
        update.effective_message.edit_text(text=text, parse_mode="HTML", reply_markup=get_game_keyboard())
        next_player(update, context)
    except errors.PlayerGot21Exception:
        if player.has_blackjack():
            text = (translate("your_cards_are") + "\n\n✅ Congratulations, you got a BlackJack!").format(user_mention, player.cardvalue,
                                                                                                        player.get_cards_string())
            update.effective_message.reply_text(text=text, parse_mode="HTML", reply_markup=None)
            next_player(update, context)
        elif player.cardvalue == 21:
            text = (translate("your_cards_are") + "\n\n✅ Congratulations, you got exactly 21!").format(user_mention, player.cardvalue,
                                                                                                       player.get_cards_string())
            update.effective_message.reply_text(text=text, parse_mode="HTML", reply_markup=None)
            next_player(update, context)


@needs_active_game
def stand_callback(update, context):
    next_player(update, context)


def newgame_callback(update, context):
    remove_inline_keyboard(update, context)
    start_cmd(update, context)
