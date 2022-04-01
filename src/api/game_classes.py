import math
from multipledispatch import dispatch

# ----Data Structures----------------------------------------------

# Tile Class is equivalent to a 'node' data structure.
#
# Stores x,y, which player is in it, and all the edges that it connects to
class tile:
    def __init__(self, x, y, parent):
        self.x = x
        self.y = y
        self.val = 0
        self.parent = parent
        self.w_north = False
        self.w_east = False
        self.w_south = False
        self.w_west = False

    def move(self, move):
        destination = self.parent.get(move)
        assert destination != None  # destination should exist
        if self.distance(destination) >= 1:
            print("Invalid move")
        assert self.distance(destination) == 1  # destination should be adjacent
        destination.val = self.val
        self.val = 0

    def distance(self, tile):
        # a^2 + b^2 = c^2
        # floor to get int value
        return math.floor(
            math.sqrt(abs(self.x - tile.x) ** 2 + abs(self.y - tile.y) ** 2)
        )

    # return northern edge
    def get_north(self):
        if self.w_north:
            return None
        return self.parent.get(self.x, self.y + 1)

    # return eastern edge
    def get_east(self):
        if self.w_east:
            return None
        return self.parent.get(self.x + 1, self.y)

    # return southern edge
    def get_south(self):
        if self.w_south:
            return None
        return self.parent.get(self.x, self.y - 1)

    # return western edge
    def get_west(self):
        if self.w_west:
            return None
        return self.parent.get(self.x - 1, self.y)

    # return player character if player is present
    def get_val(self):
        if self.val == 1:
            return "x"
        if self.val == 2:
            return "o"
        if self.val == 3:
            return "@"
        if self.val == 4:
            return "*"
        return " "

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
            return "﹋" + self.get_val() + "﹋"
        if self.w_east:
            return " " + self.get_val() + "⏐"
        if self.w_south:
            return "﹏" + self.get_val() + "﹏"
        if self.w_west:
            return "⏐" + self.get_val() + " "
        return " " + self.get_val() + " "

    # an alternative to the __str__ function.
    # Basically when tile is expected to be the string type, return the coordinates
    def __repr__(
        self,
    ):
        return self.get_coor()

    # Probably legacy code, but returns html based on the value in the cell.
    # this is how we get the nice walls and colors, probably going to be moved to
    # the web container
    def html(
        self,
    ):
        out = "<td style='"
        if self.w_north:
            out += "border-top: 2px solid;"
        if self.w_east:
            out += "border-right: 2px solid;"
        if self.w_south:
            out += "border-bottom: 2px solid;"
        if self.w_west:
            out += "border-left: 2px solid;"
        if self.val == 1:
            out += "background-color:#bae1ff;"
        elif self.val == 2:
            out += "background-color:#baffc9;"
        elif self.val == 3:
            out += "background-color:#ffffba;"
        elif self.val == 4:
            out += "background-color:#ffdfba;"
        out += "'>"
        out += chr(ord("`") + self.x)
        out += self.y.__str__()
        out += "</td>"
        return out

    def get_coor(self):
        return "(" + chr(ord("`") + self.x) + self.get_char() + self.y.__str__() + ")"


# Game class basically stores an array of tile objects
# represents a game
# todo: implement move log (array of moves like in full_game_to_array method)
# stores the board, dimensions
class game:
    # initializes, verifies players and size are valid
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

    def set_four_player(self, player1, player2, player3, player4):
        self.players[0] = player1
        self.players[1] = player2
        self.players[2] = player3
        self.players[3] = player4

    # overloaded version of get which allows string form ie: "a1" -> (1,1)
    @dispatch(str)
    def get(self, string):
        print(string, ":", len(string))
        assert len(string) == 2
        assert ord(string[0]) in range(ord("a"), ord("a") + self.size)
        assert int(string[1]) in range(1, self.size + 1)
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
                if x.val == player:
                    return x
        return None

    # maybe this should be named html for consistency with tile
    # an alternative to the __str__ function.
    # Basically when board is expected to be the string type, return the html equivalent
    def __repr__(self):
        out = "<div id='wrapper'><h1>Converted Game Board:</h1>\
      <section id='left'><table><tbody>"
        for y in range(self.size):
            out += "<tr>"
            for x in range(self.size):
                out += self.get(x + 1, self.size - y).html()
            out += "</tr>"
        out += "</tbody></table></section>"
        out += "<section id='right'><table>\
      <tr><td style = 'background-color:#bae1ff;'>Player 1</td><td style = 'background-color:#baffc9;'>Player 2</td></tr>\
      <tr><td style = 'background-color:#ffffba;'>Player 3</td><td style = 'background-color:#ffdfba;'>Player 4</td></tr>\
      </table></section>"
        return out

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


class player:
    def __init__(self, id, name):
        self.id = id
        self.name = name


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
        size += 1

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
