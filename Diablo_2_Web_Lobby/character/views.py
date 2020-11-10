from django.shortcuts import render, redirect
from django.http import HttpResponse
from character.forms import CharacterCreateForm
from character.models import Character
from authentication.models import CustomUser
from Diablo_2_Web_Lobby.servers import getCharacter, getGameInfoFromCharacter
import urllib.request, json
# Create your views here.



def showCharacter(request, name, server):
    character = getCharacter(server, name)
    if (character == "ERROR"):
        #return redirect(request.META.get('HTTP_REFERER'))
        return redirect("/")

    game = getGameInfoFromCharacter(server, name)

    context = {'character': character, 'character_dumps': json.dumps(character), 'game': game}
    if request.user.is_authenticated:
            context["user"] = CustomUser.objects.get(user=request.user)

    return render(request, template_name='character.html',
                  context=context)
