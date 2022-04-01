from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
from game_engine import *

hostName = "0.0.0.0"
hostPort = 8080

# MyServer hosts the game engine
# Manual routing is in the match functions (match is switch statement for Python)
class MyServer(BaseHTTPRequestHandler):
    def __init__(self):
        self.games = active_games()

    # Client wants data from the game engine
    def do_GET(self):
        self.send_response(200)
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
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            match self.path:
                # each endpoint can be a case here
                case "/decode":
                    self.wfile.write(
                        bytes(
                            state_to_array(post_body["state"]).__repr__(),
                            "utf-8",
                        )
                    )
                case "/move":
                    self.wfile.write(
                        bytes(
                            move_by_player(post_body["move"], post_body["state"]),
                            "utf-8",
                        )
                    )
                case "/new":
                    players = []
                    for i in range(1, post_body["num_players"] + 1):
                        players.append(
                            player(
                                post_body["player_" + str(i) + "_id"],
                                post_body["player_" + str(i) + "_name"],
                            )
                        )
                    self.games.add(
                        game(
                            post_body["id"], post_body["size"], post_body["num_players"]
                        )
                    )
                    for player in players:
                        self.games.get(post_body["id"]).add_player(player)
                    self.wfile.write(
                        bytes(
                            array_to_state(self.games.get(post_body["id"])),
                            "utf-8",
                        )
                    )

                case "/move2":
                    self.games.set(
                        post_body["id"],
                        move_by_player(
                            post_body["move"],
                            array_to_state(self.games.get(post_body["id"])),
                        ),
                    )
                    self.wfile.write(
                        bytes(
                            array_to_state(self.games.get(post_body["id"])),
                            "utf-8",
                        )
                    )

                case _:
                    self.wfile.write(
                        bytes(
                            "Error, invalid URL for POST request\n",
                            "utf-8",
                        )
                    )
        except:
            self.wfile.write(
                bytes(
                    "Error: Something went wrong",
                    "utf-8",
                )
            )


# Host the Server
myServer = HTTPServer((hostName, hostPort), MyServer)

print(time.asctime(), "Server Starting - %s:%s" % (hostName, hostPort))


# Test Cases
# print("Testing Engine conversion from shorthand to array...")
# game_engine.full_game_to_array("1. e2 e8 2. e3 e7 3. e4 e6 4. e3h g6v")
print(array_to_state(state_to_array("d4e7f4 / a2a8 / e4 e6 a4 h6 / 4 3 5 3 / 3")))
# game_engine.move_by_player("p1e3")
# game_engine.move_by_player("p1e2")

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))
