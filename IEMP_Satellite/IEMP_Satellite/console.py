from django.shortcuts import render
from django.http import HttpResponse

from IEMP_Satellite.Authorization import AuthorizationCheck
from IEMP_Satellite.settings import MLang


@AuthorizationCheck
def console(request):
    context = {"Mlang": MLang.GetLang(request.LANGUAGE_CODE)}
    Response = render(request, 'console.html', context)
    return Response

