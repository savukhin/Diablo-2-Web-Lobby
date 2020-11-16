import ctypes
import urllib.request

#Function that hashes password for PvPGN
def makeHash(password):
    url = "https://pvpgn.pro/passhash/api.php?method=hash&password=" + password
    fp = urllib.request.urlopen(url)
    print((fp.read()).decode('utf-8'))
    return (fp.read()).decode('utf-8')
'''
    test = ctypes.CDLL('authentication/bnpass.dll')
    test.pvpgn_hash.restype = ctypes.c_char_p
    test.pvpgn_hash.argtypes = [ctypes.POINTER(ctypes.c_char), ]
    print(test.pvpgn_hash(password.encode('utf-8')).decode("utf-8"))
    return test.pvpgn_hash(password.encode('utf-8')).decode("utf-8")'''

