from django.shortcuts import render

# Create your views here.

def signIn(request):
    return render(request, template_name='signIn.html')


def signUp(request):
    return render(request, template_name='signUp.html')


def signOut(request):
    return render(request, template_name='signOut.html')


def profile(request):
    return render(request, template_name='profile.html')
