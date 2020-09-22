from django.shortcuts import render
from lobby.D2GSConnetion import getGameList

# Create your views here.

def lobby(request):
    #To see game list in terminal
    print("____GAME LIST_____________", getGameList(), "____GAME LIST________--")
    return render(request, template_name='lobby.html')


def createGame(request):
    return render(request, template_name='createGame.html')
