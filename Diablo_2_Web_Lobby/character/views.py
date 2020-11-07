from django.shortcuts import render, redirect
from django.http import HttpResponse
from character.forms import CharacterCreateForm
from character.models import Character
from authentication.models import CustomUser
from Diablo_2_Web_Lobby.servers import servers
from character.PvPGNCharacter import createPvPGNCharacter
from authentication.models import PvpgnBnet
import urllib.request, json
import requests
# Create your views here.


def createChar(server, username, passhash, charname, characterClass):
    response = requests.post("http://" + server + "/createCharacter", data={'username': username,
                                                                     'passhash': passhash,
                                                                     'charname': charname,
                                                                     "characterClass": characterClass
                                                                     })
    mystr = response.text
    response.close()
    if mystr[0] == 'E':  # That means the word is Error (not a start of the json)
        return False
    elif mystr[0] == 'C':
        return "Character name is taken"

    return True

def createCharacter(request):
    #If 'submit' button pressed
    if (request.method == "POST"):
        characterForm = CharacterCreateForm(request.POST)
        if characterForm.is_valid(): #If all fields is correct
            '''
            player = CustomUser.objects.get(user_id=request.user.id)
            #Creating character on PvPGN server
            createPvPGNCharacter(player.user.username, request.POST['name'], request.POST['characterClass'])
            #There is a some code to set the player in character model
            newCharacter = characterForm.save(commit=False)
            newCharacter.player = player
            newCharacter.save()
            '''
            pvpgn_user = PvpgnBnet.objects.get(username=request.user.username)
            print(pvpgn_user.acct_passhash1)
            response = createChar(servers[request.path.split('/')[1]], pvpgn_user.username, pvpgn_user.acct_passhash1,
                                  request.POST['name'], request.POST['characterClass'])
            if (response == "Character name is taken"):
                return render(request, template_name='createCharacter.html', context={"error": "Character name is taken"})

            return redirect('/')
        return render(request, template_name='createCharacter.html', context={'form': characterForm})

    return render(request, template_name='createCharacter.html')


def getCharacter(server, name):
    fp = urllib.request.urlopen("http://" + server + "/getCharacter/" + name)
    mystr = (fp.read()).decode("utf-8")
    fp.close()
    if mystr[0] == 'E': #That means the word is Error (not a start of the json)
        return "ERROR"
    info = json.loads(mystr)
    return info


def showCharacter(request, name):
    character = getCharacter(servers[request.path.split('/')[1]], name)
    if (character == "ERROR"):
        return redirect(request.META.get('HTTP_REFERER'))

    return render(request, template_name='character.html',
                  context={'character': character,
                           'character_dumps': json.dumps(character)})
