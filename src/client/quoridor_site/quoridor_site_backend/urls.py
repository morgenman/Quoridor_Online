from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path("", views.home),
    path("player/", views.ProfileListView.as_view(), name="player"),
    path("getName/", views.getName, name="getName"),
    path("showName/", views.showName, name="showName"),
    path("new_game", views.new_game, name="new_game"),
    path("make_move/", views.make_move, name="make_move"),
]
