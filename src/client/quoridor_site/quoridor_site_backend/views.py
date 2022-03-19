from django.shortcuts import render
from django.http import HttpResponse
import requests, json


# Create your views here.

def home(request):
    return render(request, 'home.html')

def getName(request):
    return render(request, 'get_name.html')
    

def showName(request):
    name = request.POST['name']
    headers = requests.structures.CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    url = 'http://api:8080'
    data = {"name": name}
    x = requests.post(url, headers = headers,data = json.dumps(data))
    return HttpResponse(x)


def game_state(request):
    return render(request, 'game_state_demo.html')

def ascii_state(request):
    state = request.POST['state']
    url = 'http://api:8080/decode'
    headers = requests.structures.CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["charset"] = "UTF-8"
    data = {"state": state}
    x = requests.post(url, headers = headers,data = json.dumps(data))
    return render(request, "ascii.html", {"ascii" : x.text })