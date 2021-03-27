# -*- coding: utf-8 -*-
import unittest

import database.statistics
from database import Database


class StatisticsTest(unittest.TestCase):
    pass

    def setUp(self):
        pass

    def test_generate_bar_chart(self):
        """Test generation of bar charts"""
        bar_0_wins = "🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴"
        bar_1_wins = "🏆🔴🔴🔴🔴🔴🔴🔴🔴🔴"
        bar_2_wins = "🏆🏆🔴🔴🔴🔴🔴🔴🔴🔴"
        bar_3_wins = "🏆🏆🏆🔴🔴🔴🔴🔴🔴🔴"
        bar_9_wins = "🏆🏆🏆🏆🏆🏆🏆🏆🏆🔴"
        bar_10_wins = "🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆"

        bar1 = database.statistics.generate_bar_chart(0)
        self.assertEqual(bar_0_wins, bar1)
        bar2 = database.statistics.generate_bar_chart(0.5)
        self.assertEqual(bar_0_wins, bar2)
        bar3 = database.statistics.generate_bar_chart(5.0)
        self.assertEqual(bar_0_wins, bar3)

        bar4 = database.statistics.generate_bar_chart(5.1)
        self.assertEqual(bar_1_wins, bar4)

        bar5 = database.statistics.generate_bar_chart(11)
        self.assertEqual(bar_1_wins, bar5)

        bar6 = database.statistics.generate_bar_chart(16)
        self.assertEqual(bar_2_wins, bar6)

        bar7 = database.statistics.generate_bar_chart(29)
        self.assertEqual(bar_3_wins, bar7)

        bar8 = database.statistics.generate_bar_chart(91)
        self.assertEqual(bar_9_wins, bar8)

        bar9 = database.statistics.generate_bar_chart(100)
        self.assertEqual(bar_10_wins, bar9)

    def test_set_game_won(self):
        user_id = 123
        db = Database()
        db.add_user(user_id, "en", "test", "test2", "test3")

        user = db.get_user(user_id)
        self.assertEqual(user[5], 0)

        database.statistics.set_game_won(user_id)

        user = db.get_user(user_id)
        self.assertEqual(user[5], 1)

        database.statistics.set_game_won(user_id)

        user = db.get_user(user_id)
        self.assertEqual(user[5], 2)

    if __name__ == '__main__':
        unittest.main()
