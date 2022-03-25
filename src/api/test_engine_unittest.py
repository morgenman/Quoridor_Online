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

    def test_full_game_to_array(self):
        shorthand = "1. e2 e8 2. e3 e7 3. e4 e6 4. e3h g6v"
        moves = full_game_to_array(shorthand)
        self.assertEqual(len(moves), 4)
        for i in range(4):
            self.assertEqual(len(moves[i]), 2)
    
    def test_state_to_array(self):
        shorthand = "d4f4e7 / a2a8 / e4 e6 a4 h6 / 4 3 5 3 / 3"
        game = state_to_array(shorthand)
        self.assertEqual(game.get_num_players(),4)
        self.assertEqual(game.get_player(1).x,5) # e
        self.assertEqual(game.get_player(1).y,4) # 4

    def test_move_by_player(self):
        shorthand = "d4f4e7 / a2a8 / e4 e6 a4 h6 / 4 3 5 3 / 3"
        game = move_by_player("p1e5",shorthand)
        self.assertEqual(game.get_player(1).x,5) # e  
        self.assertEqual(game.get_player(1).y,5) # 5
        self.assertRaises(
            AssertionError, move_by_player, "p1e9", shorthand )  
        game2 =  game = move_by_player("p1e2")       
        self.assertEqual(game2.get_player(1).x,5) # e  
        self.assertEqual(game2.get_player(1).y,2) # 2
        self.assertEqual(game2.get_player(2).x,5) # e  
        self.assertEqual(game2.get_player(2).y,9) # 9

if __name__ == "__main__":
    unittest.main()
