# -*- coding: utf-8 -*-
import unittest

from blackjack.game import BlackJackGame
from blackjack.errors import GameAlreadyRunningException, PlayerAlreadyExistingException, MaxPlayersReachedException, NotEnoughPlayersException


class BlackJackGameTest(unittest.TestCase):

    def setUp(self):
        self.game = BlackJackGame()

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
        self.game.add_player(user_id=111, first_name="Player 111", message_id=1)
        self.assertFalse(self.game.running)
        self.game.start()
        self.assertTrue(self.game.running)

        # Assert that each player has 2 cards
        self.assertEqual(2, len(self.game.players[0].cards))
        self.assertEqual(2, len(self.game.dealer.cards))

    def test_start_twice(self):
        """
        Check that starting twice doesn't work and raises an exception
        :return:
        """
        self.game.add_player(user_id=111, first_name="Player 111", message_id=1)
        self.game.start()
        self.assertTrue(self.game.running)

        with self.assertRaises(GameAlreadyRunningException):
            self.game.start()

        self.assertTrue(self.game.running)

    def test_start_not_enough_players(self):
        """
        Check that starting without players doesn't work and raises an exception
        :return:
        """
        self.assertFalse(self.game.running)

        with self.assertRaises(NotEnoughPlayersException):
            self.game.start()

        self.assertFalse(self.game.running)

    def test_add_player(self):
        """
        Check if adding new players works
        :return:
        """
        self.assertEqual(0, len(self.game.players))
        self.game.add_player(user_id=15, first_name="Player 15", message_id=1)
        self.assertEqual(15, self.game.players[0].user_id)
        self.assertEqual("Player 15", self.game.players[0].first_name)
        self.assertEqual(1, self.game.players[0].join_id)

        self.assertEqual(1, len(self.game.players))
        self.game.add_player(user_id=125, first_name="Player 125", message_id=1)
        self.assertEqual(2, len(self.game.players))

        # Make sure that inserting players with the same name works just fine
        self.game.add_player(user_id=126, first_name="Player 125", message_id=1)
        self.assertEqual(3, len(self.game.players))

    def test_add_player_existing(self):
        """
        Check if adding existing players works as intended
        :return:
        """
        self.assertEqual(0, len(self.game.players))

        self.game.add_player(user_id=15, first_name="Player " + str(15), message_id=1)
        self.assertEqual(1, len(self.game.players))

        with self.assertRaises(PlayerAlreadyExistingException):
            self.game.add_player(user_id=15, first_name="Player " + str(15), message_id=1)

        self.assertEqual(1, len(self.game.players))

    def test_add_player_max(self):
        """
        Check if adding players when MAX_PLAYERS is reached raises an exception
        :return:
        """
        for i in range(self.game.MAX_PLAYERS):
            self.game.add_player(user_id=i, first_name="Player " + str(i), message_id=1)
        self.assertEqual(self.game.MAX_PLAYERS, len(self.game.players))

        with self.assertRaises(MaxPlayersReachedException):
            self.game.add_player(user_id=9999, first_name="Player 9999", message_id=1)

        self.assertEqual(self.game.MAX_PLAYERS, len(self.game.players))

    def test_add_player_game_started(self):
        """
        Check that it's no longer possible to add players as soon as the game is running
        :return:
        """
        self.assertEqual(0, len(self.game.players))

        self.game.add_player(user_id=15, first_name="Player " + str(15), message_id=1)
        self.assertEqual(1, len(self.game.players))

        self.game.add_player(user_id=125, first_name="Player 125", message_id=1)
        self.assertEqual(2, len(self.game.players))

        self.game.start()

        with self.assertRaises(GameAlreadyRunningException):
            self.game.add_player(user_id=111, first_name="Player 111", message_id=1)
        self.assertEqual(2, len(self.game.players))

    def test_next_player(self):
        """
        Check if using the next_player function leads to the player counter being increased
        :return:
        """
        self.game.add_player(user_id=111, first_name="Player 111", message_id=1)
        self.game.add_player(user_id=222, first_name="Player 222", message_id=1)

        self.game.start()

        self.assertEqual(0, self.game._current_player)
        self.game.next_player()
        self.assertEqual(1, self.game._current_player)

    def test_get_current_player(self):
        self.game.add_player(user_id=111, first_name="Player 111", message_id=1)
        self.game.add_player(user_id=222, first_name="Player 222", message_id=1)

        self.game.start()

        self.assertEqual(0, self.game._current_player)
        self.assertEqual(111, self.game.get_current_player().user_id)
        self.game.next_player()
        self.assertEqual(1, self.game._current_player)
        self.assertEqual(222, self.game.get_current_player().user_id)

    def test_dealers_turn(self):
        """
        Check that the dealer always draws cards until the card value > 16
        """
        # TODO generate specific Card Deck for a better test
        self.game.add_player(user_id=111, first_name="Player 111", message_id=1)
        self.game.start()

        self.assertEqual(2, len(self.game.dealer.cards))
        self.game.dealers_turn()
        self.assertGreater(self.game.dealer.cardvalue, 16)

    def test_dealers_turn_random(self):
        """
        Check that the dealer always draws cards until the card value > 16
        """
        self.game.add_player(user_id=111, first_name="Player 111", message_id=1)
        self.game.start()

        self.assertEqual(2, len(self.game.dealer.cards))
        self.game.dealers_turn()
        self.assertGreater(self.game.dealer.cardvalue, 16)


if __name__ == '__main__':
    unittest.main()
