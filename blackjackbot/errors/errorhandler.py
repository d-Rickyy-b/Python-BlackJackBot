# -*- coding: utf-8 -*-
import logging

from telegram.error import Unauthorized, BadRequest, TimedOut, NetworkError, ChatMigrated, TelegramError
from blackjackbot.gamestore import GameStore

logger = logging.getLogger(__name__)


def error_handler(update, context):
    try:
        raise context.error
    except Unauthorized as e:
        # remove update.message.chat_id from conversation list
        logger.error("The update {} raised the following 'Unauthorized' exception: {}".format(update, e))
        if e.message == "Forbidden: bot was blocked by the user":
            GameStore().remove_game(update.effective_chat.id)
        elif e.message == "Forbidden: bot was kicked from the supergroup chat" or e.message == "Forbidden: bot was kicked from the group chat":
            GameStore().remove_game(update.effective_chat.id)

    except BadRequest as e:
        # handle malformed requests - read more below!
        logger.error("The update {} raised the following 'BadRequest' exception: {}".format(update, e))
    except TimedOut as e:
        logger.warning("The update {} timed out: {}".format(update, e))
        # handle slow connection problems
    except NetworkError as e:
        # handle other connection problems
        logger.warning("The update {} raised the following 'NetworkError' exception: {}".format(update, e))
    except ChatMigrated as e:
        # the chat_id of a group has changed, use e.new_chat_id instead
        logger.warning("The update {} raised the following 'ChatMigrated' exception: {}".format(update, e))
    except TelegramError as e:
        # handle all other telegram related errors
        logger.error("The update {} caused the following TelegramError: {}".format(update, e))
