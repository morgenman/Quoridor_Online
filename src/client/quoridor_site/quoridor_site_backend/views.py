from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests, json
from django.views import generic
from .models import Profile, Game
from .forms import *
from .admin import *
from django.db.models import F
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


# import utils.py
from . import utils

# Create your views here.


def home(request):
    return render(request, "home.html")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


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
    game = Game()
    game.save()
    game.players.add(Profile.objects.filter(user=request.user).first())
    data = {
        "id": 1, #str(game.id),
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


def win(request):
    Profile.objects.all().update(wins=F("wins") + 1)

    # Put some sort of error message to user here
    return render(request, "home.html")


def lose(request):
    Profile.objects.all().update(losses=F("losses") + 1)

    # Put some sort of error message to user here
    return render(request, "home.html")


def js_test(request):
    return render(request, "js_test.html")


class ProfileDetailView(generic.DetailView):
    model = Profile


class ProfileListView(generic.ListView):
    model = Profile


class GameDetailView(generic.DetailView):
    model = Game


class GameListView(generic.ListView):
    model = Game
