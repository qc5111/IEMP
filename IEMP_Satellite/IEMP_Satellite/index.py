from django.http import HttpResponse
from django.shortcuts import render
import MainDB.models as DB
from IEMP_Satellite.settings import MLang


def index(request):
    DeviceList = DB.Machine.objects.all()[0:15]

    context = {'DeviceList': DeviceList, "Mlang": MLang.GetLang(request.LANGUAGE_CODE)}
    Response = render(request, 'index.html', context)
    Response.set_cookie("test", "123")
    return Response
