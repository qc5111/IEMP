from django.http import HttpResponse
from django.shortcuts import render
import MainDB.models as DB


def explorer(request):
    # DeviceList = DB.Machine.objects.all()[0:15]
    context = {'IP': request.GET.get("IP")}
    return render(request, 'explorer.html', context)
