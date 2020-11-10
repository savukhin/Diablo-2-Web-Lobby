from django.shortcuts import render
from Diablo_2_Web_Lobby.servers import servers, getStatus, getGameList
from authentication.models import CustomUser

# Create your views here.


def serverInfo(request, server):
    class Game:
        def __init__(self):
            self.ID = -1
            self.GameName = "None"
            self.Users = -1
            self.Difficulty = "None"

    gamelist = getGameList(server)
    context = {'server' : server, 'gamelist' : gamelist}
    if request.user.is_authenticated:
        context["user"] = CustomUser.objects.get(user=request.user)
    return render(request, template_name='serverInfo.html', context=context)


def index(request):
    class Server:
        def __init__(self):
            self.maxCountOfGames = 0
            self.runningCountOfGames = 0
            self.maxCountOfUsers = 0
            self.runningCountOfUsers = 0

    context = {'serv' : {}}
    for server in servers.keys():
        s = Server()
        status = getStatus(server)
        s.maxCountOfGames = status['maximumCountOfGames']
        s.runningCountOfGames = status['runningCountOfGames']
        #s.maxCountOfUsers = status['maximumCountOfUsers']
        s.runningCountOfUsers = status['runningCountOfUsers']
        context['serv'][server[1]] = s

    if request.user.is_authenticated:
        context["user"] = CustomUser.objects.get(user=request.user)
    return render(request, template_name='index.html',
                  context=context)