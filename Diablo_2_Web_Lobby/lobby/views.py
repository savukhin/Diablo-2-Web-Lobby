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


#This is a lobby where use choose game (character has already been chosen)
def lobby(request, name):
    character = Character.objects.get(name=name)
    thisUser = CustomUser.objects.get(user_id=request.user.id)
    if character == None: #If character not found
        return prelobby(request)
    if character.player != thisUser: #If character not belongs to this user
        return prelobby(request)

    return render(request, template_name='lobby.html', context={'character' : character})


#View to page with game creating
def createGame(request):
    return render(request, template_name='createGame.html')
