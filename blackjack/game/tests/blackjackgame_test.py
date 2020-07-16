import unittest


class BlackJackGameTest(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_creation(self):
        """
        Check if creating an instance holds all necessary values
        :return:
        """
        pass

    def test_start(self):
        """
        Check if starting the game changes the state and initializes the values of certain variables
        :return:
        """
        pass

    def test_add_player(self):
        """
        Check if adding new players works
        :return:
        """
        # Get amount of current players

        # add new player

        # assert that new count is old count + 1
        pass

    def test_add_player_existing(self):
        """
        Check if adding existing players works as intended
        :return:
        """
        # Get amount of current players

        # add existing player

        # assert that new count == old count
        pass

    def test_add_player_game_started(self):
        """
        Check that it's no longer possible to add players as soon as the game is running
        :return:
        """
        # Get amount of current players

        # add new player

        # assert that new count == old count
        pass

    def test_next_player(self):
        pass

    def test_something(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
