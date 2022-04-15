from . import bencoding
import os
import time
import hashlib


class Torrent:
    TorrentDict = {}
    encoding = ""
    PiceLen = 0

    def SizeOP(self, size):
        unit = "B"
        if size >= 4096:
            size = size / 1024
            unit = "KB"
        if size >= 4096:
            size = size / 1024
            unit = "MB"
        if size >= 4096:
            size = size / 1024
            unit = "GB"
        if size >= 4096:
            size = size / 1024
            unit = "TB"
        return str(round(size, 2)) + " " + unit

    def BytesToTextShow(self, Bytes):
        ReturnString = []
        Pos = 0
        for i in Bytes:
            ReturnString.append(hex((int(i / 16)))[-1:])
            ReturnString.append(hex((i % 16))[-1:])
            Pos += 2
        return "".join(ReturnString)

    def Load(self, filename):
        ResultDict = {}
        fsize = os.path.getsize(filename)
        fr = open(filename, "rb")
        fdata = fr.read(fsize)
        fr.close()
        self.TorrentDict = bencoding.decode(fdata)[0]
        # self.TorrentDict["info"]["pieces"] = b"\x00"*20
        # self.TorrentDict["info"]["files"] = b"\x00"*20
        # print(self.TorrentDict)
        # print(self.TorrentDict[])
        if "encoding" in self.TorrentDict:
            self.encoding = self.TorrentDict["encoding"].decode()
        else:
            self.encoding = "UTF-8"
        self.PiceLen = self.TorrentDict["info"]["piece length"]

    def CalcPiceLen(self, size):
        # 计算合适的块大小
        if size < 1024 ** 3:  # 1GB
            return 1024 ** 2  # 1MB
        elif size < 10 * 1024 ** 3:  # 10GB
            return 8 * 1024 ** 2  # 8MB
        elif size < 10 * 1024 ** 3:  # 100GB
            return 32 * 1024 ** 2  # 32MB
        else:  # 100GB or more
            return 64 * 1024 ** 2  # 64MB

    def Create(self, FilePath, TrackerServer, Private=False, source="", PiceLen=0):
        self.TorrentDict = {}
        self.encoding = "UTF-8"
        self.TorrentDict["announce"] = TrackerServer.encode(self.encoding)
        self.TorrentDict["created by"] = "QCTorrent/PY/0.0.1".encode(self.encoding)
        self.TorrentDict["creation date"] = int(time.time())
        self.TorrentDict["encoding"] = self.encoding.encode("ANSI")
        self.TorrentDict["info"] = {}
        if os.path.isfile(FilePath):  # 单文件
            fsize = os.path.getsize(FilePath)
            self.TorrentDict["info"]["length"] = fsize
            self.TorrentDict["info"]["name"] = os.path.basename(FilePath.encode(self.encoding))
            if PiceLen == 0:
                # print(self.CalcPiceLen(fsize))
                self.PiceLen = self.CalcPiceLen(fsize)
            else:
                self.PiceLen = PiceLen
            self.TorrentDict["info"]["piece length"] = self.PiceLen
            # pieces
            piecesArray = []
            fr = open(FilePath, "rb")
            while True:
                fdata = fr.read(self.PiceLen)
                if fdata == b"":
                    fr.close()
                    break
                piecesArray.append(hashlib.sha1(fdata).digest())
            self.TorrentDict["info"]["pieces"] = b"".join(piecesArray)
            piecesArray = []
            if Private:
                self.TorrentDict["info"]["private"] = 1
            self.TorrentDict["info"]["source"] = source.encode(self.encoding)
            # elif os.path.isdir(FilePath)
            pass

    def SetTrackerServer(self, TrackerServer):
        self.TorrentDict["announce"] = TrackerServer.encode(self.encoding)

    def GetFileName(self):
        return self.TorrentDict["info"]["name"].decode(self.encoding)

    def GetFileSize(self):
        return self.TorrentDict["info"]["length"]

    def Save(self, filename):
        TorrentData = bencoding.encode(self.TorrentDict)
        fw = open(filename, "wb")
        fw.write(TorrentData)
        fw.close()
        # print(TorrentData)

    def TorrentInfoInNormalText(self, ShowPiecesHASH=False):
        if self.TorrentDict == {}:
            return False
        ReturnArray = []
        ReturnArray.append("Tracker Server: " + self.TorrentDict["announce"].decode(self.encoding))  #
        # if "announce-list" in self.TorrentDict:
        #    ReturnArray.append("Backup Tracker Server: "+self.TorrentDict["announce-list"].decode(self.encoding))
        if "created by" in self.TorrentDict:
            ReturnArray.append("Created by: " + self.TorrentDict["created by"].decode(self.encoding))
        if "creation date" in self.TorrentDict:
            ReturnArray.append("Creation date: " + time.strftime("%Y-%m-%d %H:%M:%S",
                                                                 time.localtime(self.TorrentDict["creation date"])))
        if "comment" in self.TorrentDict:
            ReturnArray.append("Comment: " + self.TorrentDict["comment"].decode(self.encoding))
        ReturnArray.append("Info:")
        ReturnArray.append("    FileRootPath: " + self.TorrentDict["info"]["name"].decode(self.encoding))
        if "files" in self.TorrentDict["info"]:  # 多文件
            for i in self.TorrentDict["info"]["files"]:
                path = b""
                for i2 in i["path"]:
                    path += i2 + b"\\"
                ReturnArray.append("        FilePath:" + path[:-1].decode(self.encoding))
                ReturnArray.append("            FileSize:" + self.SizeOP(i["length"]))
            # print()
            pass
        else:
            ReturnArray.append("    FileName: " + self.TorrentDict["info"]["name"].decode(self.encoding))
            ReturnArray.append("    FileSize: " + self.SizeOP(self.TorrentDict["info"]["length"]))
        ReturnArray.append("    Piece length: " + self.SizeOP(self.PiceLen))
        ReturnArray.append("    Pieces count: " + str(int(len(self.TorrentDict["info"]["pieces"]) / 20)))
        if ShowPiecesHASH:
            for i in range(int(len(self.TorrentDict["info"]["pieces"]) / 20)):
                SHA1Value = self.BytesToTextShow(self.TorrentDict["info"]["pieces"][i * 20:(i + 1) * 20])
                print(SHA1Value)
        if "private" in self.TorrentDict["info"]:
            if self.TorrentDict["info"]["private"] == 1:
                ReturnArray.append("    Private: Yes")
            else:
                ReturnArray.append("    Private: No")
        else:
            ReturnArray.append("    Private: No")
        # ReturnArray.append()

        return "\r\n".join(ReturnArray)

    def Check(self, filename):
        if self.PiceLen == 0:
            return False
        if "files" in self.TorrentDict["info"]:  # 多文件
            fdata = b""
            pos = 0
            for i in self.TorrentDict["info"]["files"]:
                path = b""
                for i2 in i["path"]:
                    path += i2 + b"\\"

                # print(path[:-1].decode(self.encoding))
                fr = open(filename + "\\" + path[:-1].decode(self.encoding), "rb")
                while True:
                    # print(len(fdata),self.PiceLen-len(fdata))
                    fdata += fr.read(self.PiceLen - len(fdata))
                    # print(len(fdata))
                    # print(fdata[:5])
                    if len(fdata) != self.PiceLen:
                        fr.close()
                        break
                    #
                    if hashlib.sha1(fdata).digest() != self.TorrentDict["info"]["pieces"][pos * 20:(pos + 1) * 20]:
                        return False
                    fdata = b""
                    pos += 1
            if len(fdata) != 0:
                # print(self.BytesToTextShow(hashlib.sha1(fdata).digest()),self.BytesToTextShow(self.TorrentDict["info"]["pieces"][pos*20:(pos+1)*20]))
                if hashlib.sha1(fdata).digest() != self.TorrentDict["info"]["pieces"][pos * 20:(pos + 1) * 20]:
                    return False
            return True
        else:  # 单文件
            # 判断文件是否存在
            if not os.path.exists(filename):
                return False
            fr = open(filename, "rb")
            pos = 0
            while True:
                fdata = fr.read(self.PiceLen)
                if fdata == b"":
                    fr.close()
                    return True
                # print(hashlib.sha1(fdata).digest(),self.TorrentDict["info"]["pieces"][pos*20:(pos+1)*20])
                if hashlib.sha1(fdata).digest() != self.TorrentDict["info"]["pieces"][pos * 20:(pos + 1) * 20]:
                    return False
                pos += 1

    def GetInfoHash(self):
        data = bencoding.encode(self.TorrentDict["info"], "UTF-8")  #
        # data = b"info" + data
        data = data
        # print(data)
        return hashlib.sha1(data).hexdigest()
# print(torrent1.TorrentDict)
# torrent1.Write("2.torrent")
# print(torrent1.Check("2wwAT3uNA5gA.mp4"))

# torrent1.Load("3.torrent")
# printdata = torrent1.TorrentInfoInNormalText()
# print(printdata)
# print(torrent1.Check(torrent1.TorrentDict["info"]["name"].decode(torrent1.encoding)))

# torrent1 = torrent()
# torrent1.Create("test.txt","http://10.0.1.4:8000/tracker",True,"QcServer",2097152)
# torrent1.Create("test.txt","http://home.gtvps.com:8123/tracker",True,"QcServer",2097152)
# torrent1.Create("test.txt","http://10.0.1.4/announce.php",True,"QcServer",2097152)
# torrent1.Create("test.txt","http://20.194.20.47:8000/tracker",True,"QcServer",2097152)

# torrent1.Create(r"D:\Temp\Win11_EnglishInternational_x64v1.wim","http://10.0.1.123:8000/announce",True,"QcServer")

# print(torrent1.TorrentDict)
# printdata = torrent1.TorrentInfoInNormalText(True)
# torrent1.Load("3.torrent")
# print(torrent1.GetInfoHash())
# torrent1.Write("Win11_EnglishInternational_x64v1.torrent")
# print(printdata)

# FilePath,TrackerServer,Private=False,source="",PiceLen=0
# torrent1.Load("Win11_EnglishInternational_x64v1.torrent")
# printdata = torrent1.TorrentInfoInNormalText()
# print(printdata)
# fw = open("TorrInfo.txt","w")
# fw.write(printdata)

# print(torrent1.Check(torrent1.TorrentDict["info"]["name"].decode(torrent1.encoding)))
