from django.shortcuts import render
from ladder.LadderParser import parseLadder
import urllib.request, json
from Diablo_2_Web_Lobby.servers import servers, getLadder
from character.models import Character
# Create your views here.


def ladderNorStandard(request):
    ladder = getLadder(servers[request.path.split('/')[1]], 'nor', 0)
    return render(request, template_name='ladder.html',
                  context={'ladder' : ladder,
                           'title' : 'Diablo 2 Standard Ladder'})


def ladderNorHardcore(request):
    ladder = getLadder(servers[request.path.split('/')[1]], 'nor', 1)
    return render(request, template_name='ladder.html',
                  context={'ladder' : ladder,
                           'title' : 'Diablo 2 HardCore Ladder'})


def ladderExpStandard(request):
    ladder = getLadder(servers[request.path.split('/')[1]], 'exp', 0)

    return render(request, template_name='ladder.html',
                  context={'ladder' : ladder,
                           'title' : 'Diablo 2 Lod Standard Ladder'})


def ladderExpHardcore(request):
    ladder = getLadder(servers[request.path.split('/')[1]], 'exp', 1)
    return render(request, template_name='ladder.html',
                  context={'ladder' : ladder,
                           'title' : 'Diablo 2 LoD HardCore Ladder'})