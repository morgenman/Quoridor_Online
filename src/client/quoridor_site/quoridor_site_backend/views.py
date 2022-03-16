from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'home.html')


def getUser(request):
    html = "Click here to <a href=getName> Enter a Name </a>"
    return HttpResponse(html)


def getName(request):
    return render(request, 'get_name.html')
    

def showName(request):
    name = request.POST['name']
    return render(request, 'show_name.html', {'name': name})    