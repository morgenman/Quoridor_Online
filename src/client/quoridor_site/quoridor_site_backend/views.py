from django.shortcuts import render
from django.http import HttpResponse
import requests, json
from django.views import generic
from .models import Profile, Game
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


def new_game(request):
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
    x = requests.post(url, headers=headers, data=json.dumps(data))

    if x.status_code == 200:
        game = utils.state_to_array(x.text)
        return render(request, "board.html", {"board": game})


def make_move(request):
    tile = request.POST["tile"].lower()
    player = request.POST["player"]
    move = "p" + player + tile
    url = "http://api:8080/move"
    headers = requests.structures.CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["charset"] = "UTF-8"

    data = {"move": move, "id": 1}
    x = requests.post(url, headers=headers, data=json.dumps(data))
    if x.status_code == 200:
        game = utils.state_to_array(x.text)
        return render(request, "board.html", {"board": game})
    elif x.status_code == 400:
        game = utils.state_to_array(x.text)
        # Put some sort of error message to user here
        return render(request, "board.html", {"board": game})


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


class GameDetailView(generic.DetailView):
    model = Game


class GameListView(generic.ListView):
    model = Game
