# -*- coding: utf-8 -*-

from blackjack.game import Card
from blackjackbot.lang import translate


def get_cards_string(player, lang_id):
    """Returns the translated string representation of a player's hand"""
    if player.is_dealer and not player.turn_over:
        # We need to check, if we are allowed to display all of the dealer's cards already
        # Only the dealer's first card is shown until the dealer finished their turn
        return "{}  •  [❔]".format(get_card_string(player.cards[0], lang_id))
    else:
        return '  •  '.join(get_card_string(card, lang_id) for card in player.cards)


def get_card_string(card, lang_id):
    """Returns the translated string representation of a card object"""
    if card.type == Card.Type.NUMBER:
        face = card.value
    else:
        face = translate(card.str_id, lang_code=lang_id)

    return "{} {}".format(card.symbol, face)
