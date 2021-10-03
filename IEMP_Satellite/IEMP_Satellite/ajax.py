import json
from django.http import HttpResponse
from django.shortcuts import render
import MainDB.models as DB
from .Function import BytesAndString
from .Function import FileOP


def GetFileList(request):
    #  BytesAndString.Bytes2HexString()
    # 加入权限认证！！！！
    IP = request.GET.get("IP")
    Dir = request.GET.get("Dir")
    try:
        MachineInfo = DB.Machine.objects.get(IP=IP)
        Password = BytesAndString.HexString2Bytes(MachineInfo.Password)
        FileOP1 = FileOP.FileOP(IP, Password)
        result = FileOP1.GetFileList(Dir)
        return HttpResponse(json.dumps(result, ensure_ascii=False))
    except:
        return HttpResponse("Fail")
