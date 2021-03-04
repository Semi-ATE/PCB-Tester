from django.shortcuts import render
from pcbtesterinterface.viewinterface import dec_loginrequired
from django.conf import settings

@dec_loginrequired
def home(request):
    content = getContent(settings.GITHUB_HOME_README)
    if not content:
        content = "Unable to load the github content"
    return render(request, 'index/home.html', {'title': 'Home', 'github': content})


def about(request):
    content = getContent(settings.GITHUB_PCBTESTER_README)
    if not content:
        content = "Unable to load the github content"
    return render(request, 'index/about.html', {'title': 'About', 'github': content})

def getContent(filepath: str):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return None
