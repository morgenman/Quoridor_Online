import unittest

from game_engine import *

# note, method names must start with 'test'
class TestGameEngine(unittest.TestCase):
    # def test_num_players(self):
    #    self.assertEqual(game(9, 4).get_num_players(), 4)
    #    self.assertEqual(game(9, 3).get_num_players(), 3)
    #    self.assertEqual(game(9, 2).get_num_players(), 2)
    #    self.assertRaises(
    #        AssertionError, game, 9, 1
    #    )  # one is an invalid number of players

    # def test_full_game_to_array(self):
    #    shorthand = "1. e2 e8 2. e3 e7 3. e4 e6 4. e3h g6v"
    #    moves = full_game_to_array(shorthand)
    #    self.assertEqual(len(moves), 4)
    #    for i in range(4):
    #        self.assertEqual(len(moves[i]), 2)

    # def test_state_to_array(self):
    #    shorthand = "d4f4e7 / a2a8 / e4 e6 a4 h6 / 4 3 5 3 / 3"
    #    game = state_to_array(shorthand)
    #    self.assertEqual(game.get_num_players(), 4)
    #    self.assertEqual(game.get_player(1).x, 5)  # e
    #    self.assertEqual(game.get_player(1).y, 4)  # 4

    # def test_move_by_player(self):
    #    shorthand = "d4f4e7 / a2a8 / e4 e6 a4 h6 / 4 3 5 3 / 3"
    #    game = move_by_player("p1e5", shorthand)
    #    self.assertEqual(game.get_player(1).x, 5)  # e
    #    self.assertEqual(game.get_player(1).y, 5)  # 5
    #    self.assertRaises(AssertionError, move_by_player, "p1e9", shorthand)
    #    game2 = game = move_by_player("p1e2")
    #    self.assertEqual(game2.get_player(1).x, 5)  # e
    #    self.assertEqual(game2.get_player(1).y, 2)  # 2
    #    self.assertEqual(game2.get_player(2).x, 5)  # e
    #    self.assertEqual(game2.get_player(2).y, 9)  # 9

    def test_player_and_piece_checking(self):
        print("\nTesting the player-checker and piece-checker")
        shorthand = " / / e1 e9 / 10 10 / 2"
        game_test = shorthand_to_game(shorthand)
        game_test.set_two_player(player(1), player(2))
        self.assertRaises(AssertionError, game_test.check_player, 1)
        self.assertIsNone(game_test.check_player(2))
        self.assertRaises(AssertionError, game_test.check_piece, "p1e2")
        self.assertIsNone(game_test.check_piece("p2e8"))

    def test_player_moving(self):
        print("\nTesting the player movement")
        shorthand = " / / e1 e9 / 10 10 / 2"
        game_test = shorthand_to_game(shorthand)
        game_test.set_two_player(player(1), player(2))

        print(
            "\nTesting a legal move; that the player's position changes, and turn changes"
        )
        game_test.num_players = 2
        game_test.move("p2e8")
        self.assertEqual(game_test.get_player(2).__repr__(), "e8")
        self.assertEqual(int(game_test.get_turn()), 1)

        print("\nTesting an illegal move and that nothing changes")
        game_test.move("p1e5")
        self.assertEqual(game_test.get_player(1).__repr__(), "e1")
        self.assertEqual(int(game_test.get_turn()), 1)

    def test_path_reach(self):
        print(
            "\nTesting the path-checker (both individual checker and all-player checker)"
        )
        shorthand = " a4c4e4g4g6 / h5 / e1 e9 / 10 10 / 1 "
        game_test = shorthand_to_game(shorthand)

        print("\nTesting When both players can reach the other side")
        self.assertTrue(game_test.can_reach_level(game_test.get("e9"), 1))
        self.assertTrue(game_test.can_reach_level(game_test.get("e1"), 9))
        self.assertTrue(game_test.all_players_can_reach())

        print("\nTesting when neither player can reach")
        shorthand = " a4c4e4g4h6  / h5  / e1 e9 / 10 10 / 1 "
        game_test = shorthand_to_game(shorthand)
        self.assertFalse(game_test.can_reach_level(game_test.get("e9"), 1))
        self.assertFalse(game_test.can_reach_level(game_test.get("e1"), 9))
        self.assertFalse(game_test.all_players_can_reach())

        print("\nTesting when player 1 can but player 2 can't")
        shorthand = " a3c3e3  / f4f6f8  / e1 e9 / 10 10 / 1 "
        game_test = shorthand_to_game(shorthand)
        self.assertFalse(game_test.can_reach_level(game_test.get("e9"), 1))
        self.assertTrue(game_test.can_reach_level(game_test.get("e1"), 9))
        self.assertFalse(game_test.all_players_can_reach())

    def test_wall_placing(self):
        print("\nTesting Wall Placement")
        shorthand = " / / e1 e9 / 10 10 / 2"
        game_test = shorthand_to_game(shorthand)
        game_test.set_two_player(player(1), player(2))

        print("\nTesting horiziontal wall placement")
        game_test.place_wall_h("e4")
        self.assertIsNone(game_test.get("e4").get_north())
        self.assertIsNone(game_test.get("f4").get_north())
        self.assertIsNone(game_test.get("e5").get_south())
        self.assertIsNone(game_test.get("f5").get_south())
        self.assertEqual(int(game_test.get_turn()), 1)
        self.assertEqual(game_test.get_walls()[1], 9)

        print("\nTesting vertical wall placement")
        game_test.place_wall_v("h5")
        self.assertIsNone(game_test.get("h5").get_east())
        self.assertIsNone(game_test.get("h6").get_east())
        self.assertIsNone(game_test.get("i5").get_west())
        self.assertIsNone(game_test.get("i6").get_west())
        self.assertEqual(int(game_test.get_turn()), 2)
        self.assertEqual(game_test.get_walls()[0], 9)

        print("\nTesting illegal wall placement (both vertical and horizontal)")
        self.assertIsNone(game_test.place_wall_h("h5"))
        self.assertEqual(int(game_test.get_turn()), 2)
        self.assertEqual(game_test.get_walls()[1], 9)
        self.assertIsNone(game_test.place_wall_h("e4"))
        self.assertEqual(int(game_test.get_turn()), 2)
        self.assertEqual(game_test.get_walls()[1], 9)

        print("\nTesting when player has no more walls")
        game_test.set_walls([1, 0])
        self.assertIsNone(game_test.place_wall_h("d6"))
        self.assertEqual(int(game_test.get_turn()), 2)
        self.assertIsNone(game_test.place_wall_v("d6"))
        self.assertEqual(int(game_test.get_turn()), 2)

    def test_special_moves(self):
        print("\nTesting special case moves")
        shorthand = " e3 /  / e3 e9 / 10 10 / 1 "
        game_test = shorthand_to_game(shorthand)
        game_test.players = [player(1), player(2)]

        print("\nTesting when blocked by wall")
        game_test.move("p1e4")
        self.assertEqual(game_test.get_player(1).__repr__(), "e3")
        self.assertEqual(int(game_test.get_turn()), 1)

        shorthand = "  /  / e3 e4 / 10 10 / 1 "
        game_test = shorthand_to_game(shorthand)
        game_test.players = [player(1), player(2)]

        print("\nTesting jumping moves")
        game_test.move("p1e5")
        self.assertEqual(game_test.get_player(1).__repr__(), "e5")
        self.assertEqual(int(game_test.get_turn()), 2)

        shorthand = " e4 /  / e3 e4 / 10 10 / 1 "
        game_test = shorthand_to_game(shorthand)
        game_test.players = [player(1), player(2)]
        game_test.move("p1f4")
        self.assertEqual(game_test.get_player(1).__repr__(), "f4")
        self.assertEqual(int(game_test.get_turn()), 2)


if __name__ == "__main__":
    unittest.main()
