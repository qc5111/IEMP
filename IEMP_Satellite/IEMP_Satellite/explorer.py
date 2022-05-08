import json
from IEMP_Satellite.Authorization import AuthorizationCheck
from IEMP_Satellite.settings import MLang
from django.http import HttpResponse
from django.shortcuts import render
from .Function import BytesAndString
from .Function import FileOP
import MainDB.models as DB
from .Function.OrderSendToClient import Client


@AuthorizationCheck
def explorer(request):
    # DeviceList = DB.Machine.objects.all()[0:15]
    ID = request.GET.get("id")

    try:
        MachineInfo = DB.Machine.objects.get(ID=int(ID))
    except:
        return HttpResponse("Error! Machine does not exist!")
    if MachineInfo.OPSystem == 0:
        Slash = '"\\\\"'
        RootDir = '""'
    else:
        Slash = '"/"'
        RootDir = '"/"'
    context = {'ID': ID, 'IP': MachineInfo.IP, 'Slash': Slash, 'RootDir': RootDir,
               "Mlang": MLang.GetLang(request.LANGUAGE_CODE)}
    print(context)
    return render(request, 'explorer.html', context)


@AuthorizationCheck
def GetFileList(request):
    ID = request.GET.get("ID")
    MAC = request.GET.get("MAC")
    Dir = request.GET.get("Dir")

    try:
        Machine = DB.Machine.objects.get(ID=int(ID))
        Client1 = Client(Machine)
        if Client1.OPSystem == 0 or Client1.OPSystem == 3:
            Client1.Encoding = "GB2312"
        result = Client1.GetFileList(Dir)
        return HttpResponse(json.dumps(result, ensure_ascii=False))
    except:
        return HttpResponse("Fail")
