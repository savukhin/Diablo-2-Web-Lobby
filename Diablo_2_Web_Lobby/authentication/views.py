from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def signIn(request):
    if request.method == 'POST':
        print(request.POST)
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('/')
    return render(request, template_name='signIn.html')


def signUp(request):


    return render(request, template_name='signUp.html')


def signOut(request):
    logout(request)
    return redirect('/')


def profile(request):
    return render(request, template_name='profile.html')
