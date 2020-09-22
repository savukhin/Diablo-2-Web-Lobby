from telnetlib import Telnet


def getGameList():
    #Telnet on 192.168.1.14:8888
    tn = Telnet("192.168.1.14", 8888)
    #Read Welcome line
    tn.read_very_eager()
    #Enter password (don't look on abcd123, it is default D2GS password)
    tn.write("abcd123".encode("utf-8") + b"\n")
    #Read Succeed line
    tn.read_very_eager()
    #Message with game list
    tn.write("gl".encode("ascii") + b"\n")
    #Just a line with all games
    tn.read_very_eager()
    tn.close()
