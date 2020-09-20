from django.shortcuts import render, redirect
from character.forms import CharacterCreateForm
from character.models import Character
from authentication.models import CustomUser

# Create your views here.

#folder to PvPGN folder with files which contains info that is not in sql
VAR_FOLDER = "D:/PvPGN/Magic_Builder/release/var"


def createCharacter(request):
    if (request.method == "POST"):
        characterForm = CharacterCreateForm(request.POST)
        if characterForm.is_valid():
            player = CustomUser.objects.get(user_id=request.user.id)
            newCharacter = characterForm.save(commit=False)
            newCharacter.player = player
            newCharacter.save()
            return redirect('/')

    return render(request, template_name='createCharacter.html')

