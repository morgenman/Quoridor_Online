# Class that checks if the players move and if the player wall were placed correctly or not.
from game_classes import tile
from multipledispatch import dispatch
import random


class move_checker:
    def __init__(self, player, num_players, target, distance):
        # The position the player is currently in
        self.player = game.get_player
        # How many players there are
        self.num_players = game.get_num_players
        # Target = destination of where we want our piece to move to
        self.target = game.get
        # Checks the distance by taking in the tile we would like to check for.
        self.distance = tile.distance

    # players_tiles = [player(i) for i in range(1, num_players + 1)]

    # function that checks if the player move is valid or not
    def valid_player_move(player, target, distance):
        # Checks if the tile you want to travel to is too far or not.
        distance_of_tile = player[0](distance(target))
        if distance_of_tile > 1:
            # Distance is to far
            return False

        # Checks if another player is on the tile or not.
        if target(player) == 0:
            return False

        # Checks if a wall is in the way.
        #if target is north of player
        if target.x == player.x and target.y == player.y + 1:
            return player.get_north()
        #if target is east of player
        elif target.x == player.x + 1 and target.y == player.y:
            return player.get_east()
        #if target is south of player
        elif target.x == player.x and target.y == player.y - 1:
            return player.get_south()
        #if target is west of player
        elif target.x == player.x - 1 and target.y == player.y:
            return player.get_west()

        # target(tile.get_north())
        # or target(tile.get_east())
        # or target(tile.get_south())
        # or target(tile.get_west())

        # if (insert weird special case like the going around other player)
        return True

    # function that checks if the wall you are trying to place is valid or not
    def valid_wall_move():
        return True


# prints the Instance of the User

user1 = move_checker("a1", 2, "b3", "b1")
print("User instance below")
print(user1)
