from django.shortcuts import render
from main.viewinterface import loadPlugin
from main.viewinterface import dec_loginrequired

@dec_loginrequired
def home(request):
    return render(request, 'index/home.html')


def about(request):
    return render(request, 'index/about.html', {'title': 'About'})
