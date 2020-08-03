# -*- coding: utf-8 -*-
import functools
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

import config
from blackjack.errors import GameAlreadyRunningException, PlayerBustedException, InsufficientPermissionsException, MaxPlayersReachedException, \
    PlayerAlreadyExistingException, NotEnoughPlayersException, NoPlayersLeftException
from blackjack.game import BlackJackGame, GameType
from database import Database
from telegramWrapper.errors import NoActiveGameException
from telegramWrapper.gamestore import GameStore
from telegramWrapper.util import html_mention, get_game_keyboard, get_join_keyboard, generate_evaluation_string, get_start_keyboard
from telegramWrapper.utilcommands import stats_cmd, language_cmd, translate

# Game settings:
# help
# hide
# send comment

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logging.getLogger("telegram").setLevel(logging.ERROR)


def needs_active_game(func):
    @functools.wraps(func)
    def wrapper(update, context, *args, **kwargs):
        chat = update.effective_chat

        try:
            game = GameStore().get_game(chat.id)
        except NoActiveGameException:
            _remove_inline_keyboard(update, context)
            update.effective_message.reply_text("You don't have any game!")
            return

        return func(update, context)

    return wrapper


def _players_turn(update, context):
    """Execute a player's turn"""
    user = update.effective_user
    chat = update.effective_chat
    game = GameStore().get_game(chat.id)
    player = game.get_current_player()
    user_mention = html_mention(user_id=player.user_id, first_name=player.first_name)

    logger.info("Player's turn: {}".format(player))

    # TODO make sure that only current user can draw cards
    # TODO if player has 21, move to next player
    if player.has_blackjack():

        text = (translate("your_cards_are") + "\n\n✅ Congratulations, you got a BlackJack!").format(user_mention, player.cardvalue, player.get_cards_string())
        #text = "Congratulations {}, your Cards are:\n\n{}\n\nYou got a BlackJack!".format(user_mention, player.get_cards_string())
        update.effective_message.reply_text(text=text, parse_mode="HTML", reply_markup=None)
        _next_player(update, context)
    elif player.cardvalue == 21:

        text = (translate("your_cards_are") + "\n\n✅ Congratulations, you got exactly 21!").format(user_mention, player.cardvalue, player.get_cards_string())
        #text = "Congratulations {}, your Cards are:\n\n{}\n\nYou got exactly 21!".format(user_mention, player.get_cards_string())
        update.effective_message.reply_text(text=text, parse_mode="HTML", reply_markup=None)
        _next_player(update, context)
    else:
        text = translate("your_cards_are")
        update.effective_message.reply_text(text=text.format(user_mention, player.cardvalue, player.get_cards_string()),
                                            parse_mode="HTML", reply_markup=get_game_keyboard())


@needs_active_game
def _next_player(update, context):
    chat = update.effective_chat
    user = update.effective_user

    game = GameStore().get_game(chat.id)

    try:
        if user.id != game.get_current_player().user_id:
            update.callback_query.answer("It's not your turn, {}!".format(user.first_name))
            return
        if update.callback_query and not game.get_current_player().has_21():
            _remove_inline_keyboard(update, context)

        game.next_player()
    except NoPlayersLeftException:
        # TODO merge messages
        update.effective_message.reply_text("<b>Dealer: {}</b>\n\n{}".format(game.dealer.cardvalue, game.dealer.get_cards_string()), parse_mode="HTML")
        evaluation_string = generate_evaluation_string(game)
        get_join_keyboard()

        newgame_button = InlineKeyboardButton(text="New game", callback_data="newgame")
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[newgame_button]])
        update.effective_message.reply_text(evaluation_string, reply_markup=keyboard)
        game.stop(-1)
        return

    _players_turn(update, context)


def _create_game(update, context):
    """Create a new game instance for the chat of the user"""
    user = update.effective_user
    chat = update.effective_chat

    # Create either a singleplayer or multiplayer game
    if chat.type == "private":
        game_type = GameType.SINGLEPLAYER
    elif chat.type == "group" or chat.type == "supergroup":
        game_type = GameType.MULTIPLAYER_GROUP
    else:
        logger.error("Chat type '{}' not supported!".format(chat.type))
        return

    game = BlackJackGame(gametype=game_type)
    game.add_player(user_id=user.id, first_name=user.first_name)
    GameStore().add_game(chat.id, game)

    # TODO currently the game starts instantly - this should change with multiplayer rooms
    if game.type == GameType.SINGLEPLAYER:
        update.effective_message.reply_text("The game starts now. 🎲\n\nDealer's cards:\n\n{}".format(game.dealer.get_cards_string()))
        _players_turn(update, context)
    else:
        text = "Game created, please join. Players are:\n\n{}".format(game.get_player_list())
        update.effective_message.reply_text(text=text, reply_markup=get_join_keyboard())


def _remove_inline_keyboard(update, context):
    if update.effective_message.from_user.id == context.bot.id:
        update.effective_message.edit_reply_markup(reply_markup=None)


def start_cmd(update, context):
    """Handles messages contianing the /start command. Starts a game for a specific user"""
    user = update.effective_user

    Database().add_user(user.id, user.language_code, user.first_name, user.last_name, user.username)

    try:
        GameStore().get_game(update.effective_chat.id)
        # TODO notify user that there is a running game already?
    except NoActiveGameException:
        # If there is no game, we create one
        _create_game(update, context)


def rules_cmd(update, context):
    update.effective_message.reply_text("Rules:\n\n- Black Jack pays 3 to 2\n- Dealer must stand on 17 and must draw to 16\n- Insurance pays 2 to 1")


def start_callback(update, context):
    """Starts a game that has been created already"""
    # TODO only useful for groups & starting games that already exist
    user = update.effective_user

    try:
        game = GameStore().get_game(update.effective_chat.id)
    except NoActiveGameException:
        update.callback_query.answer("There is no created game!")
        _remove_inline_keyboard(update, context)
        return

    try:
        game.start(user.id)
        update.callback_query.answer("Starting game")
    except GameAlreadyRunningException:
        update.callback_query.answer("The game has already begun.")
        return
    except NotEnoughPlayersException:
        update.callback_query.answer("There are not enough players yet!")
        return
    except InsufficientPermissionsException:
        update.callback_query.answer("Fuck off {}, only the creator can start the game!".format(user.first_name))
        return

    if game.type != GameType.SINGLEPLAYER:
        players_are = "Players are:\n"
        for player in game.players:
            players_are += "👤{}\n".format(player.first_name)
        players_are += "\n"
    else:
        players_are = ""

    update.effective_message.edit_text("The game starts now. 🎲\n\n{}Dealer's cards:\n\n{}".format(players_are, game.dealer.get_cards_string()))
    _players_turn(update, context)


@needs_active_game
def stop_cmd(update, context):
    """Stops a game for a specific user"""
    user = update.effective_user
    chat = update.effective_chat

    game = GameStore().get_game(chat.id)

    try:
        game.stop(user.id)
        update.effective_message.reply_text("The game has been ended. 😉 You can /start another one if you like to.")
    except InsufficientPermissionsException:
        update.effective_message.reply_text("Only the creator can end the game!")


@needs_active_game
def join_callback(update, context):
    """Join the game via inline button"""
    user = update.effective_user
    chat = update.effective_chat

    game = GameStore().get_game(chat.id)

    try:
        game.add_player(user.id, user.first_name)
        update.effective_message.edit_text(text="Game created, please join. Players are:\n\n{}".format(game.get_player_list()),
                                           reply_markup=get_join_keyboard())
        update.callback_query.answer("Welcome {}!".format(user.first_name))

        # If players are full, replace join keyboard with start keyboard
        if len(game.players) >= game.MAX_PLAYERS:
            update.effective_message.edit_reply_markup(reply_markup=get_start_keyboard())
    except GameAlreadyRunningException:
        _remove_inline_keyboard(update, context)
        update.callback_query.answer("The game has already begun.")
    except MaxPlayersReachedException:
        update.effective_message.edit_reply_markup(reply_markup=get_start_keyboard())
        update.callback_query.answer("The max amount of players has been reached!")
    except PlayerAlreadyExistingException:
        update.callback_query.answer("You already joined the game!")


@needs_active_game
def hit_callback(update, context):
    user = update.effective_user
    chat = update.effective_chat

    game = GameStore().get_game(chat.id)
    player = game.get_current_player()
    user_mention = html_mention(user_id=player.user_id, first_name=player.first_name)

    try:
        if user.id != player.user_id:
            update.callback_query.answer("It's not your turn, {}!".format(user.first_name))
            return

        game.draw_card()
        text = translate("your_cards_are").format(user_mention, player.cardvalue, player.get_cards_string())
        update.effective_message.edit_text(text=text, parse_mode="HTML", reply_markup=get_game_keyboard())
    except PlayerBustedException:
        text = (translate("your_cards_are") + "\n\n❌ You busted!").format(user_mention, player.cardvalue, player.get_cards_string())
        update.effective_message.edit_text(text=text, parse_mode="HTML", reply_markup=get_game_keyboard())
        _next_player(update, context)


@needs_active_game
def stand_callback(update, context):
    _next_player(update, context)


def newgame_callback(update, context):
    _remove_inline_keyboard(update, context)
    start_cmd(update, context)


updater = Updater(token=config.BOT_TOKEN, use_context=True)

start_command_handler = CommandHandler("start", start_cmd)
stop_command_handler = CommandHandler("stop", stop_cmd)
language_command_handler = CommandHandler("language", language_cmd)
stats_command_handler = CommandHandler("stats", stats_cmd)

hit_callback_handler = CallbackQueryHandler(hit_callback, pattern=r"^hit$")
stand_callback_handler = CallbackQueryHandler(stand_callback, pattern=r"^stand$")
join_callback_handler = CallbackQueryHandler(join_callback, pattern=r"^join$")
start_callback_handler = CallbackQueryHandler(start_callback, pattern=r"^start$")
newgame_callback_handler = CallbackQueryHandler(newgame_callback, pattern=r"^newgame$")

handlers = [start_command_handler, stop_command_handler, join_callback_handler, hit_callback_handler, stand_callback_handler, start_callback_handler,
            language_command_handler, stats_command_handler, newgame_callback_handler]

# TODO change lang commands

for handler in handlers:
    updater.dispatcher.add_handler(handler)

if config.USE_WEBHOOK:
    updater.start_webhook(listen="127.0.0.1", port=config.WEBHOOK_PORT, url_path=config.BOT_TOKEN, cert=config.CERTPATH, webhook_url=config.WEBHOOK_URL)
    updater.bot.set_webhook(config.WEBHOOK_URL)
    logger.info("Started webhook server!")
else:
    updater.start_polling()
    logger.info("Started polling!")

logger.info("Bot started as @{}".format(updater.bot.username))
updater.idle()
