# -*- coding: utf-8 -*-
import unittest
from unittest.mock import Mock

from blackjack.errors import GameAlreadyRunningException, PlayerAlreadyExistingException, MaxPlayersReachedException, NotEnoughPlayersException, \
    GameNotRunningException, PlayerBustedException, NoPlayersLeftException
from blackjack.game import BlackJackGame, GameType


class BlackJackGameTest(unittest.TestCase):

    def setUp(self):
        self.game = BlackJackGame(gametype=GameType.MULTIPLAYER_GROUP)

    @staticmethod
    def _generate_mock_deck(value=1):
        deck = Mock()
        card = Mock()
        card.value = value
        card.is_ace.return_value = (value == 11)
        deck.pick_one_card.return_value = card
        return deck

    def test_creation(self):
        """
        Check if creating an instance holds all necessary values
        :return:
        """
        self.assertFalse(self.game.running)
        self.assertEqual([], self.game.players)
        self.assertEqual(0, self.game._current_player)

    def test_start(self):
        """
        Check if starting the game changes the state and initializes the values of certain variables
        :return:
        """
        self.game.add_player(user_id=111, first_name="Player 111")
        self.assertFalse(self.game.running)
        self.game.add_player(user_id=222, first_name="Player 222")
        self.assertFalse(self.game.running)
        self.game.start(111)
        self.assertTrue(self.game.running)

        # Assert that each player has 2 cards
        self.assertEqual(2, len(self.game.players[0]._cards))
        self.assertEqual(2, len(self.game.dealer._cards))
        self.assertEqual(2, len(self.game.players))

    def test_start_twice(self):
        """
        Check that starting twice doesn't work and raises an exception
        :return:
        """
        self.game.type = GameType.SINGLEPLAYER
        self.assertFalse(self.game.running)
        self.game.add_player(user_id=111, first_name="Player 111")
        self.assertTrue(self.game.running)

        with self.assertRaises(GameAlreadyRunningException):
            self.game.start(111)

        self.assertTrue(self.game.running)

    def test_start_not_enough_players(self):
        """
        Check that starting without players doesn't work and raises an exception
        :return:
        """
        self.assertFalse(self.game.running)

        with self.assertRaises(NotEnoughPlayersException):
            self.game.start(111)

        self.assertFalse(self.game.running)

    def test_add_player(self):
        """
        Check if adding new players works
        :return:
        """
        self.assertEqual(0, len(self.game.players))
        self.game.add_player(user_id=15, first_name="Player 15")
        self.assertEqual(15, self.game.players[0].user_id)
        self.assertEqual("Player 15", self.game.players[0].first_name)

        self.assertEqual(1, len(self.game.players))
        self.game.add_player(user_id=125, first_name="Player 125")
        self.assertEqual(2, len(self.game.players))

        # Make sure that inserting players with the same name works just fine
        self.game.add_player(user_id=126, first_name="Player 125")
        self.assertEqual(3, len(self.game.players))

    def test_add_player_existing(self):
        """
        Check if adding existing players works as intended
        :return:
        """
        self.assertEqual(0, len(self.game.players))

        self.game.add_player(user_id=15, first_name="Player " + str(15))
        self.assertEqual(1, len(self.game.players))

        with self.assertRaises(PlayerAlreadyExistingException):
            self.game.add_player(user_id=15, first_name="Player " + str(15))

        self.assertEqual(1, len(self.game.players))

    def test_add_player_max(self):
        """
        Check if adding players when MAX_PLAYERS is reached raises an exception
        :return:
        """
        for i in range(self.game.MAX_PLAYERS):
            self.game.add_player(user_id=i, first_name="Player " + str(i))
        self.assertEqual(self.game.MAX_PLAYERS, len(self.game.players))

        with self.assertRaises(MaxPlayersReachedException):
            self.game.add_player(user_id=9999, first_name="Player 9999")

        self.assertEqual(self.game.MAX_PLAYERS, len(self.game.players))

    def test_add_player_game_started(self):
        """
        Check that it's no longer possible to add players as soon as the game is running
        :return:
        """
        self.assertEqual(0, len(self.game.players))

        self.game.add_player(user_id=15, first_name="Player " + str(15))
        self.assertEqual(1, len(self.game.players))

        self.game.add_player(user_id=125, first_name="Player 125")
        self.assertEqual(2, len(self.game.players))

        self.game.start(15)

        self.assertEqual(2, len(self.game.players))

        with self.assertRaises(GameAlreadyRunningException):
            self.game.add_player(user_id=111, first_name="Player 111")

        self.assertEqual(2, len(self.game.players))

    def test_next_player(self):
        """
        Check if using the next_player function leads to the player counter being increased
        :return:
        """
        self.game.add_player(user_id=111, first_name="Player 111")
        self.game.add_player(user_id=222, first_name="Player 222")

        self.game.start(111)

        self.assertEqual(0, self.game._current_player)
        self.game.next_player()
        self.assertEqual(1, self.game._current_player)

    def test_next_player_game_not_running(self):
        """
        Check if one can move to the next player although the game is not running yet
        :return:
        """
        self.game.add_player(user_id=111, first_name="Player 111")
        self.game.add_player(user_id=222, first_name="Player 222")

        self.assertEqual(0, self.game._current_player)
        with self.assertRaises(GameNotRunningException):
            self.game.next_player()

        self.assertEqual(0, self.game._current_player)

    def test_next_player_dealer(self):
        """
        Check if using the next_player function while there are no more players leads to the dealer's turn
        :return:
        """
        self.game.add_player(user_id=111, first_name="Player 111")
        self.game.add_player(user_id=222, first_name="Player 222")

        dealers_turn = Mock()
        self.game.dealers_turn = dealers_turn

        self.game.start(111)

        self.assertEqual(0, self.game._current_player)
        self.game.next_player()
        self.assertEqual(1, self.game._current_player)
        with self.assertRaises(NoPlayersLeftException):
            self.game.next_player()
        self.assertEqual(-1, self.game._current_player)
        dealers_turn.assert_called()

    def test_get_current_player(self):
        """
        Check if we receive the correct player from get_current_player()
        :return:
        """
        self.game.add_player(user_id=111, first_name="Player 111")
        self.game.add_player(user_id=222, first_name="Player 222")

        self.game.start(111)

        self.assertEqual(0, self.game._current_player)
        self.assertEqual(111, self.game.get_current_player().user_id)
        self.game.next_player()
        self.assertEqual(1, self.game._current_player)
        self.assertEqual(222, self.game.get_current_player().user_id)

    def test_draw_card(self):
        """
        Check if drawing cards works as intended
        :return:
        """
        self.game.deck = self._generate_mock_deck()
        self.game.add_player(user_id=111, first_name="Player 111")
        self.game.add_player(user_id=222, first_name="Player 222")

        self.game.start(111)

        # We have 2 cards from the init
        self.assertEqual(2, len(self.game.players[0]._cards))
        self.game.draw_card()

        # Now we should have 3 cards after drawing one
        self.assertEqual(3, len(self.game.players[0]._cards))

        # And it should have a value of 1
        self.assertEqual(1, self.game.players[0]._cards[2].value)

    def test_draw_card_game_not_running(self):
        """
        Check if it's possible to draw cards even though the game did not start yet
        :return:
        """
        self.assertFalse(self.game.running)
        with self.assertRaises(GameNotRunningException):
            self.game.draw_card()

    def test_draw_card_player_busted(self):
        """
        Check if we receive an exception when a player busted while drawing a card
        :return:
        """
        self.game.deck = self._generate_mock_deck(value=10)
        self.game.add_player(user_id=111, first_name="Player 111")
        self.game.add_player(user_id=222, first_name="Player 222")

        self.game.start(111)

        # We have 2 cards from the init
        self.assertEqual(2, len(self.game.players[0]._cards))
        self.assertEqual(20, self.game.players[0].cardvalue)

        with self.assertRaises(PlayerBustedException):
            self.game.draw_card()

        # Now we should have 3 cards after drawing one
        self.assertEqual(3, len(self.game.players[0]._cards))

        # And it should have a value of 10
        self.assertEqual(10, self.game.players[0]._cards[2].value)
        self.assertEqual(30, self.game.players[0].cardvalue)

    def test_dealers_turn(self):
        """
        Check that the dealer always draws cards until the card value > 16
        """
        self.game.type = GameType.SINGLEPLAYER

        # TODO generate specific Card Deck for a better test
        self.game.add_player(user_id=111, first_name="Player 111")

        self.assertEqual(2, len(self.game.dealer._cards))
        self.game.dealers_turn()
        self.assertGreater(self.game.dealer.cardvalue, 16)

    def test_dealers_turn_random(self):
        """
        Check that the dealer always draws cards until the card value > 16
        """
        self.game.type = GameType.SINGLEPLAYER
        self.game.add_player(user_id=111, first_name="Player 111")

        self.assertEqual(2, len(self.game.dealer._cards))
        self.game.dealers_turn()
        self.assertGreater(self.game.dealer.cardvalue, 16)

    def test_dealers_turn_game_not_running(self):
        """
        Check that the dealer can't take turn when the game is not running yet
        """
        self.game.add_player(user_id=111, first_name="Player 111")

        with self.assertRaises(GameNotRunningException):
            self.game.dealers_turn()

        self.assertEqual(0, self.game.dealer.cardvalue)


if __name__ == '__main__':
    unittest.main()
