from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('getUser', views.getUser, name = 'getUser'),
    path('getName', views.getName),
    path('showName', views.showName),
]
