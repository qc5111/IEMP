import hashlib
from functools import wraps
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

import MainDB.models as DB
from IEMP_Satellite.settings import MLang


def AuthorizationCheck(func):
    @wraps(func)
    def wrapTheFunction(request):
        if "Username" in request.session:
            if request.session["Username"] == DB.SateliteInfo.objects.get(Name="Username").Value:
                return func(request)
        return HttpResponseRedirect("/Login")

    return wrapTheFunction


def Login(request):
    context = {"Mlang": MLang.GetLang(request.LANGUAGE_CODE)}
    Response = render(request, 'login.html', context)
    return Response


def AjaxLogin(request):
    if request.POST.get('Username') == DB.SateliteInfo.objects.get(Name="Username").Value and hashlib.sha1(
            request.POST.get(
                'Password').encode()).hexdigest() == DB.SateliteInfo.objects.get(Name="Password").Value:
        request.session["Username"] = request.POST.get('Username')
        return HttpResponse("OK")
    else:
        return HttpResponse("ERROR")


def Logout(request):
    request.session.flush()
    return HttpResponseRedirect("/Login")
