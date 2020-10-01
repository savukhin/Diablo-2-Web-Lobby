from django.shortcuts import render, redirect
from django.http import HttpResponse
from character.forms import CharacterCreateForm
from character.models import Character
from authentication.models import CustomUser
from django.http import HttpResponseRedirect
from character.PvPGNCharacter import createPvPGNCharacter
# Create your views here.


def createCharacter(request):
    #If 'submit' button pressed
    if (request.method == "POST"):
        characterForm = CharacterCreateForm(request.POST)
        if characterForm.is_valid(): #If all fields is correct
            player = CustomUser.objects.get(user_id=request.user.id)
            #Creating character on PvPGN server
            createPvPGNCharacter(player.user.username, request.POST['name'], request.POST['characterClass'])
            #There is a some code to set the player in character model
            newCharacter = characterForm.save(commit=False)
            newCharacter.player = player
            newCharacter.save()
            return redirect('/')
        return render(request, template_name='createCharacter.html', context={'form': characterForm})

    return render(request, template_name='createCharacter.html')


def getCharacter(name):
    import urllib.request, json
    fp = urllib.request.urlopen("http://127.0.0.1:8001/" + name)
    mystr = (fp.read()).decode("utf-8")
    fp.close()
    if mystr[0] == 'E': #That means the word is Error (not a start of the json)
        return "ERROR"
    info = json.loads(mystr)
    return info


def showCharacter(request, name):
    character = getCharacter(name)
    if (character == "ERROR"):
        return redirect(request.META.get('HTTP_REFERER'))
    return render(request, template_name='character.html',
                  context={'owner': Character.objects.get(name=name).player,
                           'character': character})
