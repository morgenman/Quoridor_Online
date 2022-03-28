# these are copied from API, a few unecessary functions have been removed
# TODO: Clean this up a bit


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

    return gameOut


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

    # an alternative to the __str__ function.
    # Basically when tile is expected to be the string type, return the coordinates
    def __repr__(
        self,
    ):
        return self.get_coor()

    def html(self):
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
    def __init__(self, size, players):
        assert players > 1 & players < 5, f"{players} is an invalid number of players"
        assert size > 1 & size < 10, f"{size} is an invalid board size"
        self.size = size
        self.board = [
            [tile(1 + x, size - y, self) for x in range(size)] for y in range(size)
        ]
        self.num_players = players
        self.players = [players]

    # """returns the number of players"""
    def get_num_players(self):
        return self.num_players

    def get(self, x, y):  # 3 4
        return self.board[self.size - y][x - 1]  # 5 3

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


class player:
    def __init__(self):
        self.id = None
        self.name = None
        self.walls = 10

    def set_id(self, id):
        self.id = id

    def set_name(self, name):
        self.name = name

    def set_walls(self, num):
        self.walls = num

    def get_walls(self):
        return self.walls
