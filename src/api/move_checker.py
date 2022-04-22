# Function that checks if the players move is valid or not
#
from game_classes import *
from multipledispatch import dispatch
import random

# player_tile = the tile of the player
players_tiles = [game.get_player(i) for i in range(1, game.get_num_players() + 1)]

# target = destination of where we want our piece to move to
target = game.get("b2")


@dispatch
def valid_player_move(players_tiles, target):
    # Checks if the tile you want to travel to is too far or not.
    distance_of_tile = players_tiles[0](tile.distance(target))
    if distance_of_tile > 1:
        # Distance is to far
        return False
    # Checks if another player is on the tile or not.
    if target(game.get_player()) == 0:
        return False
    # Checks if a wall is in the way but still need more work.
    if (
        target(tile.get_north())
        or target(tile.get_east())
        or target(tile.get_south())
        or target(tile.get_west())
    ):
        return False

    # if (insert weird special case like the going around other player)

    return True


valid_player_move(players_tiles, target)
