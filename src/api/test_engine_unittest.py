import unittest

from game_engine import *


class TestGameEngine(unittest.TestCase):
    def not_enough_players(self):
        game1 = game(9, 1)  # not enough players
        

    def too_many_players(self):
        game2 = game(9, 5)  # too many players


if __name__ == "__main__":
    unittest.main()
