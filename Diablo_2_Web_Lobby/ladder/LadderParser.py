from struct import unpack,calcsize
from os import stat


### Some struct from d2cs/d2dbs source
#
# ladder header (4 + 4 = 8):
#   bn_int maxtype
#   bn_int checksum
LD_HEAD="<2i"
szLD_HEAD = calcsize(LD_HEAD)

#
# ladder info (4 + 2 + 1 + 1 + 16 = 24):
#   bn_int experience
#   bn_short status
#   bn_byte level
#   bn_byte class;
#   char charname[16];
LD_INFO="<Ihbb16s"
szLD_INFO = calcsize(LD_INFO)

#
# ladder index (4 + 4 + 4 = 12):
#   bn_int type
#   bn_int offset
#   bn_int number
LD_INDEX="<3i"
szLD_INDEX = calcsize(LD_INDEX)

## Status flags
S_INIT = 0x1
S_EXP  = 0x20
S_HC   = 0x04
S_DEAD = 0x08


classes = {
    0x00 : ['Amazon', 'f'],
    0x01 : ['Sorceress', 'f'],
    0x02 : ['Necromancer', 'm'],
    0x03 : ['Paladin', 'm'],
    0x04 : ['Barbarian', 'm'],
    0x05 : ['Druid', 'm'],
    0x06 : ['Assassin', 'f']
    }


diff = {
    'nor': {
        0x1: { 0 : { 'm': 'Sir', 'f': 'Dame' },
               1 : { 'm': 'Count', 'f': 'Countess' }
               },
               
        0x2: { 0 : { 'm': 'Lord', 'f': 'Lady' },
               1 : { 'm': 'Duke', 'f': 'Duchess' }
               },
               
        0x3: { 0 : { 'm': 'Baron', 'f': 'Baroness' },
               1 : { 'm': 'King', 'f': 'Queen' }
               }
        },

    'exp': {
        0x1: { 0 : { 'm': 'Slayer', 'f': 'Slayer' },
               1 : { 'm': 'Destroyer', 'f': 'Destroyer' }
               },
               
        0x2: { 0 : { 'm': 'Champion', 'f': 'Champion' },
               1 : { 'm': 'Conqueror', 'f': 'Conqueror' }
               },
               
        0x3: { 0 : { 'm': 'Patriarch', 'f': 'Matriarch' },
               1 : { 'm': 'Guardian', 'f': 'Guardian' }
               }
        }
    }




def remove_null(text):
    return text.split(chr(0).encode('utf-8'))[0].decode('utf-8')


def get_ladder(file):
    try:
        size = stat(file)[6]
        data = open(file, "rb")
    except:
        print("Error opening " + file + "for read")
        exit()
    
    maxtype, checksum = unpack(LD_HEAD, data.read(szLD_HEAD))

    size = size - szLD_HEAD

    head = []

    for i in range(maxtype):
        type, offset, number = unpack(LD_INDEX, data.read(szLD_INDEX))
        size = size - szLD_INDEX
        head.append(
        {
        'type': type,
        'offset': offset,
        'number': number
        })
        

    ladder = {}
    ladder['nor'] = []
    ladder['exp'] = []

    temp = {}
    temp['nor'] = []
    temp['exp'] = []


    while size > 0:
        try:
            experience, status, level, _class, charname = unpack(LD_INFO, data.read(szLD_INFO))
        except:
            ### Bad data
            size = size - szLD_INFO
            continue
        
        size = size - szLD_INFO

        ## Avoid null chars
        if not experience:
            continue
        
        charname = remove_null(charname)
        died = 0

        if status & S_EXP:
            _type = 'exp'
            difficulty = ((status >> 0x08) & 0x0f) / 5
        else:
            _type = 'nor'
            difficulty = ((status >> 0x08) & 0x0f) / 5

        if status & S_HC:
            hc = 1
            if status & S_DEAD:
                died = 1
        else:
            hc = 0
        
        c_class = classes[_class]

        if difficulty and diff[_type].has_key(difficulty):
            prefix = diff[_type][difficulty][hc][c_class[1]]
        else:
            prefix = None
        
        char = (experience, {
            'charname'   : charname,
            'prefix'     : prefix,
            'experience' : experience,
            'class'      : c_class[0],
            'sex'        : c_class[0],
            'level'      : level,
            'type'       : _type,
            'difficulty' : difficulty,
            'hc'         : hc,
            'died'       : died
            })
        ## Dupe char? why?
        if char not in temp[_type]:
            temp[_type].append(char)
        
    data.close()

    ## Sorting by exp
    temp['nor'].sort()
    temp['nor'].reverse()
    temp['exp'].sort()
    temp['exp'].reverse()

    for _type in temp.keys():
        for ch in temp[_type]:
            ladder[_type].append(ch[1])
    del temp

    return ladder

def parseLadder():
    file = "D:/PvPGN/Magic_Builder/release/var/ladders/ladder.D2DV"
    ladder = get_ladder(file)
    return ladder
