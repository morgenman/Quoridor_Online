from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.home),
    path('getName/', views.getName, name = 'getName'),
    path('showName/', views.showName, name = 'showName'),
    path('game_state/',views.game_state, name = 'game_state'),
    path('ascii_state/',views.ascii_state,name='ascii_state')
]
