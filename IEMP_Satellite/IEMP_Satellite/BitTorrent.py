from django.http import HttpResponse
from . import bencoding
import MainDB.models as DB
from pyaria2 import Aria2RPC


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


def announce(request):
    ReturnValue = {}
    SourceDict = {}
    SourceDict = request.GET.dict()

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
            SourceDict["Status"] = 2
        else:
            SourceDict["Status"] = 0
    else:
        SourceDict["Status"] = -1  # 状态不变
    SourceDict["IPAndPort"] = IPPort2Str(SourceDict["IP"], SourceDict["port"])
    # print("GET:", SourceDict)
    DBresult = DB.TrackerClientList.objects.filter(peer_id=SourceDict["peer_id"])
    # print(SourceDict["peer_id"])
    # print(len(SourceDict["peer_id"].decode("ascii")))
    # print(SourceDict["peer_id"])

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
    if SourceDict["left"] == "9223372036854775807":
        SourceDict["left"] = "100"

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


def test(request):
    print(request.body)
    return HttpResponse("OK")
