from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from authentication.models import CustomUser, PvpgnBnet
from authentication.forms import FormReg
from django.contrib.auth.models import User
from Diablo_2_Web_Lobby.servers import servers
from character.models import Character
import urllib.request, json
import requests
from authentication.forms import ChangeAvatarForm
from authentication.passhash import makeHash

# Create your views here.

#It is not a view but a function for creation PvPGN profile
def createPvPGNProfile(name, password, email, isAdmin="false"):
    newProfile = PvpgnBnet.objects.createProfile(name, password, email, isAdmin)
    return newProfile


def checkLogin(server, username, password):
    response = requests.post("http://" + server + "/checkLogin", data={'username': username,
                                                                       "passhash": makeHash(password)})
    mystr = response.text
    response.close()
    if mystr[0] == 'E':  # That means the word is Error (not a start of the json)
        return False
    return True

def register(server, username, password, email):
    response = requests.post("http://" + server + "/register", data={'username': username,
                                                                     "passhash": makeHash(password),
                                                                     'email': email})
    mystr = response.text
    response.close()
    if mystr[0] == 'E':  # That means the word is Error (not a start of the json)
        return False
    elif mystr[0] == 'U':
        return "Username is taken"

    return True

#View for Log in (sign in)
def signIn(request):
    if request.method == 'POST': #If 'submit' button has been pressed then try to authenticate

        if checkLogin(servers[request.POST['server']], request.POST['username'], request.POST['password']):

            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None: #If Django found a user then login
                login(request, user)
                return redirect('/')

    return render(request, template_name='signIn.html')


#View for Registration
def signUp(request):
    if request.method == 'POST': #If 'submit' button has been pressed
        formUser = FormReg(request.POST)
        if formUser.is_valid(): #If input data is correct
            '''
            #Instance of PvPGN Profile
            newPvPGNProfile = createPvPGNProfile(request.POST['username'], request.POST['password1'],
                                                 request.POST['email'])
            #Instance of Django user
            formUser.save()
            #Instance of model which is contains relation between PvPGN profile and Django user
            NewCustomUser = CustomUser(user=formUser.instance, pvpgn_user=newPvPGNProfile)
            NewCustomUser.save()
            #And authentication
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, user)
            '''
            response = register(servers[request.POST['server']], request.POST['username'],
                     request.POST['password1'], request.POST['email'])
            if (response == "Username is taken"):
                print("Yoh!....")
                return render(request, template_name='signUp.html', context={"error": "Username is taken"})

            return redirect('/')
        print("Em....")
        return render(request, template_name='signUp.html', context={'form': formUser})

    return render(request, template_name='signUp.html')


#View for log out (sign out)
def signOut(request):
    logout(request)
    return redirect('/')


#View for profile displaying
def profile(request, id):
    djangoUser = User.objects.get(id=id)
    customUser = CustomUser.objects.get(user_id=djangoUser.id)
    #characters = Character.objects.filter(player_id=customUser.id)
    fp = urllib.request.urlopen("http://" + servers[request.path.split("/")[1]] + "/getCharactersFromUser/" + customUser.user.username)
    mystr = (fp.read()).decode("utf-8")
    fp.close()
    if mystr[0] == 'E':  # That means the word is Error (not a start of the json)
        return "ERROR"
    characters = mystr.split("\n")[:-1]
    print(characters)
    if request.method == "POST":
        form = ChangeAvatarForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.cleaned_data.get("photo")
            customUser.photo = img
            customUser.save()
            return redirect('/profile/' + str(id))

    return render(request, template_name='profile.html',
                  context={'request': request,'profile': customUser, 'characters': characters,
                           'form': ChangeAvatarForm()})
