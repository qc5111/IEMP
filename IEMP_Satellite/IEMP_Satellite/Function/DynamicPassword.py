import hashlib
import datetime
import time
import struct

def DynamicPassword(encrypt,codelen):
    i2 = 0
    code = [0] * codelen
    timestap = int(time.mktime(datetime.datetime.utcnow().timetuple())/30)
    MD5Encrypted = hashlib.md5(encrypt+struct.pack('<I', timestap)).digest()
    #MD5Encrypted = list(MD5Encrypted)
    #print(MD5Encrypted)
    #print_hex(MD5Encrypted)
    for i in range(16):
        code[i2] = (code[i2]+MD5Encrypted[i])%256
        #print(code,MD5Encrypted[i])
        i2 += 1
        if i2==codelen:
            i2=0
    #print(code)
    #code[7]+=1 Error code test
    code = bytes(code)
    return code
