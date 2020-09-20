from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from authentication.models import CustomUser, PvpgnBnet
from authentication.forms import FormReg
from authentication.passhash import makeHash

# Create your views here.

#It is not a view but a function for creation PvPGN profile
def createPvPGNProfile(name, password, email, isAdmin="false"):
    newProfile = PvpgnBnet.objects.createProfile(name, password, email, isAdmin)
    return newProfile


#View for Log in (sign in)
def signIn(request):
    if request.method == 'POST': #If 'submit' button has been pressed then try to authenticate
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
            return redirect('/')
        return render(request, template_name='signUp.html', context={'form': formUser})

    return render(request, template_name='signUp.html')


#View for log out (sign out)
def signOut(request):
    logout(request)
    return redirect('/')

#View for profile displaying
def profile(request):
    return render(request, template_name='profile.html')
