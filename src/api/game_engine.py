# Game Engine contains data structures and methods for the engine
# Notation info: https://quoridorstrats.wordpress.com/notation/

# function overloading

from game_classes import *
from multipledispatch import dispatch
import random


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


# shorthand_to_game converts a game state to a game object
# todo: return object
# Example of board state
# d4f4e7 / a2a8 / e4 e6 a4 h6 / 4 3 5 3 / 3
# horzontal walls / vertical walls / player pieces / walls remaining by player / which player's turn?
def shorthand_to_game(shorthand):
    # print(shorthand)
    temp = shorthand.split("/")
    temp[0] = temp[0].strip()
    temp[1] = temp[1].strip()
    temp[2] = temp[2].strip()
    temp[3] = temp[3].strip()
    temp[4] = temp[4].strip()

    num_players = temp[2].split(" ").__len__()
    assert num_players in range(1, 5)  # Python range is not inclusive.
    gameOut = game(random.randint(10, 99), 9, num_players)

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
    gameOut.players = [player(i) for i in range(len(players))]
    for i in range(len(players)):

        gameOut.get(players[i]).set_player(i + 1)

    walls = temp[3].split(" ")
    gameOut.set_walls(walls)

    gameOut.set_turn(temp[4])

    # print("It is Player " + temp[4] + "'s turn.")

    return gameOut
