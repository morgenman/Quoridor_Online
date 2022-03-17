from django.shortcuts import render
from django.http import HttpResponse
import requests
from requests.structures import CaseInsensitiveDict


# Create your views here.

def home(request):
    return render(request, 'home.html')


def getUser(request):
    return render(request, 'get_user.html')


def getName(request):
    return render(request, 'get_name.html')
    

def showName(request):
    name = request.POST['name']
    # data_to_be_sent = "{'name': 'somevalue'}"
    # response = requests.post('http://api:8080', data = data_to_be_sent)
    # result = render(response, 'show_name.html', {'name': response.name}) 
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    url = 'http://api:8080'
    data = """
    {"name": "Cole"} 
    """
    x = requests.post(url, headers = headers,data = data)
    return x