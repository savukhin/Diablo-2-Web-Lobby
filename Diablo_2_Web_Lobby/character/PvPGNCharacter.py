import numpy as np
import os

#folder to PvPGN folder with files which contains info that is not in sql
VAR_FOLDER = "D:/PvPGN/Magic_Builder/release/var/"
CHARSAVE_FOLDER = VAR_FOLDER + "charsave"
CHARINFO_FOLDER = VAR_FOLDER + "charinfo"

characterClassCodes = {'Amazon' : 0,
                  "Sorceress" : 1,
                  "Necromancer" : 2,
                  "Paladin" : 3,
                  "Barbarian": 4,
                  "Druid" :5,
                  "Assassin" : 6}


def createCharInfo(player, name, characterClass):
    #Final folder for charinf   o file
    folder = CHARINFO_FOLDER + "/" + player

    # q - byte array from clear charinfo
    s = "charinfo_" + characterClass
    f = open("character/clear_char_files/" + s, "rb")
    q = f.read()
    f.close()

    w = []
    #Copying some bytes from q to w
    for i in range(0, 48):
        w.append(q[i])

    #Copy character name to w
    s = name.encode("utf-8")
    for i in range(0, 16):
        if i >= len(s):
            w.append(0)
        else:
            w.append(s[i])

    #Copy player name to bytearray w
    s = player.encode("utf-8")
    for i in range(0, 16):
        if i >= len(s):
            w.append(0)
        else:
            w.append(s[i])

    #Copying some bytes from q to w
    for i in range(80, len(q)):
        w.append(q[i])

    #Add info about character class
    w[188] = characterClassCodes[characterClass]


    try:
        os.mkdir(folder)
    except:
        pass
    f = open(folder + "/" + name, "wb")
    f.write(bytearray(w))
    f.close()


#Function that calculate special checksum for charsave file (this is Diablo 2 hacking protection)
#Python don't have int32 so I used numpy.int32
def d2charsave_checksum(filename, offset=12):
    def checksum(data, start_value=0):
        acc = np.int32(start_value)

        for value in data:
            acc = np.int32((acc << 1) + value + (acc < 0))

        return np.int32(acc)

    data = np.fromfile(filename, dtype=np.uint8)

    checksum_byte_length = np.dtype("int32").itemsize

    pre_data, post_data = data[:offset], data[offset + checksum_byte_length:]

    pre_checksum = checksum(
        pre_data,
        start_value=0
    )

    on_checksum = checksum(
        np.zeros(checksum_byte_length, dtype=np.uint8),
        start_value=pre_checksum
    )

    post_checksum = checksum(
        post_data,
        start_value=on_checksum
    )

    return post_checksum


#Function to create charsave file
def createCharSave(name, characterClass):
    #q - byte array from clear charsave
    s = "charsave_" + characterClass
    f = open("character/clear_char_files/" + s, "rb")
    q = f.read()
    f.close()

    #w - byte array for new charsave
    w = []

    #Copying some bytes from q to w
    for i in range(0, 12):
        w.append(q[i])

    #Some bytes with checksum. Must be 0 to calculate checksum
    for i in range(12, 16):
        w.append(0)

    #Copying some bytes from q to w
    for i in range(16, 20):
        w.append(q[i])

    #Copy name to bytearray w
    s = name.encode("utf-8")
    for i in range(0, 16):
        if i >= len(s):
            w.append(0)
        else:
            w.append(s[i])

    #Copying some bytes from q to w
    for i in range(36, 40):
        w.append(q[i])

    #Add info about character class
    w.append(characterClassCodes[characterClass])

    #Copying some bytes from q to w
    for i in range(41, len(q)):
        w.append(q[i])

    f = open(CHARSAVE_FOLDER + "/" + name, "wb")
    f.write(bytearray(w))
    f.close()

    check = d2charsave_checksum(CHARSAVE_FOLDER + "/" + name)
    temp = int(check).to_bytes(4, "little", signed=True)
    for i in range(12, 16):
        w[i] = temp[i - 12]

    f = open(CHARSAVE_FOLDER + "/" + name, "wb")
    f.write(bytearray(w))
    f.close()


def createPvPGNCharacter(player, name, characterClass):
    createCharSave(name, characterClass)
    createCharInfo(player, name, characterClass)
