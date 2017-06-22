__author__ = 'Rico'


class Player(object):
    def give_card(self, card, value):
        self.cards.append(card)

        if value == 1 and self.cardvalue <= 10:
            value = 11
            self.give_ace()

        self.cardvalue += value
        self.number_of_cards += 1

    def give_ace(self):
        self.has_ace = True

    def remove_ace(self):
        self.has_ace = False
        self.cardvalue -= 10

    def has21(self):
        return self.cardvalue == 21

    def has_busted(self):
        return self.cardvalue > 21

    def get_cards_string(self):
        cards_string = ""
        for i, card in enumerate(self.cards):
            cards_string += self.deck.get_card_name(card)
            if i+1 < len(self.cards):
                cards_string += ", "
        return cards_string

    def get_number_of_cards(self):
        return self.number_of_cards

    def get_first_name(self):
        return self.first_name

    def get_cardvalue(self):
        return self.cardvalue

    def get_userid(self):
        return self.user_id

    def get_lang_id(self):
        return self.lang_id

    def __init__(self, user_id, first_name, deck, lang_id="en"):
        self.user_id = user_id
        self.first_name = first_name
        self.lang_id = lang_id
        self.deck = deck
        self.number_of_cards = 0
        self.cardvalue = 0
        self.has_ace = False
        self.cards = []
