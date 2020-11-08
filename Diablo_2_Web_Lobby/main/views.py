from django.shortcuts import render
from Diablo_2_Web_Lobby.servers import servers, getStatus, getGameList, getGameInfoById

# Create your views here.


def serverInfo(request, server):
    class Game:
        def __init__(self):
            self.ID = -1
            self.GameName = "None"
            self.Users = -1
            self.Difficulty = "None"

    gamelist = getGameList(servers[server])
    gameInfos = []
    for game in gamelist:
        gameInfos.append(getGameInfoById(servers[server], game['ID']))
    return render(request, template_name='serverInfo.html', context={'server' : server, 'gamelist' : gameInfos})


def index(request):
    class Server:
        def __init__(self):
            self.maxCountOfGames = 0
            self.runningCountOfGames = 0
            self.maxCountOfUsers = 0
            self.runningCountOfUsers = 0

    context = {'serv' : {}}
    for server in servers.items():
        s = Server()
        status = getStatus(server[1])
        s.maxCountOfGames = status['maximumCountOfGames']
        s.runningCountOfGames = status['runningCountOfGames']
        #s.maxCountOfUsers = status['maximumCountOfUsers']
        s.runningCountOfUsers = status['runningCountOfUsers']
        context['serv'][server[1]] = s
        print(s.maxCountOfGames)
    return render(request, template_name='index.html',
                  context=context)