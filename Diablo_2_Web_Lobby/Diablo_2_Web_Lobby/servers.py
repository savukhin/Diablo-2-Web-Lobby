import urllib.request, json
from authentication.passhash import makeHash
import requests
import os
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

servers = {"MyServer" : "127.0.0.1:6110"}

@csrf_exempt
def proceesInfo(request):
    if (request.method != "POST"):
        return HttpResponse("Wrong request method")

    server = request.POST["server"]
    try:
        os.mkdir(server)
    except:
        pass
    updateLadder(server, request.POST["ladder"])
    updateCharacters(server,request.POST["characters"])
    updateUsers(server, request.POST["users"])
    updateStatus(server, request.POST["status"])
    updateGamelist(server, request.POST["gamelist"])
    return HttpResponse("Nice cock\tawesome dick")


def updateGamelist(server, gamelist):
    f = open(server + "/gamelist", "w")
    f.write(gamelist)
    f.close()

def updateLadder(server, ladder):
    f = open(server + "/ladder", "w")
    f.write(ladder)
    f.close()

def updateCharacters(server, characters):
    f = open(server + "/characters", "w")
    f.write(characters)
    f.close()

def updateUsers(server, users):
    f = open(server + "/users", "w")
    f.write(users)
    f.close()

def updateStatus(server, status):
    f = open(server + "/status", "w")
    f.write(status)
    f.close()

#Authentication
def getUser(server, username):
    f = open(server + "/users", "r")
    mystr = f.read()
    f.close()
    users = json.loads(mystr)
    for user in users:
        if user['username'].lower() == username.lower():
            return user
    return "ERROR"


def checkLogin(server, username, password):
    f = open(server + "/users", "r")
    mystr = f.read()
    f.close()
    users = json.loads(mystr)
    passhash = makeHash(password)

    for user in users:
        if user['username'] == username:
            if user['passhash'] == passhash:
                return True
            return False

    return False


def register(server, username, password, email):
    return False


#Character
def createChar(server, username, passhash, charname, characterClass):
    return False


def getCharacter(server, name):
    f = open(server + "/characters", "r")
    mystr = f.read()
    f.close()
    characters = json.loads(mystr)
    for character in characters:
        if character['header']['name'].lower() == name.lower():
            return character
    return "ERROR"


def getCharactersFromUser(server, username):
    fp = urllib.request.urlopen(
        "http://" + server + "/getCharactersFromUser/" + username)
    mystr = (fp.read()).decode("utf-8")
    fp.close()
    if mystr[0] == 'E':  # That means the word is Error (not a start of the json)
        return "ERROR"
    return mystr.split("\n")[:-1]


#Ladder
def getLadder(server, diabloVersion, isHardcoreMode):
    f = open(server + "/ladder", "r")
    mystr = f.read()
    f.close()
    ladder = json.loads(mystr)

    if diabloVersion not in ladder.keys():
        return {}

    confirmedLadder = []
    for char in ladder[diabloVersion]:
        if char['hc'] == isHardcoreMode:
            confirmedLadder.append(char)
            # if Character.objects.filter(name=char['charname']):
            #    confirmedLadder.append(char)
    return confirmedLadder


#Status
def getStatus(server):
    f = open(server + "/status", "r")
    mystr = f.read()
    f.close()
    info = json.loads(mystr)
    return info

#Games
def getGameList(server):
    f = open(server + "/gamelist", "r")
    mystr = f.read()
    f.close()
    info = json.loads(mystr)
    return info


def getGameInfoById(server, id):
    f = open(server + "/gamelist", "r")
    mystr = f.read()
    f.close()
    gamelist = json.loads(mystr)

    for game in gamelist:
        if str(game['GameID']) == str(id):
            return game

    return "ERROR"


def getGameInfoFromCharacter(server, charname):
    f = open(server + "/gamelist", "r")
    mystr = f.read()
    f.close()
    if mystr == "null":
        return "ERROR"

    gamelist = json.loads(mystr)
    for game in gamelist:
        for user in game['Users']:
            if user['Charname'].lower() == charname.lower():
                return game

    return "ERROR"
