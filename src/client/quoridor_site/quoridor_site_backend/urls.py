from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path("", views.home),
    path("user/", views.user, name="user"),
    path("getName/", views.getName, name="getName"),
    path("showName/", views.showName, name="showName"),
    path("game_state/", views.game_state, name="game_state"),
    path("game_board/", views.get_board, name="game_board"),
    path("new_game", views.new_game, name="new_game"),
    path("move/", views.make_move, name="move"),
]
