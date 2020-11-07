from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from authentication.models import CustomUser, PvpgnBnet
from authentication.forms import FormReg
from django.contrib.auth.models import User
from Diablo_2_Web_Lobby.servers import servers, getCharacter, checkLogin, register, getCharactersFromUser
from authentication.forms import ChangeAvatarForm

# Create your views here.

#It is not a view but a function for creation PvPGN profile
def createPvPGNProfile(name, password, email, isAdmin="false"):
    newProfile = PvpgnBnet.objects.createProfile(name, password, email, isAdmin)
    return newProfile


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
    class CharacterForm:
        def __init__(self):
            self.photo = ""
            self.name = ""
    djangoUser = User.objects.get(id=id)
    customUser = CustomUser.objects.get(user_id=djangoUser.id)
    #characters = Character.objects.filter(player_id=customUser.id)

    characters = getCharactersFromUser(servers[request.path.split("/")[1]], customUser.user.username)
    characters_final = []
    for character in characters:
        try:
            q = getCharacter(servers[request.path.split("/")[1]], character)
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

    return render(request, template_name='profile.html',
                  context={'request': request,'profile': customUser, 'characters': characters_final,
                           'form': ChangeAvatarForm()})
