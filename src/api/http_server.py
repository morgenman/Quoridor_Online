from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
from game_engine import *

hostName = "0.0.0.0"
hostPort = 8080
games = active_games()

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


# Test Cases
# print("Testing Engine conversion from shorthand to array...")
# game_engine.full_game_to_array("1. e2 e8 2. e3 e7 3. e4 e6 4. e3h g6v")
print(shorthand_to_game("d4e7f4 / a2a8 / e4 e6 a4 h6 / 4 3 5 3 / 3"))
# game_engine.move_by_player("p1e3")
# game_engine.move_by_player("p1e2")

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))
