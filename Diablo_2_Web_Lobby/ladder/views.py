from django.shortcuts import render
from ladder.LadderParser import parseLadder
from character.models import Character
# Create your views here.


def processLadder(ladder, diabloVersion, hardcoreMode):
    confirmedLadder = []
    for char in ladder[diabloVersion]:
        if char['hc'] == hardcoreMode:
            confirmedLadder.append(char)
            #if Character.objects.filter(name=char['charname']):
            #    confirmedLadder.append(char)

    return confirmedLadder


def ladderNorStandard(request):
    ladder = [x for x in parseLadder()['nor'] if x['hc'] == 0]
    return render(request, template_name='ladder.html',
                  context={'ladder' : ladder,
                           'title' : 'Diablo 2 Standard Ladder'})


def ladderNorHardcore(request):
    ladder = [x for x in parseLadder()['nor'] if x['hc'] == 1]
    return render(request, template_name='ladder.html',
                  context={'ladder' : ladder,
                           'title' : 'Diablo 2 HardCore Ladder'})


def ladderExpStandard(request):
    ladder = processLadder(parseLadder(), 'exp', 0)

    return render(request, template_name='ladder.html',
                  context={'ladder' : ladder,
                           'title' : 'Diablo 2 Lod Standard Ladder'})


def ladderExpHardcore(request):
    ladder = [x for x in parseLadder()['exp'] if x['hc'] == 1]
    return render(request, template_name='ladder.html',
                  context={'ladder' : ladder,
                           'title' : 'Diablo 2 LoD HardCore Ladder'})