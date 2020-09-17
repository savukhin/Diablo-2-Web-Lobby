from django.shortcuts import render

# Create your views here.

def lobby(request):
    return render(request, template_name='lobby.html')


def createGame(request):
    return render(request, template_name='createGame.html')
