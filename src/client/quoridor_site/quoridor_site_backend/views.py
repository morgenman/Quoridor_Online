import re
from tkinter import E
from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests, json
from django.views import generic
from .models import Profile, Game, User
from .forms import *
from .admin import *
from django.db.models import F
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect


# import utils.py
from . import utils

# Create your views here.

# home page
def home(request):
    return render(request, "home.html")


def help(request):
    return render(request, "help.html")


# prompts user to select a second player
def second_player(request):
    context = {}
    context["dataset"] = Profile.objects.exclude(user=request.user)
    context["player_id"] = request.user.id
    return render(request, "second_player.html", context)


# registers a user (creates User and corresponding Profile)
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        # if form has no errors
        if form.is_valid():
            # save user with given information
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            # logs new user in
            login(request, user)
            # redirect to home page
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


# requests name from user (should probably be removed)
def getName(request):
    return render(request, "get_name.html")


# sends name to api by user and displays response (should probably be removed)
def showName(request):
    name = request.POST["name"]
    headers = requests.structures.CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    url = "http://api:8080"
    data = {"name": name}
    x = requests.post(url, headers=headers, data=json.dumps(data))
    return HttpResponse(x)


# starts a new game
def new_game(request):

    # create a new game model (with default state)
    # adds both players (player1 being the current user)
    p1 = Profile.objects.filter(user=request.user).first()
    p2name = request.POST["id"]
    p2 = Profile.objects.filter(user=p2name).first()
    if p1 != p2:
        game = Game(player1=p1, player2=p2)
        game.save()
        # send request to api to make a new game
        url = "http://api:8080/new"
        headers = requests.structures.CaseInsensitiveDict()
        headers["Content-Type"] = "application/json"
        headers["charset"] = "UTF-8"
        # sets data to game's info (id, player1, player2)
        id = str(game.id)
        player1 = game.player1.id
        player2 = game.player2.id
        data = {
            "id": id,
            "player1": player1,
            "player2": player2,
            "players": 2,
            "size": 9,
        }
        x = requests.post(url, headers=headers, data=json.dumps(data))

        # if sent successfullly, render board
        if x.status_code == 200:
            board = utils.state_to_array(x.text)
            state = game.state
            return HttpResponseRedirect("/game/" + id)

    else:

        return redirect(request.META["HTTP_REFERER"])


# make a move in the current game
def make_move(request):
    # retrieve data from POST request
    tile = request.POST["tile"].lower()
    player = request.POST["player"]
    curr_player = Profile.objects.filter(user=request.user).first()
    playerid = curr_player.__str__()
    id = request.POST["id"]
    current_state = request.POST["state"]
    # send move request to api
    move = "p" + player + tile
    url = "http://api:8080/move"
    headers = requests.structures.CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["charset"] = "UTF-8"
    data = {"move": move, "id": id, "playerid": playerid}
    x = requests.post(url, headers=headers, data=json.dumps(data))
    # if legal move
    if x.status_code == 200:
        # grab the new state and make new board
        new_state = x.text
        board = utils.state_to_array(x.text)
        # update state of corresponding game model
        game = Game.objects.filter(id=id).first()
        game.state = new_state
        game.save()
        # render new board
        return HttpResponseRedirect("/game/" + game.id)
    # else if illegal move
    elif x.status_code == 400:
        # make board of original state
        board = utils.state_to_array(x.text)
        # TODO Put some sort of error message to user here
        # render original board
        # return render(
        #     request,
        #     "board.html",
        #     {"board": board, "id": id, "state": current_state},
        # )
        return get_game(request, id)


# adds a win to all profiles and goes back to home page
def win(request):
    Profile.objects.all().update(wins=F("wins") + 1)

    # Put some sort of error message to user here
    return render(request, "home.html")


# adds a loss to all profiles and goes back to home page
def lose(request):
    Profile.objects.all().update(losses=F("losses") + 1)

    # Put some sort of error message to user here
    return render(request, "home.html")


# testing page for js fancy board
def js_test(request):
    return render(request, "js_test.html")


class ProfileDetailView(generic.DetailView):
    model = Profile


class ProfileListView(generic.ListView):
    model = Profile


def second_player_debug(request):
    context = {}
    context["dataset"] = Profile.objects.exclude(user=request.user)
    context["state"] = "d4f4e7 / a2a8 / e4 e7 a4 h6 / 4 3 5 3 / 3"
    # horzontal walls / vertical walls / player pieces / available walls per player / active player

    return render(request, "second_player_debug.html", context)


# starts a new game
def debug(request):
    state = request.POST["state"]
    # create a new game model (with default state)
    game = Game()
    game.save()
    # adds both players (player1 being the current user)
    game.players.add(Profile.objects.filter(user=request.user).first())
    p2name = request.POST["player2"]
    p2user = User.objects.filter(username=p2name).first()
    p2 = Profile.objects.filter(user=p2user).first()

    return render(request, "debug.html", {"state": state})


def get_game(request, pk):
    game = Game.objects.filter(id=pk).first()
    # send request to api to make a new game
    url = "http://api:8080/get"
    headers = requests.structures.CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["charset"] = "UTF-8"
    # sets data to game's info (id, player1, player2)
    id = str(game.id)
    data = {"id": id}
    x = requests.post(url, headers=headers, data=json.dumps(data))
    # if sent successfullly, render board
    if x.status_code == 200:
        # grab the new state and make new board
        new_state = x.text
        # board = utils.state_to_array(x.text)
        # update state of corresponding game model
        game = Game.objects.filter(id=id).first()
        game.state = new_state
        game.save()
        # render new board
        return render(
            request,
            "board.html",
            {"board": "board", "id": id, "state": new_state},
        )

    # # else if illegal move
    # elif x.status_code == 400:
    #     # make board of original state
    #     #board = utils.state_to_array(x.text)
    #     # TODO Put some sort of error message to user here
    #     # render original board
    #     return render(
    #         request,
    #         "board.html",
    #         {"board": "board", "id": id, "state": current_state},
    #     )


class GameListView(generic.ListView):
    model = Game
