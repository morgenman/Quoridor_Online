import requests, json

def new_game():
  state = "/ / e1 e9 / 10 10 / 1"
  url = "http://api:8080/decode"
  headers = requests.structures.CaseInsensitiveDict()
  headers["Content-Type"] = "application/json"
  headers["charset"] = "UTF-8"
  data = {"state": state}
  return requests.post(url, headers=headers, data=json.dumps(data))


def make_move(move,state,player):
  tile = move
  temp = state.split("/")
  move = "p" + player + tile
  url = "http://api:8080/move"
  headers = requests.structures.CaseInsensitiveDict()
  headers["Content-Type"] = "application/json"
  headers["charset"] = "UTF-8"
  data = {"move": move, "state": state}
  return requests.post(url, headers=headers, data=json.dumps(data))

