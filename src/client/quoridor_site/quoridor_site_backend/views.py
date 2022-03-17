from django.shortcuts import render
from django.http import HttpResponse
import requests, json


# Create your views here.

def home(request):
    return render(request, 'home.html')


def getUser(request):
    return render(request, 'get_user.html')


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
