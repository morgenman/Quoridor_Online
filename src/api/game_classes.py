from asyncio.windows_events import NULL
import math
import maiadb as db
import numpy
from multipledispatch import dispatch


# numpy data types (for converting games to binary)
gamedt = NULL
tiledt = numpy.dtype(
    [
        ("x", numpy.int32),
        ("y", numpy.int32),
        ("player", numpy.int32),
        ("game", gamedt),
        ("w_north", numpy.bool),
        ("w_east", numpy.bool),
        ("w_south", numpy.bool),
        ("w_west", numpy.bool),
    ]
)
# may have to change id
gamedt = numpy.dtype(
    [
        ("id", numpy.string),
        ("size", numpy.int32),
        ("num_players", numpy.int32),
        # hope this one works
        ("board", numpy.array(dtype=numpy.array(dtype=tiledt))),
        ("walls", numpy.array()),
        ("turn", numpy.int32),
    ]
)

playerdt = numpy.dtype([('id' = numpy.string)])

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
        assert destination != None, f"Destination cannot be empty"
        if player.distance(destination) > 1:
            print("Invalid move")
        assert (
            player.distance(destination) == 1
        ), f"{player.distance(destination)} is too many tiles away to be a valid move"
        assert (
            destination.get_player() == 0
        ), f"{destination.get_player()} is already occupied"
        player.set_player(0)
        destination.set_player(int(move[1]))

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

    # name = db, use env veriables DB_USER, DB_PASSWORD
    # env variables:

    # DB_HOST=db
    # DB_USER=api
    # B_PASSWORD=password
    # DB_NAME=quoridor_db
    # DB_PORT=3306

    # convert to binary
    # store in db // update db when nessecary
    # pull from db on boot-up // make db if not already there
    #
    #
    #
    # def convert_to_binary(self):
    #
    #
    # def mariadb_connect(db_name)
    #
    #
    #
    # def insert_file(file_name, db_name, table_name):
    #
    # def rebuild(db_name, table_name)
