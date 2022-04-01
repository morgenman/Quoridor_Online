import requests, json


def new_game():
    url = "http://api:8080/new"
    headers = requests.structures.CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["charset"] = "UTF-8"

    # TODO replace ids with game id and player ids
    data = {
        "id": 1,
        "player1": 11,
        "player2": 12,
        "players": 2,
        "size": 9,
    }

    return requests.post(url, headers=headers, data=json.dumps(data))


print(new_game().text)


def make_move(move, player):
    tile = move
    move = "p" + player.__str__() + tile
    url = "http://api:8080/move"
    headers = requests.structures.CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["charset"] = "UTF-8"
    data = {"move": move, "id": 1}
    return requests.post(url, headers=headers, data=json.dumps(data))


print(make_move("e2", 1).text)
