from django.shortcuts import render
from character.models import Character
from django.contrib.auth.models import User
from authentication.models import CustomUser
from lobby.D2GSConnetion import getGameList

# Create your views here.

#This is a prelobby where user choose character
def preLobby(request):
    thisUesr = CustomUser.objects.get(user_id=request.user.id)
    characters = Character.objects.filter(player_id=thisUesr.id)
    return render(request, template_name='preLobby.html',
                  context={'request': request, 'user': thisUesr, 'characters': characters})


#Return true, if this character belongs to this user
#IT IS NOT A VIEW!!!
def isCharacterCorrect(thisUser, character):
    if character == None:  # If character not found
        return False
    if character.player != thisUser:  # If character not belongs to this user
        return False
    return True


#This is a n0n-database object which describes a game to show in lobby
class Game:
    def __init__(self, title=None, password=None, difficulty="normal", users=0):
        self.title = title
        self.password = password
        self.difficulty = difficulty
        self.users = users


def lobby(request, name):
    #User must enter to the lobby with his character
    character = Character.objects.get(name=name)
    thisUser = CustomUser.objects.get(user_id=request.user.id)
    if isCharacterCorrect(thisUser, character) == False:  # If something wrong with this character
        #The we render the prelobby page
        return preLobby(request)


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

    return render(request, template_name='lobby.html', context={'character': character, 'games' : games})


#View to page with game creating (character has already been chosen)
def createGame(request, name):
    character = Character.objects.get(name=name)
    thisUser = CustomUser.objects.get(user_id=request.user.id)
    if isCharacterCorrect(thisUser, character) == False:  # If something wrong with this character
        return preLobby(request)

    return render(request, template_name='createGame.html', context={'character' : character})
