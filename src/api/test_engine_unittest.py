import unittest

from game_engine import *

# note, method names must start with 'test'
class TestGameEngine(unittest.TestCase):
    def test_num_players(self):
        self.assertEqual(game(9, 4).get_num_players(), 4)
        self.assertEqual(game(9, 3).get_num_players(), 3)
        self.assertEqual(game(9, 2).get_num_players(), 2)
        self.assertRaises(
            AssertionError, game, 9, 1
        )  # one is an invalid number of players

    def test_too_many_players(self):
        game2 = game(9, 5)  # too many players


if __name__ == "__main__":
    unittest.main()
