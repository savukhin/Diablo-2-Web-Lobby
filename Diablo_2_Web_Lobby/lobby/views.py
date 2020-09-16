from django.shortcuts import render

# Create your views here.

def lobby(request):
    return render(request, template_name='lobby.html')