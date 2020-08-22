# -*- coding: utf-8 -*-
import functools
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from blackjack.errors import NoPlayersLeftException
from blackjack.game import BlackJackGame
from blackjackbot.bot.commands.util import remove_inline_keyboard, html_mention, get_game_keyboard, get_join_keyboard, generate_evaluation_string
from blackjackbot.bot.commands.util.commands import translate
from blackjackbot.errors import NoActiveGameException
from blackjackbot.gamestore import GameStore

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
            remove_inline_keyboard(update, context)
            update.effective_message.reply_text("You don't have any game!")
            return

        return func(update, context)

    return wrapper


def players_turn(update, context):
    """Execute a player's turn"""
    user = update.effective_user
    chat = update.effective_chat
    game = GameStore().get_game(chat.id)
    player = game.get_current_player()
    user_mention = html_mention(user_id=player.user_id, first_name=player.first_name)

    logger.info("Player's turn: {}".format(player))

    if player.has_blackjack():
        text = (translate("your_cards_are") + "\n\n✅ Congratulations, you got a BlackJack!").format(user_mention, player.cardvalue, player.get_cards_string())
        update.effective_message.reply_text(text=text, parse_mode="HTML", reply_markup=None)
        next_player(update, context)
    elif player.cardvalue == 21:
        text = (translate("your_cards_are") + "\n\n✅ Congratulations, you got exactly 21!").format(user_mention, player.cardvalue, player.get_cards_string())
        update.effective_message.reply_text(text=text, parse_mode="HTML", reply_markup=None)
        next_player(update, context)
    else:
        text = translate("your_cards_are")
        update.effective_message.reply_text(text=text.format(user_mention, player.cardvalue, player.get_cards_string()),
                                            parse_mode="HTML", reply_markup=get_game_keyboard())


@needs_active_game
def next_player(update, context):
    chat = update.effective_chat
    user = update.effective_user

    game = GameStore().get_game(chat.id)

    try:
        if user.id != game.get_current_player().user_id:
            update.callback_query.answer(translate("mp_not_your_turn_callback").format(user.first_name))
            return
        if update.callback_query and not game.get_current_player().has_21():
            # TODO why did I put that here?
            remove_inline_keyboard(update, context)

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

    players_turn(update, context)


def create_game(update, context):
    """Create a new game instance for the chat of the user"""
    user = update.effective_user
    chat = update.effective_chat

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
        update.effective_message.reply_text(translate("game_starts_now").format("", game.dealer.get_cards_string()))
        players_turn(update, context)
    else:
        text = translate("mp_request_join").format(game.get_player_list())
        update.effective_message.reply_text(text=text, reply_markup=get_join_keyboard())
