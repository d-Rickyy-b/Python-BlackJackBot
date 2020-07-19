import unittest

from blackjack.game import BlackJackGame
from blackjack.errors import GameAlreadyRunningException, PlayerAlreadyExistingException, MaxPlayersReachedException


class BlackJackGameTest(unittest.TestCase):

    def setUp(self) -> None:
        self.game = BlackJackGame()

    def tearDown(self) -> None:
        pass

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
        self.game.start()
        self.assertTrue(self.game.running)

    def test_start_twice(self):
        """
        Check that starting twice doesn't work and raises an exception
        :return:
        """
        self.game.start()
        self.assertTrue(self.game.running)

        with self.assertRaises(GameAlreadyRunningException):
            self.game.start()

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
        pass


if __name__ == '__main__':
    unittest.main()
