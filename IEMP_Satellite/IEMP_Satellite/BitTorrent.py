import _thread
import json
import os
import time

from django.http import HttpResponse, StreamingHttpResponse
from . import bencoding
import MainDB.models as DB
from django.shortcuts import render
from pyaria2 import Aria2RPC

from .Function.Torrent.torrent import Torrent
from .settings import MLang, ServerAddr


def get_middle_text(text, start, end, start_pos=0):
    # text=str(text)
    # print(start)
    # print(start_pos)
    head = text.find(start, start_pos)
    if head == -1:
        return "", 0
    final = text.find(end, head + len(start))
    return_text = text[head + len(start):final]
    return return_text, final + len(end)


def CheckTorrentThread(info_hash):
    TorrentInfo = DB.TorrentList.objects.get(info_hash=info_hash)
    FileStoragePath = DB.SateliteInfo.objects.get(Name="FileStoragePath")
    TorrentFile = Torrent()
    TorrentFile.Load(FileStoragePath.Value + "/Torrents/" + TorrentInfo.info_hash + ".torrent")
    if TorrentFile.Check(FileStoragePath.Value + "/" + TorrentInfo.FileName):  # 文件完整
        TorrentInfo.Status = 1
    else:
        TorrentInfo.Status = 2
    TorrentInfo.save()
    pass


def URLCode2BytesString(URLCode):
    pos = 0
    ReturnArray = []
    while True:
        if pos >= len(URLCode):
            break
        if URLCode[pos] == "%":
            ReturnArray.append(URLCode[pos + 1:pos + 3])
            pos += 3
        else:
            NowText = hex(ord(URLCode[pos]))[2:]
            # print(hex(ord(URLCode[pos])), NowText)
            if len(NowText) == 1:
                NowText = "0" + NowText
            ReturnArray.append(NowText)
            pos += 1
    return "".join(ReturnArray).lower()


def IPPort2Str(IP, Port):
    Port = int(Port)
    IPSplited = IP.split(".")
    IPSplited.append(int(Port / 256))
    IPSplited.append(Port % 256)
    ReturnData = []
    for i in IPSplited:
        HexData = hex(int(i))[2:]
        if len(HexData) == 1:
            HexData = "0" + HexData
        ReturnData.append(HexData)

    return "".join(ReturnData)


def ReadFile(file_name, chunk_size=16384):
    with open(file_name, "rb") as Fr:
        while True:
            Data = Fr.read(chunk_size)
            if Data:
                yield Data
            else:
                break


def CreateDownload(IP, info_hash):
    jsonrpc = Aria2RPC("http://%s:48290/rpc" % IP)
    FileStoragePath = DB.SateliteInfo.objects.get(Name="FileStoragePath")
    Fr = open(FileStoragePath.Value + "/Torrents/" + info_hash + ".torrent", "rb")
    TorrentRawData = Fr.read()
    Fr.close()
    DownloadID = jsonrpc.addTorrent(TorrentRawData)
    return DownloadID


def CheckExpiredPeer():
    # 检查过期的peer
    DB.TorrentRunningList.objects.filter(LastUpdateTime__lt=int(time.time()) - 300).delete()


def GetInfoHashFromFileName(FileName):
    try:
        return DB.TorrentList.objects.get(FileName=FileName).info_hash
    except:
        return ""


def Tracker(request):
    ReturnValue = {}
    SourceDict = {}
    SourceDict = request.GET.dict()
    CheckExpiredPeer()
    if "info_hash" not in SourceDict:
        return HttpResponse("Error")
    SourceDict["info_hash"] = URLCode2BytesString(get_middle_text(request.get_full_path(), "info_hash=", "&")[0])
    SourceDict["peer_id"] = URLCode2BytesString(get_middle_text(request.get_full_path(), "peer_id=", "&")[0])
    if "key" in SourceDict:
        SourceDict["key"] = URLCode2BytesString(get_middle_text(request.get_full_path(), "key=", "&")[0])
    else:
        SourceDict["key"] = b""
    SourceDict["IP"] = request.META.get('REMOTE_ADDR')

    if "event" in SourceDict:
        if SourceDict["event"] == "started":
            SourceDict["Status"] = 1
        elif SourceDict["event"] == "completed":  # seeding
            print("completed")
            print(SourceDict["IP"])
            SourceDict["Status"] = 2
        else:
            SourceDict["Status"] = 0
    else:
        SourceDict["Status"] = -1  # 状态不变
    SourceDict["IPAndPort"] = IPPort2Str(SourceDict["IP"], SourceDict["port"])
    DBresult = DB.TrackerClientList.objects.filter(peer_id=SourceDict["peer_id"])


    """
    # 判断并注册服务器
    
    if not DBresult:
        DBresult = DB.TrackerClientList.objects.filter(key=SourceDict["key"])
        if not DBresult:
            DBresult = DB.TrackerClientList(
                peer_id=SourceDict["peer_id"],
                IPAndPort=SourceDict["IPAndPort"],
                key=SourceDict["key"],
            )
            DBresult.save()
        else:
            DBresult.update(
                peer_id=SourceDict["peer_id"],
                IPAndPort=SourceDict["IPAndPort"],
            )
            DBresult = DBresult[0]

    else:
        DBresult = DBresult[0]
    """
    # 判断并注册种子
    # print(SourceDict["left"])

    #
    if SourceDict["Status"] == 1:
        if SourceDict["left"] == "0":
            SourceDict["Status"] = 2
        DB.TorrentRunningList(
            info_hash=SourceDict["info_hash"],
            peer_id=SourceDict["peer_id"],
            IPAndPort=SourceDict["IPAndPort"],
            left=int(SourceDict["left"]),
            Status=SourceDict["Status"],  # 0:stopped, 1:downloading, 2:seeding
            LastUpdateTime=int(time.time())
        ).save()
    elif SourceDict["Status"] == -1 or SourceDict["Status"] == 2:
        DBresult = DB.TorrentRunningList.objects.filter(info_hash=SourceDict["info_hash"],
                                                        peer_id=SourceDict["peer_id"])
        if SourceDict["Status"] == -1:
            SourceDict["Status"] = DBresult[0].Status
        DBresult.update(
            IPAndPort=SourceDict["IPAndPort"],
            left=int(SourceDict["left"]),
            Status=SourceDict["Status"],  # 0:stopped, 1:downloading, 2:seeding
            LastUpdateTime=int(time.time())
        )
    elif SourceDict["Status"] == 0:
        DB.TorrentRunningList.objects.filter(info_hash=SourceDict["info_hash"], peer_id=SourceDict["peer_id"]).delete()

    # 回复

    ReturnValue["interval"] = 240  # 最大汇报时间，由于是内网服务器，调小一点
    ReturnValue["min interval"] = 30  # 最小汇报时间，由于是内网服务器，调小一点

    # ReturnValue["complete"] = DB.TorrentRunningList.objects.filter(info_hash=SourceDict["info_hash"],
    #                                                               left=0).count()  # 下载完成人数，应从数据库查询
    # ReturnValue["incomplete"] = DB.TorrentRunningList.objects.filter(info_hash=SourceDict["info_hash"],
    #                                                                 Status=1).count()  # 未下载完成人数，应从数据库查询
    DBpeers = DB.TorrentRunningList.objects.values("IPAndPort").filter(info_hash=SourceDict["info_hash"])
    peers = []
    for i in DBpeers:
        if i["IPAndPort"] != SourceDict["IPAndPort"]:
            peers.append(i["IPAndPort"])
    # print(peers)
    ReturnValue["peers"] = bytes.fromhex("".join(peers))  # 对端简写，应从数据库查询 10.0.1.123:8012
    # print(bencoding.encode(ReturnValue, "ASCII"))
    return HttpResponse(bencoding.encode(ReturnValue, "ASCII"))


def AddTorrent(request):
    # 文件上传
    FileStoragePath = DB.SateliteInfo.objects.get(Name="FileStoragePath")
    TorrentPath = FileStoragePath.Value + "/Torrents/" + request.FILES["file"].name
    Fw = open(TorrentPath, "wb")
    for chunk in request.FILES["file"].chunks():
        Fw.write(chunk)
    Fw.close()
    # 读取torrent文件
    TorrentFile = Torrent()
    TorrentFile.Load(TorrentPath)
    # 重定义Tracker服务器地址
    TorrentFile.SetTrackerServer(ServerAddr + "Tracker")
    info_hash = TorrentFile.GetInfoHash()
    TorrentFile.Save(FileStoragePath.Value + "/Torrents/" + info_hash + ".torrent")
    os.remove(TorrentPath)
    # 添加到数据库
    DB.TorrentList(info_hash=info_hash,
                   FileName=TorrentFile.GetFileName(), FileSize=TorrentFile.GetFileSize(), Status=4,
                   UpdateTime=int(time.time())).save()
    # 多线程启动检查线程
    _thread.start_new_thread(CheckTorrentThread, (info_hash,))
    return HttpResponse("OK")


def AjaxGetTorrentList(request):
    # 获取种子列表
    TorrentList = DB.TorrentList.objects.all()
    TorrentList = [{"info_hash": i.info_hash, "FileName": i.FileName, "FileSize": i.FileSize, "Status": i.Status,
                    "UpdateTime": i.UpdateTime, "AutoSeeding": i.AutoSeeding} for i in TorrentList]
    return HttpResponse(json.dumps(TorrentList))


def TorrentOP(request):
    OP = request.POST.get('OP')
    if OP == "AutoSeedingChange":
        if request.POST.get('AutoSeeding') == "true":
            AutoSeeding = True
        else:
            AutoSeeding = False
        DB.TorrentList.objects.filter(info_hash=request.POST.get('info_hash')).update(AutoSeeding=AutoSeeding)
    elif OP == "Delete":
        DB.TorrentList.objects.filter(info_hash=request.POST.get('info_hash')).delete()
    elif OP == "SetFileStoragePath":
        DB.SateliteInfo.objects.filter(Name="FileStoragePath").update(Value=request.POST.get('FileStoragePath'))
    elif OP == "Check":
        _thread.start_new_thread(CheckTorrentThread, (request.POST.get('info_hash'),))
    return HttpResponse("OK")


def TorrentManagement(request):
    FileStoragePath = DB.SateliteInfo.objects.get(Name="FileStoragePath")
    context = {"FileStoragePath": FileStoragePath.Value, "Mlang": MLang.GetLang(request.LANGUAGE_CODE)}
    Response = render(request, 'torrent-management.html', context)
    return Response


def UploadFile(request):
    # 文件上传
    FileStoragePath = DB.SateliteInfo.objects.get(Name="FileStoragePath")
    Fw = open(FileStoragePath.Value + "/" + request.FILES["file"].name, "wb")
    for chunk in request.FILES["file"].chunks():
        Fw.write(chunk)
    Fw.close()
    return HttpResponse("OK")


def TorrentDownload(request):
    info_hash = request.GET.get('info_hash')
    FileStoragePath = DB.SateliteInfo.objects.get(Name="FileStoragePath")
    TorrentInfo = DB.TorrentList.objects.get(info_hash=info_hash)
    response = StreamingHttpResponse(ReadFile(FileStoragePath.Value + "/Torrents/" + info_hash + ".torrent"))
    response["Content-Type"] = "application/x-bittorrent"
    response["Content-Disposition"] = 'attachment; filename={0}'.format(TorrentInfo.FileName + ".torrent")
    response["Access-Control-Expose-Headers"] = "Content-Disposition"
    return response


def CreateBT(request):
    CreateDownload(request.GET.get('IP'), request.GET.get('info_hash'))
    return HttpResponse("OK")
