from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
import game_engine

hostName = "0.0.0.0"
hostPort = 8080

class MyServer(BaseHTTPRequestHandler):
    # Client wants data from the game engine
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        match self.path:
            # each endpoint can be a case here
            case "/testing":
                self.wfile.write(bytes("<body><p>You got to Testing!</p>", "utf-8"))
        self.wfile.write(bytes("<p>You accessed path: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
    
    # Client gives data to the game engine
    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        post_body = json.loads(self.rfile.read(content_len))
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("I have detected that 'name' is " + post_body['name']+'\n',"utf-8"))
        print("I have detected that 'name' is " + post_body['name'])


myServer = HTTPServer((hostName, hostPort), MyServer)

print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

print("Testing Engine conversion from shorthand to array...")
game_engine.full_game_to_array("1. e2 e8 2. e3 e7 3. e4 e6 4. e3h g6v")  
game_engine.state_to_array("d4f4e7 / a2a8 / e4 e6 a4 h6 / 4 3 5 3 / 3")

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))