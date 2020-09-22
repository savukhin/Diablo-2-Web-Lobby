from django.shortcuts import render, redirect
from character.forms import CharacterCreateForm
from character.models import Character
from authentication.models import CustomUser
from character.PvPGNCharacter import createPvPGNCharacter

# Create your views here.


def createCharacter(request):
    if (request.method == "POST"):
        characterForm = CharacterCreateForm(request.POST)
        if characterForm.is_valid():
            player = CustomUser.objects.get(user_id=request.user.id)
            createPvPGNCharacter(player.user.username, request.POST['name'], request.POST['characterClass'])
            newCharacter = characterForm.save(commit=False)
            newCharacter.player = player
            newCharacter.save()
            return redirect('/')

    return render(request, template_name='createCharacter.html')


def showCharacter(request, name):
    return render(request, template_name='character.html',
                  context={'character': Character.objects.get(name=name)})
