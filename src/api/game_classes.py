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
        self.can_place = True

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

    # returns edges regardless of wall placement
    # return northern edge
    def get_true_north(self):
        return self.game.get(self.x, self.y + 1)

    # return eastern edge
    def get_true_east(self):
        return self.game.get(self.x + 1, self.y)

    # return southern edge
    def get_true_south(self):
        return self.game.get(self.x, self.y - 1)

    # return western edge
    def get_true_west(self):
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
        if self.can_place and (self.get_true_east().get_north() != None):
            # print("Horizontal wall at " + self.__repr__())
            self.get_true_north().w_south = True
            self.w_north = True
            self.get_true_east().get_true_north().w_south = True
            self.get_true_east().w_north = True
            self.can_place = False

    # sets the vertical wall flag.
    # Note: this actually affects two tile pieces:
    # first is a wall east of this tile
    # second is a wall east of the tile north to this wall
    def set_wall_v(self):
        if self.can_place and (self.get_true_north().get_east() != None):
            # print("Vertical wall at " + self.__repr__())
            self.get_true_north().get_true_east().w_west = True
            self.get_true_north().w_east = True
            self.get_true_east().w_west = True
            self.w_east = True
            self.can_place = False

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
        self.checked = []

    def move(self, move):
        player = self.get_player(int(move[1]))
        destination = self.get(move[2:])
        print("player is " + str(player))
        print("destination is " + str(destination))
        # print("valid move is " + str(self.valid_player_move(player, destination)))

        if self.valid_player_move(player, destination):
            print("hmm2")
            player.set_player(0)
            destination.set_player(int(move[1]))
            self.next()

    # function that checks if the player move is valid or not
    def valid_player_move(self, player, target):
        distance = player.distance(target)
        user = copy.deepcopy(player)
        print("distance = " + str(distance))

        # Jumping over player case
        if distance == 2:
            # if target is north of player
            if target.x == user.x and target.y == user.y + 2:
                location = copy.deepcopy(player.get_north())
                if self.check_walls(player, location):
                    if self.check_walls(location, target):
                        if location.get_player() != 0:
                            print("Jump")
                            return True
            # if target is east of player
            elif target.x == user.x + 2 and target.y == user.y:
                location = copy.deepcopy(player.get_east())
                if self.check_walls(player, location):
                    if self.check_walls(location, target):
                        if location.get_player() != 0:
                            print("Jump")
                            return True
            # if target is south of player
            elif target.x == user.x and target.y == user.y - 2:
                location = copy.deepcopy(player.get_south())
                if self.check_walls(player, location):
                    if self.check_walls(location, target):
                        if location.get_player() != 0:
                            print("Jump")
                            return True
            # if target is west of player
            elif target.x == user.x - 2 and target.y == user.y:
                location = copy.deepcopy(player.get_west())
                if self.check_walls(player, location):
                    if self.check_walls(location, target):
                        if location.get_player() != 0:
                            print("Jump")
                            return True

        # Moving diagonal next to another player case
        if distance != 1:
            # if target is northeast of player
            if target.x == user.x + 1 and target.y == user.y + 1:
                # If the opposing player is to the east
                if player.get_east().get_player() != 0:
                    location = copy.deepcopy(player.get_east())
                    if self.check_walls(player, location):
                        # Check for the wall behind the opposing player, required for this case
                        if location.if_east():
                            if self.check_walls(location, target):
                                if location.get_player() != 0:
                                    print("NE Diagonal")
                                    return True
                # If the opposing player is to the north
                else:
                    location = copy.deepcopy(player.get_north())
                    if self.check_walls(player, location):
                        # Check for the wall behind the opposing player, required for this case
                        if location.if_north():
                            if self.check_walls(location, target):
                                if location.get_player() != 0:
                                    print("NE Diagonal")
                                    return True
            # if target is southeast of player
            elif target.x == user.x + 1 and target.y == user.y - 1:
                # If the opposing player is to the east
                if player.get_east().get_player() != 0:
                    location = copy.deepcopy(player.get_east())
                    if self.check_walls(player, location):
                        # Check for the wall behind the opposing player, required for this case
                        if location.if_east():
                            if self.check_walls(location, target):
                                if location.get_player() != 0:
                                    print("SE Diagonal")
                                    return True
                # If the opposing player is to the south
                else:
                    location = copy.deepcopy(player.get_south())
                    if self.check_walls(player, location):
                        # Check for the wall behind the opposing player, required for this case
                        if location.if_south():
                            if self.check_walls(location, target):
                                if location.get_player() != 0:
                                    print("SE Diagonal")
                                    return True
            # if target is southwest of player
            elif target.x == user.x - 1 and target.y == user.y - 1:
                # If the opposing player is to the west
                if player.get_west().get_player() != 0:
                    location = copy.deepcopy(player.get_west())
                    if self.check_walls(player, location):
                        # Check for the wall behind the opposing player, required for this case
                        if location.if_west():
                            if self.check_walls(location, target):
                                if location.get_player() != 0:
                                    print("SW Diagonal")
                                    return True
                # If the opposing player is to the south
                else:
                    location = copy.deepcopy(player.get_south())
                    if self.check_walls(player, location):
                        # Check for the wall behind the opposing player, required for this case
                        if location.if_south():
                            if self.check_walls(location, target):
                                if location.get_player() != 0:
                                    print("SW Diagonal")
                                    return True
            # if target is northwest of player
            elif target.x == user.x - 1 and target.y == user.y + 1:
                # If the opposing player is to the west
                if player.get_west().get_player() != 0:
                    location = copy.deepcopy(player.get_west())
                    if self.check_walls(player, location):
                        # Check for the wall behind the opposing player, required for this case
                        if location.if_west():
                            if self.check_walls(location, target):
                                if location.get_player() != 0:
                                    print("NW Diagonal")
                                    return True
                # If the opposing player is to the north
                else:
                    location = copy.deepcopy(player.get_north())
                    if self.check_walls(player, location):
                        # Check for the wall behind the opposing player, required for this case
                        if location.if_north():
                            if self.check_walls(location, target):
                                if location.get_player() != 0:
                                    print("NW Diagonal")
                                    return True

        # Checks if the tile you want to travel to is too far or not.
        if distance > 1:
            # Distance is too far
            print("It's too far! Invalid move")
            return False

        # Checks if another player is on the tile or not.
        if target.get_player() != 0:
            print("There's another player there! Invalid move")
            return False

        # Checks if a wall is in the way.
        print("Wall check")
        return self.check_walls(player, target)

        # if (insert weird special case like the going around other player)
        # return True

    # Checks if there is a wall between any two tiles. Returns False if there is a wall
    def check_walls(self, player, target):
        user = copy.deepcopy(player)
        if target.x == user.x and target.y == user.y + 1:
            return not player.if_north()
        # if target is east of player
        elif target.x == user.x + 1 and target.y == user.y:
            return not player.if_east()
        # if target is south of player
        elif target.x == user.x and target.y == user.y - 1:
            return not player.if_south()
        # if target is west of player
        elif target.x == user.x - 1 and target.y == user.y:
            return not player.if_west()
        return True

    # places horizintal walls while checking for valid path
    def place_wall_h(self, wall):
        # fails if the player doesn't have any walls to place
        if int(self.walls[int(self.get_turn()) - 1]) < 1:
            print("player" + str(self.get_turn()) + " has no more walls")
            return None
        # makes copy of game with added wall
        temp_game = copy.deepcopy(self)
        wall_tile = temp_game.get(wall)

        # check if a wall can be placed there
        if wall_tile.can_place and (wall_tile.get_true_east().get_north() != None):
            wall_tile.set_wall_h()
        else:
            print("a wall cannot be placed there")
            return None
        # print(temp_game.__repr__())
        # if all players pass, place wall in actual game
        if temp_game.all_players_can_reach():
            self.get(wall).set_wall_h()
            self.walls[int(self.get_turn()) - 1] = (
                int(self.walls[int(self.get_turn()) - 1]) - 1
            )
            self.next()
            print("successfully placed a horizontal wall at " + str(wall))

    # places vertical walls while checking for valid path
    def place_wall_v(self, wall):
        # fails if the player doesn't have any walls to place
        if int(self.walls[int(self.get_turn()) - 1]) < 1:
            print("player" + str(self.get_turn()) + " has no more walls")
            return None
        # makes copy of game with added wall
        temp_game = copy.deepcopy(self)
        wall_tile = temp_game.get(wall)

        # check if a wall can be placed there
        if wall_tile.can_place and (wall_tile.get_true_north().get_east() != None):
            wall_tile.set_wall_v()
        else:
            print("a wall cannot be placed there")
            return None
        # print(temp_game.__repr__())
        # if all players pass, place wall in actual game
        if temp_game.all_players_can_reach():
            self.get(wall).set_wall_v()
            self.walls[int(self.get_turn()) - 1] = (
                int(self.walls[int(self.get_turn()) - 1]) - 1
            )
            self.next()
            print("successfully placed a vertical wall at " + str(wall))

    # check that all player can reach their desired end
    def all_players_can_reach(self):
        # checks for 2 player game
        if self.num_players == 2:
            # print("player 1 is " + self.players[0].__str__())
            # print("player 1 is at " + self.get_player(1))
            # checks if player 1 can reach the end, if not fails
            start = self.get_player(1)
            if not self.can_reach_level(start, 9):
                print("player 1 can't reach row 1")
                return False
            # checks if player 2 can reach the end, if not fails
            start = self.get_player(2)
            if not self.can_reach_level(start, 1):
                print("player 2 can't reach row 9")
                return False
        # checks for 4 player game
        elif self.num_players == 4:
            # checks if player 1 can reach the end, if not fails
            start = self.get_player(1)
            if not self.can_reach_level(start, 9):
                print("player 1 can't reach row 9")
                return False
            # checks if player 2 can reach the end, if not fails
            start = self.get_player(2)
            if not self.can_reach_level(start, -9):
                print("player 2 can't reach row i")
                return False
            # checks if player 3 can reach the end, if not fails
            start = self.get_player(3)
            if not self.can_reach_level(start, 1):
                print("player 3 can't reach row 1")
                return False
            # checks if player 4 can reach the end, if not fails
            start = self.get_player(4)
            if not self.can_reach_level(start, -1):
                print("player 4 can't reach row a")
                return False
        return True

    # check if player at given tile can reach the specified level
    # use positive level value for y direction, and negative values for x direction
    def can_reach_level(self, player, level):
        self.checked = []
        return self.reached(player, player, level, 0)

    def reached(self, player, checking, level, iterations):
        # if tile checking doesnt exist, return false
        if checking == None:
            # print("Node is None")
            return False
        # if tile already checked, return false, otherwise, add to checked
        if checking.__repr__() in self.checked:
            return False
        self.checked.append(checking.__repr__())
        # check if tile is at desired level
        if int(checking.y) == level:
            return True
        elif int(checking.x) == -level:
            return True
        # if checked 81 tiles (entire board) return false
        if iterations >= 9 * 9:
            return False
        # otherwise check all other tile directions

        # print(
        #    "checking "
        #    + checking.__repr__()
        #    + "; distance: "
        #    + str(player.distance(checking))
        #    + "; iterations: "
        #    + str(iterations)
        #    + "; checked: "
        #    + str(self.checked)
        # )

        iterations += 1

        # check north
        if self.reached(player, checking.get_north(), level, iterations):
            return True
        # check east
        if self.reached(player, checking.get_east(), level, iterations):
            return True
        # check south
        if self.reached(player, checking.get_south(), level, iterations):
            return True
        # check west
        if self.reached(player, checking.get_west(), level, iterations):
            return True
        # print("Reached the end of " + checking.__repr__())
        return False

    # checks who's turn it is to who's sending the move request
    def check_player(self, playerid):
        curr_player = self.players[int(self.get_turn()) - 1]
        print(
            "Current Player ID: "
            + str(curr_player.get_id())
            + "; Player attempting to make move: "
            + str(playerid)
        )
        assert int(curr_player.get_id()) == int(
            playerid
        ), f"it is not {playerid}'s turn"

    def check_piece(self, move):
        print(str(self.get_turn()) + " and " + move[1])
        assert int(self.get_turn()) == int(
            move[1]
        ), f"player{str(self.get_turn())} cannot move player{move[1]}'s piece"

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
            self.turn = int(self.turn) + 1

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
        x = ord(string[0]) - ord("a") + 1
        y = int(string[1])
        return self.get(x, y)

    # returns the tile at the given coordinates
    @dispatch(int, int)
    def get(self, x, y):  # 3 4
        if x < 1 or x > 9 or y < 1 or y > 9:
            return None
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

    def __repr__(self):
        return self.id

    def __len__(self):
        return 1


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

    def __repr__(self):
        return str(self.two_queue) + "\n " + str(self.four_queue)

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
            temp = [self.two_queue.pop(0).id]
            return temp
        else:
            temp = [
                self.four_queue.pop(0).id,
                self.four_queue.pop(0).id,
                self.four_queue.pop(0).id,
            ]
            return temp
