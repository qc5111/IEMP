from django.http import HttpResponse
import django.core.handlers.wsgi
import wsgiref.util
import json

# django.core.handlers.wsgi.LimitedStream
from IEMP_Server import IEMP_Server1


import sys


def Test2(request):
    print(request.GET)
    return HttpResponse("TEST2")


def Test(request):
    print(request)
    # for key in request.environ:
    #     print(key, request.environ[key],type(request.environ[key]))

    environ = request.environ
    # print(environ["wsgi.input"].stream)
    # print(environ["wsgi.input"].remaining)
    # print(environ["wsgi.input"].buf_size)

    del environ["wsgi.input"]
    del environ["wsgi.errors"]
    del environ["wsgi.file_wrapper"]
    del environ["PATH"]
    del environ["TEMP"]
    del environ["PSMODULEPATH"]
    del environ["PYTHONPATH"]

    jsondata = json.dumps(environ)
    print(jsondata)

    environ2 = json.loads(jsondata)
    environ2["wsgi.input"] = sys.stdin
    environ2["wsgi.errors"] = sys.stderr

    req2 = django.core.handlers.wsgi.WSGIRequest(environ2)
    return Test2(req2)


def Proxy(request):
    EID = b'\x00\x00\x00\x00'

    return IEMP_Server1.GetResponse(EID, request)
