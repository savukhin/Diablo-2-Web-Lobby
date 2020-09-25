from telnetlib import Telnet
import re


def getGameList():
    #Telnet on 192.168.1.14:8888
    tn = Telnet("192.168.1.14", 8888)
    #Read Welcome line
    tn.read_until(b"Password: ")
    #Enter password (don't look on abcd123, it is default D2GS password)
    tn.write("abcd123".encode("utf-8") + b"\n")
    #Read Succeed line
    tn.read_until(b"D2GS>")
    #Message with game list
    tn.write("gl".encode("ascii") + b"\n")
    #Just a line with all games
    answer = str(tn.read_until(b"D2GS>"))

    #There is an answer in table format

    #No game etc
    #| 1 name etc |
    #| 2 name2 etc |

    #So there is simple regex which find info about games (array of the each raw in table)
    games = re.findall(r'\|[^\|]*\|', answer)
    #Do array of splitted info in each raw (array of arrays which includes symbols '|' on the edges)
    games = [x.split() for x in games]
    #Get rid of symbols '|' from the right and left edges of array
    games = [x[1:-1] for x in games]

    #Closing telnet connection to avoid memory leak
    tn.close()
    return games
