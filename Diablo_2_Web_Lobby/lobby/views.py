from django.shortcuts import render
from lobby.D2GSConnetion import getGameList

# Create your views here.

#This is a n0n-database object which describes a game to show in lobby
class Game:
    def __init__(self, title=None, password=None, difficulty="normal", users=0):
        self.title = title
        self.password = password
        self.difficulty = difficulty
        self.users = users


def lobby(request):
    #To see game list in terminal. There is array of splitted information about each game (array of arrays)
    rawGameList = getGameList()
    #There is something in format [['001', 'Www', '1', 'exp', 'sc', 'normal', 'ladder', '1', '10:42:35', 'N']]

    games = []
    for x in rawGameList:
        title = x[1]
        password = None
        users = 0
        difficulty = "normal"
        if len(x) == 10: #That means game doesn't have a password field.
            password = None
            users = x[7]
            difficulty = x[5]
        else:
            password = x[2]
            users = x[8]
            difficulty = x[6]

        #Adding information about this game in list
        games.append(Game(title, password, difficulty, users))

    return render(request, template_name='lobby.html', context={'games' : games})


def createGame(request):
    return render(request, template_name='createGame.html')
