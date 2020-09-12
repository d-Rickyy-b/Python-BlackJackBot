# -*- coding: utf-8 -*-
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from blackjack.errors import NoPlayersLeftException
from blackjack.game import BlackJackGame
from blackjackbot.commands.util.decorators import needs_active_game
from blackjackbot.commands.util import html_mention, get_game_keyboard, get_join_keyboard, generate_evaluation_string, remove_inline_keyboard
from blackjackbot.gamestore import GameStore
from blackjackbot.lang import Translator
from blackjackbot.util import get_cards_string
from database import Database

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logging.getLogger("telegram").setLevel(logging.ERROR)


def is_button_affiliated(update, context, game, lang_id):
    try:
        game_id = int(update.callback_query.data.split("_")[1])
        if game.id != game_id:
            update.callback_query.answer("Sorry, the button you pressed is not for your current game!")
            remove_inline_keyboard(update, context)
            return False
        return True
    except Exception as e:
        logger.error("Something unexpected happened while checking button affiliation: {} - {}".format(update.callback_query.data, e))
        return False


def players_turn(update, context):
    """Execute a player's turn"""
    chat = update.effective_chat
    game = GameStore().get_game(chat.id)
    player = game.get_current_player()
    user_mention = html_mention(user_id=player.user_id, first_name=player.first_name)

    lang_id = Database().get_lang_id(chat.id)
    translator = Translator(lang_id=lang_id)

    logger.info("Player's turn: {}".format(player))
    player_cards = get_cards_string(player, lang_id)

    # Check if player already has 21 or a BlackJack before their move. If so, automatically jump to the next player.
    # We need reply_text here, because we must send a new message (this is the first message for the player)!
    if player.has_blackjack():
        text = (translator("your_cards_are") + "\n\n" + translator("got_blackjack")).format(user_mention, player.cardvalue, player_cards)
        update.effective_message.reply_text(text=text, parse_mode="HTML", reply_markup=None)
        next_player(update, context)
    elif player.cardvalue == 21:
        text = (translator("your_cards_are") + "\n\n" + translator("got_21")).format(user_mention, player.cardvalue, player_cards)
        update.effective_message.reply_text(text=text, parse_mode="HTML", reply_markup=None)
        next_player(update, context)
    else:
        text = translator("your_cards_are").format(user_mention, player.cardvalue, player_cards)
        update.effective_message.reply_text(text=text, parse_mode="HTML", reply_markup=get_game_keyboard())


@needs_active_game
def next_player(update, context):
    chat = update.effective_chat
    user = update.effective_user
    lang_id = Database().get_lang_id(chat.id)
    translator = Translator(lang_id=lang_id)

    game = GameStore().get_game(chat.id)

    try:
        if user.id != game.get_current_player().user_id:
            update.callback_query.answer(translator("mp_not_your_turn_callback").format(user.first_name))
            return

        game.next_player()
    except NoPlayersLeftException:
        # TODO merge messages
        update.effective_message.reply_text("<b>Dealer: {}</b>\n\n{}".format(game.dealer.cardvalue, get_cards_string(game.dealer, lang_id)), parse_mode="HTML")
        evaluation_string = generate_evaluation_string(game, lang_id)

        newgame_button = InlineKeyboardButton(text=translator("inline_keyboard_newgame"), callback_data="newgame")
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[newgame_button]])
        update.effective_message.reply_text(evaluation_string, reply_markup=keyboard)
        game.stop(-1)
        return

    players_turn(update, context)


def create_game(update, context):
    """Create a new game instance for the chat of the user"""
    user = update.effective_user
    chat = update.effective_chat
    lang_id = Database().get_lang_id(chat.id)
    translator = Translator(lang_id=lang_id)

    # Create either a singleplayer or multiplayer game
    if chat.type == "private":
        game_type = BlackJackGame.Type.SINGLEPLAYER
    elif chat.type == "group" or chat.type == "supergroup":
        game_type = BlackJackGame.Type.MULTIPLAYER_GROUP
    else:
        logger.error("Chat type '{}' not supported!".format(chat.type))
        return

    game = BlackJackGame(gametype=game_type)
    game.add_player(user_id=user.id, first_name=user.first_name)
    GameStore().add_game(chat.id, game)

    # TODO currently the game starts instantly - this should change with multiplayer rooms
    if game.type == BlackJackGame.Type.SINGLEPLAYER:
        update.effective_message.reply_text(translator("game_starts_now").format("", get_cards_string(game.dealer, lang_id)))
        players_turn(update, context)
    else:
        text = translator("mp_request_join").format(game.get_player_list())
        update.effective_message.reply_text(text=text, reply_markup=get_join_keyboard(lang_id))
