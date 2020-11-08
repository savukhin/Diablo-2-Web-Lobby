import urllib.request, json
from authentication.passhash import makeHash
import requests

servers = {"MyServer" : "127.0.0.1:6110",
           "" : "127.0.0.1:6110"}

#Authentication
def checkLogin(server, username, password):
    response = requests.post("http://" + server + "/checkLogin", data={'username': username,
                                                                       "passhash": makeHash(password)})
    mystr = response.text
    response.close()
    if mystr[0] == 'E':  # That means the word is Error (not a start of the json)
        return False
    return True


def register(server, username, password, email):
    response = requests.post("http://" + server + "/register", data={'username': username,
                                                                     "passhash": makeHash(password),
                                                                     'email': email})
    mystr = response.text
    response.close()
    if mystr[0] == 'E':  # That means the word is Error (not a start of the json)
        return False
    elif mystr[0] == 'U':
        return "Username is taken"

    return True


#Character
def createChar(server, username, passhash, charname, characterClass):
    response = requests.post("http://" + server + "/createCharacter", data={'username': username,
                                                                     'passhash': passhash,
                                                                     'charname': charname,
                                                                     "characterClass": characterClass
                                                                     })
    mystr = response.text
    response.close()
    if mystr[0] == 'E':  # That means the word is Error (not a start of the json)
        return False
    elif mystr[0] == 'C':
        return "Character name is taken"

    return True


def getCharacter(server, name):
    fp = urllib.request.urlopen("http://" + server + "/getCharacter/" + name)
    mystr = (fp.read()).decode("utf-8")
    fp.close()
    if mystr[0] == 'E': #That means the word is Error (not a start of the json)
        return "ERROR"
    info = json.loads(mystr)
    return info


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
        if char['hc'] == isHardcoreMode:
            confirmedLadder.append(char)
            #if Character.objects.filter(name=char['charname']):
            #    confirmedLadder.append(char)
    return confirmedLadder


#Status
def getStatus(server):
    fp = urllib.request.urlopen("http://" + server + "/getStatus/")
    mystr = (fp.read()).decode("utf-8")
    fp.close()
    if mystr[0] == 'E':  # That means the word is Error (not a start of the json)
        return "ERROR"
    info = json.loads(mystr)
    return info

#Games
def getGameList(server):
    fp = urllib.request.urlopen("http://" + server + "/getGamelist/")
    mystr = (fp.read()).decode("utf-8")
    fp.close()
    if mystr[0] == 'E':  # That means the word is Error (not a start of the json)
        return "ERROR"
    info = json.loads(mystr)
    return info


def getGameInfoById(server, id):
    fp = urllib.request.urlopen("http://" + server + "/getGameInfoById/" + id)
    mystr = (fp.read()).decode("utf-8")
    fp.close()
    if mystr[0] == 'E':  # That means the word is Error (not a start of the json)
        return "ERROR"
    info = json.loads(mystr)
    return info


def getGameInfoFromCharacter(server, charname):
    fp = urllib.request.urlopen("http://" + server + "/getGameInfoFromCharacter/" + charname)
    mystr = (fp.read()).decode("utf-8")
    fp.close()
    if mystr[0] == 'E':  # That means the word is Error (not a start of the json)
        return "ERROR"
    info = json.loads(mystr)
    return info