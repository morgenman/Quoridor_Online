import re
from tkinter import E
from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests, json
from django.views import generic
from .models import Profile, Game, User
from .forms import *
from django.db.models import Q
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
    if request.user.is_anonymous == False:
        playerid = str(Profile.objects.filter(user=request.user).first().id)
        active_games = Game.objects.filter(Q(player1=playerid) | Q(player2=playerid))
        active_games = active_games.filter(is_active=True)
        context = {"active_games": active_games}
    else:
        context = {"active_games": []}
    return render(request, "home.html", context=context)


def help(request):
    return render(request, "help.html")


# prompts user to select a second player
def second_player(request):
    context = {}
    context["dataset"] = Profile.objects.exclude(user=request.user)
    context["player_id"] = str(Profile.objects.get(user=request.user).id)
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


# starts a new game
def new_game(request):

    # create a new game model (with default state)
    # adds both players (player1 being the current user)
    p1 = Profile.objects.filter(user=request.user).first()
    p2name = request.POST["id"]
    p2 = Profile.objects.filter(id=p2name).first()
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
        player1 = str(game.player1.id)
        player2 = str(game.player2.id)
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

    playerid = str(Profile.objects.filter(player=curr_player).first().id)
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
        # update state of corresponding game model
        game = Game.objects.filter(id=id).first()
        game.state = new_state
        game.save()
        # render new board
        return HttpResponseRedirect("/game/" + str(game.id))
    # else if illegal move
    elif x.status_code == 400:
        # make board of original state
        # TODO Put some sort of error message to user here
        # render original board
        # return render(
        #     request,
        #     "board.html",
        #     {"board": board, "id": id, "state": current_state},
        # )
        return redirect(request.META["HTTP_REFERER"])


# adds a win to all profiles and goes back to home page
def win(request):
    # Profile.objects.all().update(wins=F("wins") + 1)
    Profile.objects.filter(user=request.user).update(wins=F("wins") + 1)
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
    context["player_id"] = request.user.id
    context["players"] = 2
    context["state"] = " a4c4e4g4g6  / h5  / e1 e9 / 10 10 / 1 "
    # horzontal walls / vertical walls / player pieces / available walls per player / active player

    return render(request, "second_player_debug.html", context)


# starts a new game
def debug(request):
    state = request.POST["state"]
    # create a new game model (with default state)
    p1 = Profile.objects.filter(user=request.user).first()

    game = Game(player1=p1, player2=p1)
    game.save()
    turn = game.get_player_turn(request.user.id)

    # adds both players (player1 being the current user)
    p2name = request.POST["player2"]
    p2user = User.objects.filter(username=p2name).first()
    p2 = Profile.objects.filter(user=p2user).first()

    return render(request, "debug.html", {"state": state, "turn": turn})


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
        playerid = str(Profile.objects.filter(user=request.user).first().id)
        turn = game.get_player_turn(playerid)
        # render new board
        return render(
            request,
            "board.html",
            {
                "board": "board",
                "id": id,
                "state": new_state,
                "turn": turn,
                "playerid": playerid,
            },
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
