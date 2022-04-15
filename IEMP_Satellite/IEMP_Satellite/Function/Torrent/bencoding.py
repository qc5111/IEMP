
def decode(source):
    # print(source[0])
    #判断为数组或字典
    if source[0] == 100:#d
        ResultDict = {}
        Array = False
        
    elif source[0] == 108:#l
        Array = True
        ResultDict = []

    pos = 1
    while True:
        if source[0] == 100:#d
            # 定位首个":"
            #title
            nextpos = pos
            while True:
                if source[nextpos+1] >= 0x30 and source[nextpos+1] <= 0x39: #数字0-9
                    nextpos+=1
                else:
                    break
            nextpos += 2
            datalen = int(source[pos:nextpos-1])
            pos = nextpos+datalen
            datatitle = source[nextpos:pos].decode()
            #data
        
        
        
        nextpos = pos
        while True:
            if source[nextpos] >= 0x30 and source[nextpos] <= 0x39: #数字0-9
                nextpos+=1
            else:
                break
        if nextpos == pos: #数据不为文本
            
            if source[nextpos:nextpos+1] == b"i":#整数
                pos = source.find(b"e",nextpos)
                if Array:
                    ResultDict.append(int(source[nextpos+1:pos]))
                else:
                    ResultDict[datatitle] = int(source[nextpos+1:pos])
                
                # print(datatitle,data)
                
                pos += 1
            elif source[nextpos:nextpos+1] == b"d":#字典
                if Array:
                    Result,pos = decode(source[nextpos:])
                    ResultDict.append(Result)
                else:
                    ResultDict[datatitle],pos = decode(source[nextpos:])
                pos+=nextpos+1
                # print("finish")
                
            elif source[nextpos:nextpos+1] == b"l":#数组
                if Array:
                    Result,pos = decode(source[nextpos:])
                    ResultDict.append(Result)
                else:
                    ResultDict[datatitle],pos = decode(source[nextpos:])
                pos+=nextpos+1
                pass
        else:#文本型
            nextpos += 1
            # print(source[pos-1:pos+3])
            datalen = int(source[pos:nextpos-1])
            pos = nextpos+datalen
            data = source[nextpos:pos]
            #print(datatitle,data)
            if Array:
                ResultDict.append(data)
            else:
                ResultDict[datatitle] = data
        if source[pos] == 101: #e
            return ResultDict,pos
def encode(DictData,encodeding=""):
    BencodingByteArray = []
    # print(type(DictData))
    if encodeding == "":
        encodeding = DictData["encoding"].decode()
    if type(DictData) == dict:
        BencodingByteArray.append(b"d")
        for key in DictData:
            BencodingByteArray.append(str(len(key)).encode(encodeding))
            BencodingByteArray.append(b":")
            BencodingByteArray.append(key.encode(encodeding))
            if type(DictData[key]) == bytes:
                BencodingByteArray.append(str(len(DictData[key])).encode(encodeding))
                BencodingByteArray.append(b":")
                BencodingByteArray.append(DictData[key])
            elif type(DictData[key]) == int:
                BencodingByteArray.append(b"i")
                BencodingByteArray.append(str(DictData[key]).encode(encodeding))
                BencodingByteArray.append(b"e")
            elif type(DictData[key]) == dict:
                #BencodingByteArray.append(b":")
                BencodingByteArray.append(encode(DictData[key],encodeding))
            elif type(DictData[key]) == list:
                BencodingByteArray.append(encode(DictData[key],encodeding))
        #BencodingByteArray.append(b"e")
        
    elif type(DictData) == list:
        BencodingByteArray.append(b"l")
        for i in DictData:
            if type(i) == bytes:
                BencodingByteArray.append(str(len(i)).encode(encodeding))
                BencodingByteArray.append(b":")
                BencodingByteArray.append(i)
            elif type(i) == int:
                BencodingByteArray.append(b"i")
                BencodingByteArray.append(str(i).encode(encodeding))
                BencodingByteArray.append(b"e")
            elif type(i) == dict:
                #BencodingByteArray.append(b":")
                BencodingByteArray.append(encode(i,encodeding))
            elif type(i) == list:
                BencodingByteArray.append(encode(i,encodeding))
    BencodingByteArray.append(b"e")
    return b"".join(BencodingByteArray)