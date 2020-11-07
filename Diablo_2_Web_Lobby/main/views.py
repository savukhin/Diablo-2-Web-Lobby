from django.shortcuts import render
from Diablo_2_Web_Lobby.servers import servers, getStatus

# Create your views here.

class Server:
    def __init__(self):
        self.maxCountOfGames = 0
        self.runningCountOfGames = 0
        self.maxCountOfUsers = 0
        self.runningCountOfUsers = 0




def index(request):
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