# Game Engine contains data structures and methods for the engine
# Notation info: https://quoridorstrats.wordpress.com/notation/

# function overloading

from game_classes import *
from multipledispatch import dispatch

# ----Tests--------------------------------------------------------

# this is not a proper unit test. It is just a quick test to see if the tile system is working as expected.
def test():
    game1 = game(9, 2)
    game1.get(5, 3).set_wall_h()
    game1.get(7, 2).set_wall_v()
    game1.get(5, 1).val = 1
    game1.get(5, 9).val = 2
    game1.draw()
    print(game1.get(3, 4).get_coor() + ":")
    print()
    print("                " + game1.get(3, 4).get_north().get_coor())
    print(
        "        "
        + game1.get(3, 4).get_west().get_coor()
        + " "
        + game1.get(3, 4).get_coor()
        + " "
        + game1.get(3, 4).get_east().get_coor()
    )
    print("                " + game1.get(3, 4).get_south().get_coor())
    print()


# ----Methods------------------------------------------------------

# full_game_to_array should convert a series of moves to a board state
# todo - right now it just puts the moves into an array, implement ^
# Example of a game record, each number referring to a round.
# 1. e2 e8 2. e3 e7 3. e4 e6 4. e3h g6v
def full_game_to_array(shorthand):
    # print(shorthand)
    count = -1
    moves = []
    for i in shorthand.split(" "):
        if i[1] == ".":
            count += 1
            moves.append([])
        else:
            moves[count].append(i)
    # print("This game has", count + 1, "rounds")
    # print(moves)
    return moves


# state_to_array converts a game state to a game object
# todo: return object
# Example of board state
# d4f4e7 / a2a8 / e4 e6 a4 h6 / 4 3 5 3 / 3
# horzontal walls / vertical walls / player pieces / walls remaining by player / which player's turn?
def state_to_array(shorthand):
    walls = [0, 0, 0, 0]
    # print(shorthand)
    temp = shorthand.split("/")
    temp[0] = temp[0].strip()
    temp[1] = temp[1].strip()
    temp[2] = temp[2].strip()
    temp[3] = temp[3].strip()
    temp[4] = temp[4].strip()

    num_players = temp[2].split(" ").__len__()
    assert num_players in range(1, 5)  # Python range is not inclusive.
    gameOut = game(9, num_players)

    # Horizontal Walls
    hori = [temp[0][i : i + 2] for i in range(0, len(temp[0]), 2)]
    for i in hori:
        x = ord(i[0]) - ord("`")
        y = int(i[1])
        gameOut.get(x, y).set_wall_h()

    # Vertical Walls
    verti = [temp[1][i : i + 2] for i in range(0, len(temp[1]), 2)]
    for i in verti:
        x = ord(i[0]) - ord("`")
        y = int(i[1])
        gameOut.get(x, y).set_wall_v()

    # players
    players = temp[2].split(" ")
    for i in range(len(players)):
        x = ord(players[i][0]) - ord("`")
        y = int(players[i][1])
        gameOut.get(x, y).val = i + 1

    walls = temp[3].split(" ")
    # for i in range(len(walls)):
    #     print(
    #         "Player "
    #         + (i + 1).__str__()
    #         + " has "
    #         + walls[i].__str__()
    #         + " walls remaining."
    #     )

    # print("It is Player " + temp[4] + "'s turn.")

    return gameOut


# dispatch allows function overloading
@dispatch(str)
def move_by_player(move):
    print("MOVE sent:", move)
    return move_by_player(move, "/ / e1 e9 / 10 10 / 1")


@dispatch(str, str)
def move_by_player(move, shorthand):
    print("MOVE sent:", move)
    game = state_to_array(shorthand)
    assert len(move) == 4  # move should be four char
    assert move[0] == "p"  # move should start with p prefix indicating player
    assert int(move[1]) in range(1, 5)  # player number should be 1,2,3
    assert ord(move[2]) in range(
        ord("a"), ord("a") + game.size
    )  # x coordinate should be a->(a+board size)
    assert int(move[3]) in range(1, game.size)  # y coordinate should be 1->board size
    players = [game.get_player(i) for i in range(1, game.get_num_players() + 1)]
    for i in range(len(players)):
        assert players[i] != None  # all players should exist

    print("distance between p1 & p2: ", players[0].distance(players[1]))
    players[int(move[1]) - 1].move(move[2:4])
    return game
