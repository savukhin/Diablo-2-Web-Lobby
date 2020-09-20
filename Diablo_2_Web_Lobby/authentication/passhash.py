import ctypes

#Function that hashes password for PvPGN
def makeHash(password):
    test = ctypes.CDLL('authentication/bnpass.dll')
    test.pvpgn_hash.restype = ctypes.c_char_p
    test.pvpgn_hash.argtypes = [ctypes.POINTER(ctypes.c_char), ]
    return test.pvpgn_hash(password.encode('utf-8')).decode("utf-8")
