from django.shortcuts import render
from ladder.LadderParser import parseLadder
import urllib.request, json
from Diablo_2_Web_Lobby.servers import servers
from character.models import Character
# Create your views here.


def getLadder(server, diabloVersion, hardcoreMode):
    fp = urllib.request.urlopen("http://" + server + "/getLadder")
    mystr = (fp.read()).decode("utf-8")
    fp.close()
    if mystr[0] == 'E':  # That means the word is Error (not a start of the json)
        return "ERROR"
    ladder = json.loads(mystr)

    if diabloVersion not in ladder.keys():
        return {}

    confirmedLadder = []
    for char in ladder[diabloVersion]:
        if char['hc'] == hardcoreMode:
            confirmedLadder.append(char)
            #if Character.objects.filter(name=char['charname']):
            #    confirmedLadder.append(char)
    return confirmedLadder


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