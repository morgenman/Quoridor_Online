import math
from multipledispatch import dispatch
import copy


# ----Data Structures----------------------------------------------

# Tile Class is equiplayerent to a 'node' data structure.
#
# Stores x,y, which player is in it, and all the edges that it connects to
class tile:
    def __init__(self, x, y, game):
        self.x = x
        self.y = y
        self.player = 0
        self.game = game
        self.w_north = False
        self.w_east = False
        self.w_south = False
        self.w_west = False

    def distance(self, tile):
        # a^2 + b^2 = c^2
        # floor to get int playerue
        return math.floor(
            math.sqrt(abs(self.x - tile.x) ** 2 + abs(self.y - tile.y) ** 2)
        )

    # return northern edge
    def get_north(self):
        if self.w_north:
            return None
        return self.game.get(self.x, self.y + 1)

    # return eastern edge
    def get_east(self):
        if self.w_east:
            return None
        return self.game.get(self.x + 1, self.y)

    # return southern edge
    def get_south(self):
        if self.w_south:
            return None
        return self.game.get(self.x, self.y - 1)

    # return western edge
    def get_west(self):
        if self.w_west:
            return None
        return self.game.get(self.x - 1, self.y)

    # return True if there is a wall
    # return northern edge
    def if_north(self):
        return self.w_north

    # return eastern edge
    def if_east(self):
        return self.w_east

    # return southern edge
    def if_south(self):
        return self.w_south

    # return western edge
    def if_west(self):
        return self.w_west

    # return player character if player is present
    def get_player(self):
        return self.player

    def set_player(self, player):
        self.player = player

    # sets the horizontal wall flag.
    # Note: this actually affects two tile pieces:
    # first is a wall north of this tile
    # second is a wall north of the tile east to this wall
    def set_wall_h(self):
        # print("Horizontal wall at " + self.__repr__())
        self.get_north().w_south = True
        self.w_north = True
        self.get_east().get_north().w_south = True
        self.get_east().w_north = True

    # sets the vertical wall flag.
    # Note: this actually affects two tile pieces:
    # first is a wall east of this tile
    # second is a wall east of the tile north to this wall
    def set_wall_v(self):
        # print("Vertical wall at " + self.__repr__())
        self.get_north().get_east().w_west = True
        self.get_north().w_east = True
        self.get_east().w_west = True
        self.w_east = True

    # used for ascii board.
    # todo: trim legacy code
    def get_char(self):
        if self.w_north:
            return "﹋" + self.get_player() + "﹋"
        if self.w_east:
            return " " + self.get_player() + "⏐"
        if self.w_south:
            return "﹏" + self.get_player() + "﹏"
        if self.w_west:
            return "⏐" + self.get_player() + " "
        return " " + self.get_player() + " "

    # an alternative to the __str__ function.
    # Basically when tile is expected to be the string type, return the coordinates
    def __repr__(self):
        return self.get_coor()

    def get_coor(self):
        return (
            chr(ord("`") + self.x)
            + self.y.__str__()
            # + "player: "
            # + self.player.__str__()
            # + " N Wall: "
            # + self.w_north.__str__()
            # + " E Wall: "
            # + self.w_east.__str__()
        )


# Game class basically stores an array of tile objects
# represents a game
# todo: implement move log (array of moves like in full_game_to_array method)
# stores the board, dimensions
class game:
    # initializes, verifies players and size are playerid
    def __init__(self, id, size, players):
        assert players > 1 & players < 5, f"{players} is an invalid number of players"
        assert size > 1 & size < 10, f"{size} is an invalid board size"
        self.id = id
        self.size = size
        # this board is very confusing to look at.
        # it is a 2d array of tile objects, arranged so the first tile
        # (board[0][0]) is the top left corner and the last tile is
        # in the bottom right corner (board[size-1][size-1])
        self.board = [
            [tile(1 + x, size - y, self) for x in range(size)] for y in range(size)
        ]
        self.num_players = players
        self.players = [None for i in range(players)]
        self.walls = []
        self.turn = 1

    def move(self, move):
        player = self.get_player(int(move[1]))
        destination = self.get(move[2:])
        if self.valid_player_move(player, destination):
            player.set_player(0)
            destination.set_player(int(move[1]))

    # function that checks if the player move is valid or not
    def valid_player_move(self, player, target):
        distance = player.distance(target)
        user = copy.deepcopy(player)
        # Jumping over player case
        if distance == 2:
            # if target is north of player
            if target.x == user.x and target.y == user.y + 2:
                location = copy.deepcopy(player.get_north())
                if location.get_player() != 0:
                    print("Jump")
                    return True
            # if target is east of player
            elif target.x == user.x + 2 and target.y == user.y:
                location = copy.deepcopy(player.get_east())
                if location.get_player() != 0:
                    print("Jump")
                    return True
            # if target is south of player
            elif target.x == user.x and target.y == user.y - 2:
                location = copy.deepcopy(player.get_south())
                if location.get_player() != 0:
                    print("Jump")
                    return True
            # if target is west of player
            elif target.x == user.x - 2 and target.y == user.y:
                location = copy.deepcopy(player.get_west())
                if location.get_player() != 0:
                    print("Jump")
                    return True

        # Checks if the tile you want to travel to is too far or not.
        if distance > 1:
            # Distance is too far
            print("Invalid move")
            return False

        # Checks if another player is on the tile or not.
        if target.get_player() != 0:
            print("Inalid move")
            return False

        # Checks if a wall is in the way.
        # if target is north of player
        if target.x == user.x and target.y == user.y + 1:
            return player.if_north()
        # if target is east of player
        elif target.x == user.x + 1 and target.y == user.y:
            return player.if_east()
        # if target is south of player
        elif target.x == user.x and target.y == user.y - 1:
            return player.if_south()
        # if target is west of player
        elif target.x == user.x - 1 and target.y == user.y:
            return player.if_west()

        # if (insert weird special case like the going around other player)
        return True

    # checks who's turn it is to who's sending the move request
    def check_player(self, playerid, move):
        curr_player = self.players[int(self.get_turn()) - 1]
        assert curr_player.get_id() == playerid, f"it is not {playerid}'s turn"
        assert (
            self.get_turn() == move[1]
        ), f"{playerid} cannot move {curr_player.get_id()}'s piece"

    def set_walls(self, walls):
        self.walls = walls

    def get_walls(self):
        return self.walls

    def set_turn(self, turn):
        self.turn = turn

    def next(self):
        if self.turn == self.num_players:
            self.turn = 1
        else:
            self.turn += 1

    def get_turn(self):
        return self.turn

    # """returns the number of players"""
    def get_num_players(self):
        return self.num_players

    def set_two_player(self, player1, player2):
        self.players[0] = player1
        self.players[1] = player2
        self.get("e1").set_player(1)
        self.get("e9").set_player(2)
        self.walls = [10, 10]

    def set_four_player(self, player1, player2, player3, player4):
        self.players[0] = player1
        self.players[1] = player2
        self.players[2] = player3
        self.players[3] = player4
        self.get("e1").set_player(1)
        self.get("a5").set_player(2)
        self.get("e9").set_player(3)
        self.get("i5").set_player(4)
        self.walls = [10, 10, 10, 10]

    # overloaded version of get which allows string form ie: "a1" -> (1,1)
    @dispatch(str)
    def get(self, string):
        assert len(string) == 2, f"{string} is not a valid coordinate (type 1)"
        assert ord(string[0]) in range(
            ord("a"), ord("a") + self.size
        ), f"{string} is not a valid coordinate (type 2)"
        assert int(string[1]) in range(
            1, self.size + 1
        ), f"{string} is not a valid coordinate (type 3)"
        x = ord(string[0]) - ord("a") + 1
        y = int(string[1])
        return self.get(x, y)

    # returns the tile at the given coordinates
    @dispatch(int, int)
    def get(self, x, y):  # 3 4
        return self.board[self.size - y][x - 1]  # 5 3

    # returns the tile of the player
    def get_player(self, player):
        for y in self.board:
            for x in y:
                if x.player == player:
                    return x
        return None

    # legacy code
    # ascii art representation of board
    def draw(self):
        print(
            "------------------------------------------------------------------------------------------------------------------------------------------"
        )
        print()
        for y in range(self.size):
            for x in range(self.size):
                print(self.get(x + 1, self.size - y), end="      \t")
            print()
            print()
        print(
            "------------------------------------------------------------------------------------------------------------------------------------------"
        )

    def __repr__(self):
        bd = self.board
        size = self.size
        h_walls = []
        v_walls = []
        player_listNum = []
        player_piece = []
        ignore_h = ignore_v = False
        for y in range(size):
            for x in range(size):
                tile = self.get(x + 1, y + 1)
                if tile.w_north is True:
                    code = tile.get_coor()
                    if not ignore_h:
                        h_walls.append(code)
                        ignore_h = True
                    else:
                        ignore_h = False
                if tile.w_east is True:
                    code = tile.get_coor()
                    if not ignore_v:
                        v_walls.append(code)
                        ignore_v = True
                    else:
                        ignore_v = False
                if tile.get_player() > 0:
                    player_piece.append(tile)

        # print(h_walls)
        # print(v_walls)
        # h_walls = h_walls[::2]
        # v_walls = v_walls[1::2]
        h_walls.sort()
        v_walls.sort()
        temp = [None for i in range(self.num_players)]
        for player in player_piece:
            temp[player.get_player() - 1] = player.get_coor()
        player_piece = temp
        for walls in self.get_walls():
            player_listNum.append(walls)

        hwStr = "".join([str(element) for element in h_walls])
        vwStr = "".join([str(element) for element in v_walls])
        piece = " ".join([str(element) for element in player_piece])
        endCount = " ".join([str(element) for element in player_listNum])

        turn = self.get_turn()

        # End hold the final String
        end = (
            (hwStr)
            + " / "
            + (vwStr)
            + " / "
            + (piece)
            + " / "
            + (endCount)
            + " / "
            + (turn.__str__())
        )
        return end


class player:
    def __init__(self, id):
        self.id = id

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id


# Active Games class stores all the currently active games
class active_games:
    # initialize active_games with an empty games array
    @dispatch()
    def __init__(self):
        self.games = []
        self.size = 0

    # initialize active_games with the given games array
    @dispatch(list)
    def __init__(self, games):
        self.games = games
        self.size = len(self.games)

    # adds a game to the games array
    def add(self, game):
        self.games.append(game)
        self.size += 1

    # removes game with given id from games array
    def remove(self, id):
        game = self.get(id)
        self.games.remove(game)
        self.size -= 1

    # returns game in array with given id
    def get(self, id):
        for x in range(self.size):
            if self.games[x].id == id:
                return self.games[x]
        return None

    def set(self, id, game):
        for x in range(self.size):
            if self.games[x].id == id:
                self.games[x] = game
                return True
        return False


class queue:
    def __init__(self):
        self.two_queue = []
        self.four_queue = []

    def add_two(self, player):
        if player not in self.two_queue:
            self.two_queue.append(player)

    def add_four(self, player):
        if player not in self.four_queue:
            self.four_queue.append(player)

    def is_ready(self, size, player):
        cutoff = 0
        assert size == 2 or size == 4, "Invalid size"
        if size == 2:
            if player in self.two_queue:
                cutoff = 2
            else:
                cutoff = 1

            if len(self.two_queue) >= cutoff:
                return True
            else:
                return False
        else:
            if player in self.four_queue:
                cutoff = 4
            else:
                cutoff = 3

            if len(self.four_queue) >= cutoff:
                return True
            else:
                return False

    def get_players(self, size):
        assert size == 2 or size == 4, "Invalid size"
        if size == 2:
            return self.two_queue.pop(0)
        else:
            temp = [
                self.four_queue.pop(0),
                self.four_queue.pop(0),
                self.four_queue.pop(0),
            ]
            return temp
