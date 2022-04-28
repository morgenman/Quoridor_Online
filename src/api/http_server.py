from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
import mysql.connector
from game_engine import *
import os


hostName = "0.0.0.0"
hostPort = 8080
games = active_games()

db = mysql.connector.connect(
    user = 'root',
    password = 'Bxu<!yGaY"tj={J7b3U[T],qm9Ms>^ZL',
    host = os.getenv('DB_HOST'),
    #user = os.getenv('DB_USER'),
    #password = os.getenv('DB_PASSWORD'),
    port = os.getenv('DB_PORT'),
    #DB_HOST=db
    #DB_USER=api
    #DB_PASSWORD=password
    #DB_NAME=quoridor_db
    #DB_PORT=3306
)
#creates database if not already exists
#db.cursor().execute("GRANT ALL PRIVILEGES ON *.* TO 'api'@'%' IDENTIFIED BY 'password'")
db.cursor().execute('CREATE DATABASE IF NOT EXISTS active_games')

db = mysql.connector.connect(
    user = 'root',
    password = 'Bxu<!yGaY"tj={J7b3U[T],qm9Ms>^ZL',
    host = os.getenv('DB_HOST'),
    #user = os.getenv('DB_USER'),
    #password = os.getenv('DB_PASSWORD'),
    database = 'active_games',
    port = os.getenv('DB_PORT'),
    #DB_HOST=db
    #DB_USER=api
    #DB_PASSWORD=password
    #DB_NAME=quoridor_db
    #DB_PORT=3306
)

db_cursor = db.cursor()

db_cursor.execute("GRANT ALL PRIVILEGES ON *.* TO 'api'@'%'")
db_cursor.execute("CREATE TABLE games (str_rep VARCHAR(128))")

for x in db_cursor:
    print(x)

# MyServer hosts the game engine
# Manual routing is in the match functions (match is switch statement for Python)
class MyServer(BaseHTTPRequestHandler):

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
                        curr_game.move(post_body["move"])
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
                    self.end_headers()
                    self.wfile.write(
                        bytes(
                            games.get(post_body["id"]).__repr__(),
                            "utf-8",
                        )
                    )

                case _:
                    self.send_response(418)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
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
