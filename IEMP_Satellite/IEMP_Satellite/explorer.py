from django.http import HttpResponse
from django.shortcuts import render
import MainDB.models as DB
from IEMP_Satellite.settings import MLang


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
    context = {'ID': ID, 'IP': MachineInfo.IP, 'Slash': Slash, 'RootDir': RootDir, "Mlang": MLang.GetLang(request.LANGUAGE_CODE)}
    print(context)
    return render(request, 'explorer.html', context)
