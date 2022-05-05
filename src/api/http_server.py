from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
import mysql.connector
from game_engine import *
import os


hostName = "0.0.0.0"
hostPort = 8080
games = active_games()
queue = queue()

db = mysql.connector.connect(
    user="root",
    password='Bxu<!yGaY"tj={J7b3U[T],qm9Ms>^ZL',
    host=os.getenv("DB_HOST"),
    # user = os.getenv('DB_USER'),
    # password = os.getenv('DB_PASSWORD'),
    port=os.getenv("DB_PORT"),
)
# creates database if not already exists
# db.cursor().execute("GRANT ALL PRIVILEGES ON *.* TO 'api'@'%' IDENTIFIED BY 'password'")
db.cursor().execute("CREATE DATABASE IF NOT EXISTS active_games")


db = mysql.connector.connect(
    user="root",
    password='Bxu<!yGaY"tj={J7b3U[T],qm9Ms>^ZL',
    host=os.getenv("DB_HOST"),
    # user = os.getenv('DB_USER'),
    # password = os.getenv('DB_PASSWORD'),
    database="active_games",
    port=os.getenv("DB_PORT"),
)

db_cursor = db.cursor()
db_cursor.execute(
    "CREATE TABLE IF NOT EXISTS games (id VARCHAR(50) PRIMARY KEY, str_rep VARCHAR(128))"
)
db_cursor.execute(
    "ALTER TABLE games ADD COLUMN IF NOT EXISTS (player1 VARCHAR(150), player2 VARCHAR(150), player3 VARCHAR(150), player4 VARCHAR(150))"
)
db_cursor.execute("DELETE FROM games WHERE player1 IS NULL")
db.commit()

# adding all games in db to active_games
db_cursor.execute("SELECT games.id FROM games ORDER BY id")
results = db_cursor.fetchall()

for x in results:
    sql = "SELECT games.str_rep FROM games WHERE id = %s"
    val = x
    db_cursor.execute(sql, val)
    rep = db_cursor.fetchall()
    rep_str = str(rep).replace("[('", " ")
    rep_str = str(rep_str).replace("',)]", " ")
    new_game = shorthand_to_game(rep_str)
    # sets game id
    id = str(x).replace("('", "")
    id = id.replace("',)", "")
    new_game.id = id
    # sets players
    # player1
    sql = "SELECT games.player1 FROM games WHERE id = %s"
    val = x
    db_cursor.execute(sql, val)
    player1 = str(db_cursor.fetchall())
    player1 = player1.replace("[('", "")
    player1 = player1.replace("',)]", "")
    #player2
    sql = "SELECT games.player2 FROM games WHERE id = %s"
    val = x
    db_cursor.execute(sql, val)
    player2 = str(db_cursor.fetchall())
    player2 = player2.replace("[('", "")
    player2 = player2.replace("',)]", "")
    # player3
    sql = "SELECT games.player3 FROM games WHERE id = %s"
    val = x
    db_cursor.execute(sql, val)
    player3 = str(db_cursor.fetchall())
    player3 = player3.replace("[(", "")
    player3 = player3.replace(",)]", "")
    player3 = player3.replace("'", "")
    player3 = player3.replace("'", "")
    #player4
    sql = "SELECT games.player4 FROM games WHERE id = %s"
    val = x
    db_cursor.execute(sql, val)
    player4 = str(db_cursor.fetchall())
    player4 = player4.replace("[(", "")
    player4 = player4.replace(",)]", "")
    player4 = player4.replace("'", "")
    player4 = player4.replace("'", "")
    # sets in new_game
    if player3 == "None":
        new_game.set_two_player(player(player1), player(player2))
    else:
        new_game.set_four_player(
            player(player1), player(player2), player(player3), player(player4)
        )
    # adds game
    games.add(new_game)


# MyServer hosts the game engine
# Manual routing is in the match functions (match is switch statement for Python)
class MyServer(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    # Client wants data from the game engine
    def do_GET(self):
        self.send_response(418)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(
            bytes(
                "<body><p>Error: Nothing is hosted on this server.</p></body></html>",
                "utf-8",
            )
        )

    # Client gives data to the game engine
    def do_POST(self):
        try:
            content_len = int(self.headers.get("Content-Length"))
            post_body = json.loads(self.rfile.read(content_len))
            match self.path:
                # need to pass game id, size, players(num of players), player1(id of player1)...
                case "/new":
                    if games.get(post_body["id"]) != None:
                        games.remove(post_body["id"])
                    new_game = game(
                        post_body["id"], post_body["size"], post_body["players"]
                    )
                    if post_body["players"] == 2:
                        new_game.set_two_player(
                            player(post_body["player1"]), player(post_body["player2"])
                        )
                    elif post_body["players"] == 4:
                        new_game.set_four_player(
                            player(post_body["player1"]),
                            player(post_body["player2"]),
                            player(post_body["player3"]),
                            player(post_body["player4"]),
                        )

                    # adding new game to sql database
                    if new_game.get_num_players() == 2:
                        sql = "INSERT INTO games (id, player1, player2, str_rep) VALUES (%s, %s, %s, %s)"
                        val = (
                            new_game.id,
                            new_game.players[0].get_id(),
                            new_game.players[1].get_id(),
                            new_game.__repr__(),
                        )
                    elif new_game.get_num_players() == 4:
                        sql = "INSERT INTO games (id, player1, player2, player3, player4, str_rep) VALUES (%s, %s, %s, %s, %s, %s)"
                        val = (
                            new_game.id.get_id(),
                            new_game.players[0].get_id(),
                            new_game.players[1].get_id(),
                            new_game.players[2].get_id(),
                            new_game.players[3].get_id(),
                            new_game.__repr__(),
                        )

                    success = False
                    while success == False:
                        try:
                            db_cursor.execute(sql, val)
                            db.commit()
                            success = True
                        except mysql.connector.InterfaceError:
                            time.sleep(100)
                            print("Reconnecting..")
                            db.reconnect()

                    games.add(new_game)
                    self.send_response(200)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(
                        bytes(
                            games.get(post_body["id"]).__repr__(),
                            "utf-8",
                        )
                    )

                case "/move":
                    curr_game = games.get(post_body["id"])
                    try:
                        curr_game.check_player(post_body["playerid"], post_body["move"])
                        curr_game.move(post_body["move"])
                        # updating curr_game in database
                        sql = "UPDATE games SET str_rep= %s WHERE id = %s"
                        val = (curr_game.__repr__(), post_body["id"])
                        db_cursor.execute(sql, val)
                        db.commit()

                        self.send_response(200)
                    except AssertionError:
                        self.send_response(400)
                        print("Invalid move")
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(
                        bytes(
                            games.get(post_body["id"]).__repr__(),
                            "utf-8",
                        )
                    )
                case "/get":
                    try:
                        curr_game = games.get(post_body["id"])
                        print("Sending game " + post_body["id"])
                        print("Game State: " + curr_game.__repr__())

                        self.send_response(200)
                    except AssertionError:
                        self.send_response(400)
                        print("Invalid Game ID")
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
                    self.send_header(
                        "Access-Control-Allow-Headers", "Content-Type, Authorization"
                    )
                    self.end_headers()
                    self.wfile.write(
                        bytes(
                            games.get(post_body["id"]).__repr__(),
                            "utf-8",
                        )
                    )

                case "/queue":
                    player_id = post_body["player_id"]
                    if queue.is_ready(post_body["size"], player_id):
                        temp_players = queue.get_players(post_body["size"])
                    else:
                        temp_players = []

                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
                    self.send_header(
                        "Access-Control-Allow-Headers", "Content-Type, Authorization"
                    )
                    self.end_headers()
                    match temp_players.__len__():
                        case 0:
                            out = {
                                "ready": False,
                            }
                        case 1:
                            out = {
                                "ready": True,
                                "p1": temp_players[0],
                            }
                        case 3:
                            out = {
                                "ready": True,
                                "p1": temp_players[0],
                                "p2": temp_players[1],
                                "p3": temp_players[2],
                            }

                    self.wfile.write(
                        bytes(
                            json.dumps(out),
                            "utf-8",
                        )
                    )

                case _:
                    self.send_response(418)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
                    print("Error, invalid URL for POST request\n")
                    self.wfile.write(
                        bytes(
                            "Error, invalid URL for POST request\n",
                            "utf-8",
                        )
                    )
        except Exception as e:
            self.send_response(418)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            print("Exception " + repr(e) + ": " + str(e))
            self.wfile.write(
                bytes(
                    "Exception " + repr(e) + ": " + str(e),
                    "utf-8",
                )
            )


# Host the Server
myServer = HTTPServer((hostName, hostPort), MyServer)

print(time.asctime(), "Server Starting - %s:%s" % (hostName, hostPort))

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))
