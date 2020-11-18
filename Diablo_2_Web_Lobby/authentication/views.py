from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from authentication.models import CustomUser, PvpgnBnet
from Diablo_2_Web_Lobby.servers import getCharacter, checkLogin, getUser
from authentication.forms import ChangeAvatarForm
from django.http import HttpResponseNotFound

import json
from django.contrib.auth.decorators import login_required

# Create your views here.

#It is not a view but a function for creation PvPGN profile
def createPvPGNProfile(name, password, email, isAdmin="false"):
    newProfile = PvpgnBnet.objects.createProfile(name, password, email, isAdmin)
    return newProfile


#View for Log in (sign in)
def signIn(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == 'POST': #If 'submit' button has been pressed then try to authenticate

        if checkLogin(request.POST['server'], request.POST['username'], request.POST['password']):
            django_username = request.POST['server'] + "_" + request.POST['username']
            user = authenticate(username=django_username, password=request.POST['password'])
            if user is not None: #If Django found a user then login
                login(request, user)
            else:
                from django.contrib.auth.forms import UserCreationForm
                formUser = UserCreationForm({"username": django_username, "password1": request.POST['password'],
                                      "password2": request.POST['password']})

                formUser.save()
                NewCustomUser = CustomUser(user=formUser.instance, username=request.POST['username'],
                                           server=request.POST['server'])
                NewCustomUser.save()
                user = authenticate(username=django_username, password=request.POST['password'])
                login(request, user)
            return redirect('/')

    return render(request, template_name='signIn.html')


#View for log out (sign out)
def signOut(request):
    logout(request)
    return redirect('/')


#View for profile displaying
def profile(request, server, username):
    class CharacterForm:
        def __init__(self):
            self.photo = ""
            self.name = ""
    try:
        customUser = CustomUser.objects.get(username=username)
    except:
        customUser = {'user': {'id': 0}, 'username': username, 'server': server,
                      'photo': {'url': "/media/Avatars/blankAvatar/blankAvatar.png"},
                      'notExists': True}
    try:
        characters = getUser(server, username)['characters']
    except:
        return HttpResponseNotFound("Not found " + username + " on server " + server)

    if (characters == None):
        characters = ['']
    characters_final = []
    for character in characters:
        try:
            q = getCharacter(server, character)
            q['header']['class']
            characters_final.append(CharacterForm())
            characters_final[-1].name = character
            characters_final[-1].photo = "img/CharacterIcons/" + q['header']['class'] + "Icon.png"
        except:
            pass

    if request.method == "POST":
        form = ChangeAvatarForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.cleaned_data.get("photo")
            customUser.photo = img
            customUser.save()
            return redirect('/profile/' + str(id))

    context = {'request': request,'profile': customUser, 'characters': characters_final, 'form': ChangeAvatarForm()}
    if request.user.is_authenticated:
        context["user"] = CustomUser.objects.get(user=request.user)

    return render(request, template_name='profile.html',
                  context=context)
