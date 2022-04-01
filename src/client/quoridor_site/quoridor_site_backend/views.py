from django.shortcuts import render
from django.http import HttpResponse
import requests, json
from django.views import generic
from .models import Profile, Games
from .admin import *

# import utils.py
from . import utils

# Create your views here.


def home(request):
    return render(request, "home.html")


def getName(request):
    return render(request, "get_name.html")


def showName(request):
    name = request.POST["name"]
    headers = requests.structures.CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    url = "http://api:8080"
    data = {"name": name}
    x = requests.post(url, headers=headers, data=json.dumps(data))
    return HttpResponse(x)


def game_state(request):
    return render(request, "game_state_demo.html")


# get_board pushes the game state string to the api and passes through
# the returned html to the board.html template page
def get_board(request):
    state = request.POST["state"]
    url = "http://api:8080/decode"
    headers = requests.structures.CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["charset"] = "UTF-8"
    data = {"state": state}
    x = requests.post(url, headers=headers, data=json.dumps(data))
    return render(request, "board.html", {"board": x.text, "state": state})


def new_game(request):
    state = "/ / e1 e9 / 10 10 / 1"
    url = "http://api:8080/decode"
    headers = requests.structures.CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["charset"] = "UTF-8"
    data = {"state": state}
    x = requests.post(url, headers=headers, data=json.dumps(data))
    game = utils.state_to_array(state)
    return render(request, "board.html", {"board": game, "state": state})


def make_move(request):
    tile = request.POST["tile"].lower()
    state = request.POST["state"]
    player = request.POST["player"]
    temp = state.split("/")

    move = "p" + player + tile
    url = "http://api:8080/move"
    headers = requests.structures.CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["charset"] = "UTF-8"
    data = {"move": move, "state": state}
    x = requests.post(url, headers=headers, data=json.dumps(data))
    # if x.text is empty return the same board
    if (x.text == None) | (x.text == "") | (x.text == "Error: Something went wrong"):
        return render(
            request, "board.html", {"board": request.POST["board"], "state": state}
        )
    else:
        # Cole will explain this cryptic line later
        state = state.replace(temp[2].strip().split(" ")[int(player) - 1][0:2], tile)
        return render(request, "board.html", {"board": x.text, "state": state})


def player(request):
    """View function for user page of site."""

    num_wins = Profile.wins
    num_losses = Profile.losses
    context = {
        "num_wins": num_wins,
        "num_losses": num_losses,
    }
    # Profile.wins += 1
    # Profile.save()
    # Render the HTML template user.html with the data in the context variable
    return render(request, "player.html", context=context)


class ProfileDetailView(generic.DetailView):
    model = Profile


class ProfileListView(generic.ListView):
    model = Profile


class GamesListView(generic.ListView):
    model = Games
