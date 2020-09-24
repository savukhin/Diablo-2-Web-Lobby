from django.shortcuts import render
from character.models import Character
from django.contrib.auth.models import User
from authentication.models import CustomUser

# Create your views here.

#This is a prelobby where user choose character
def prelobby(request):
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


#This is a lobby where use choose game (character has already been chosen)
def lobby(request, name):
    character = Character.objects.get(name=name)
    thisUser = CustomUser.objects.get(user_id=request.user.id)
    if isCharacterCorrect(thisUser, character) == False: #If something wrong with this character
        return prelobby(request)

    return render(request, template_name='lobby.html', context={'character' : character})


#View to page with game creating (character has already been chosen)
def createGame(request, name):
    character = Character.objects.get(name=name)
    thisUser = CustomUser.objects.get(user_id=request.user.id)
    if isCharacterCorrect(thisUser, character) == False:  # If something wrong with this character
        return prelobby(request)

    return render(request, template_name='createGame.html', context={'character' : character})
