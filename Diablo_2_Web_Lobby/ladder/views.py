from django.shortcuts import render, redirect
from Diablo_2_Web_Lobby.servers import getLadder
from authentication.models import CustomUser
from character.models import Character
# Create your views here.


def ladder(request):
    return redirect("/")


def ladderNorStandard(request, server):
    ladder = getLadder(server, 'nor', 0)
    context = {'ladder': ladder, 'title': 'Diablo 2 Standard Ladder', 'server': server}
    if request.user.is_authenticated:
        context["user"] = CustomUser.objects.get(user=request.user)
    return render(request, template_name='ladder.html',
                  context=context)


def ladderNorHardcore(request, server):
    ladder = getLadder(server, 'nor', 1)
    context = {'ladder': ladder, 'title': 'Diablo 2 Standard Ladder', 'server': server}
    if request.user.is_authenticated:
        context["user"] = CustomUser.objects.get(user=request.user)
    return render(request, template_name='ladder.html',
                  context=context)


def ladderExpStandard(request, server="MyServer"):
    ladder = getLadder(server, 'exp', 0)

    context = {'ladder': ladder, 'title': 'Diablo 2 Standard Ladder', 'server': server}
    if request.user.is_authenticated:
        context["user"] = CustomUser.objects.get(user=request.user)
    return render(request, template_name='ladder.html',
                  context=context)


def ladderExpHardcore(request, server):
    ladder = getLadder(server, 'exp', 1)
    context = {'ladder': ladder, 'title': 'Diablo 2 Standard Ladder', 'server': server}
    if request.user.is_authenticated:
        context["user"] = CustomUser.objects.get(user=request.user)
    return render(request, template_name='ladder.html',
                  context=context)