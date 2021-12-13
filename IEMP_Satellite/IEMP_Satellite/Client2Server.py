import json
import socket  # 网络编程需要用到socket模块
import struct
import sys
import time
import _thread
import zstd

from collections import OrderedDict

import django.core.handlers.wsgi
from django.http import HttpResponse

from django.urls.resolvers import URLResolver, URLPattern
from django.utils.module_loading import import_string

from IEMP_Satellite import settings


def recursion_urls(param, param1, urlpatterns, url_ordered_dict):
    pass


class Client2Server:
    def __init__(self, ServerIP, ServerPort, EID):
        _thread.start_new_thread(self.TrytoConnect, (ServerIP, ServerPort, EID))
    def TrytoConnect(self,ServerIP, ServerPort,EID):
        Success = False
        self.client = socket.socket()  # 创建一个客户端
        while not Success:
            try:
                self.client.connect((ServerIP, ServerPort))  # 连接服务端
                self.client.send(EID)  # EID
                _thread.start_new_thread(self.DataWait, (EID,))
                Success = True
            except:
                time.sleep(30)
    def dealItmes(self, Items):
        ItemDict = {}
        for key, value in Items():
            DataString = value.OutputString(None)
            DataArray = DataString.split(";")
            for DataString in DataArray:
                DataArray = DataString.strip().split("=")
                ItemDict[DataArray[0]] = DataArray[1]
        return ItemDict

    def DataWait(self, EID):
        while True:
            SendSign = False
            Order = self.client.recv(1)  # 接受服务端发来的指令
            if Order == b"\x00":
                self.client.send(b"\x00\x00\x00\x00")
            elif Order == b"\x01":
                DataLen = struct.unpack('<I', self.client.recv(4))[0]  # 数据总长度
                # print(DataLen)
                RequestJson = self.client.recv(DataLen)
                print(len(RequestJson))
                RequestJson = zstd.decompress(RequestJson)
                print(len(RequestJson))
                # RequestJson = RequestJson.decode(encoding="UTF-8")

                environ = json.loads(RequestJson)

                environ["wsgi.input"] = sys.stdin
                environ["wsgi.errors"] = sys.stderr
                environ["_MODULE"] = "IEMP_Client.settings"

                # environ["_MODULE"] = "IEMP_Client.settings"
                request = django.core.handlers.wsgi.WSGIRequest(environ)  # new
                # 匹配URL

                md = import_string(settings.ROOT_URLCONF)
                for i in md.urlpatterns:
                    if i.pattern.match(request.path_info[1:]) is not None:
                        Response = i.callback(request)
                        ResponseJson = {
                            "headers": str(Response.headers),
                            "_charset": Response._charset,
                            "_resource_closers": Response._resource_closers,
                            "_handler_class": Response._handler_class,
                            "closed": Response.closed,
                            "_reason_phrase": Response._reason_phrase,
                            "_container": Response._container[0].decode(),
                        }

                        if len(Response.cookies.items()) > 0:
                            ResponseJson["cookies"] = self.dealItmes(Response.cookies.items)

                        ResponseJson = json.dumps(ResponseJson, ensure_ascii=False)
                        ResponseJson = ResponseJson.encode(encoding="UTF-8")
                        # 压缩
                        ResponseJson = zstd.compress(ResponseJson)
                        # 加密
                        self.client.send(b"\x00")
                        self.client.send(struct.pack('<I', len(ResponseJson)))
                        self.client.send(ResponseJson)
                        SendSign = True
                        break
                #
                if not SendSign:
                    self.client.send(b"\xff")

    def close(self):
        self.client.close()  # 关闭客户端

# time.sleep(1000)
