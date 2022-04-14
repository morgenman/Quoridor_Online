from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("player/", views.ProfileListView.as_view(), name="player"),
    path("games/", views.GameListView.as_view(), name="games"),
    path("getName/", views.getName, name="getName"),
    path("showName/", views.showName, name="showName"),
    path("second_player", views.second_player, name="second_player"),
    path("new_game", views.new_game, name="new_game"),
    path("make_move/", views.make_move, name="make_move"),
    path("win", views.win, name="win"),
    path("lose", views.lose, name="lose"),
    path("register", views.register, name="register"),
    path("js_test/", views.js_test, name="js_test"),
]
