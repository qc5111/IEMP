def Bytes2HexString(Data):
    HexString = []
    for i in Data:
        HexString.append(hex(i)[2:].zfill(2))
    return "".join(HexString)


def HexString2Bytes(Data):
    return bytes.fromhex(Data)


#print(Bytes2HexString(b"0123456789abcdef"))
#print(HexString2Bytes(("30313233343536373839616263646566")))
