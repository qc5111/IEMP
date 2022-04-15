import json
from django.http import HttpResponse
from django.shortcuts import render
import MainDB.models as DB
from .Function import BytesAndString
from .Function import FileOP


def GetFileList(request):
    #  BytesAndString.Bytes2HexString()
    # 加入权限认证！！！！
    ID = request.GET.get("ID")
    Dir = request.GET.get("Dir")


    try:
        MachineInfo = DB.Machine.objects.get(ID=int(ID))
        Password = BytesAndString.HexString2Bytes(MachineInfo.Password)
        FileOP1 = FileOP.FileOP(MachineInfo.IP, Password)
        if MachineInfo.OPSystem == 0:
            FileOP1.Encoding = "ANSI"
        result = FileOP1.GetFileList(Dir)
        print("ajax ok")
        return HttpResponse(json.dumps(result, ensure_ascii=False))
    except:
        return HttpResponse("Fail")
