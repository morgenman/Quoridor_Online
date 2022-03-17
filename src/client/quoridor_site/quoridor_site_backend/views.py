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
    data = {'name': name}
    response = requests.post('http://api:8080', data = json.dumps(data), headers = {'Content-Type': 'application/json'})
    result = render(response, 'show_name.html', {'name': response.name}) 
    return HttpResponse(result)