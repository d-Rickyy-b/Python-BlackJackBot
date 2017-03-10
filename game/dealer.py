from game.player import Player


class Dealer(Player):
    credits = 0

    def __init__(self, first_name, deck):
        self.number_of_cards = 0
        self.user_id = -1
        self.first_name = first_name
        self.cardvalue = 0
        self.has_ace = False
        self.cards = [] * 0
        self.deck = deck
        self.bet = 0
