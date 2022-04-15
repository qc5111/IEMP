import ctypes
from ctypes import memmove

from django.http import HttpResponse
from IEMP_Satellite.Function import wol, BytesAndString

import MainDB.models as DB
from IEMP_Satellite.Function.OrderSendToClient import Client


def TurnOn(request):
    Device = DB.Machine.objects.get(ID=request.GET.get("ID"))
    wol.Wol(Device.MAC, Device.IP)
    return HttpResponse("OK")


def TurnOff(request):
    Machine = DB.Machine.objects.get(ID=request.GET.get("ID"))
    Client1 = Client(Machine)
    Client1.NormalOrderSend(b"\x00\x00")
    return HttpResponse("OK")
