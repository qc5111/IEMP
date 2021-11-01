import json
import socket  # 网络编程需要用到socket模块
import _thread
import struct
import threading
import time

import zstd
from django.http import HttpResponse


def IP2Bytes(IP, Port):
    ReturnArr = [0] * 6
    IP = IP.split(".")
    ReturnArr[0] = int(IP[0])
    ReturnArr[1] = int(IP[1])
    ReturnArr[2] = int(IP[2])
    ReturnArr[3] = int(IP[3])
    ReturnArr[4] = int(Port / 256)
    ReturnArr[5] = Port % 256
    return bytes(ReturnArr)


def EnvironSimplify(environ):
    environnew = {"SERVER_NAME": environ["SERVER_NAME"], "GATEWAY_INTERFACE": environ["GATEWAY_INTERFACE"],
                  "SERVER_PORT": environ["SERVER_PORT"], "REMOTE_HOST": environ["REMOTE_HOST"],
                  "CONTENT_LENGTH": environ["CONTENT_LENGTH"], "SCRIPT_NAME": environ["SCRIPT_NAME"],
                  "SERVER_PROTOCOL": environ["SERVER_PROTOCOL"], "SERVER_SOFTWARE": environ["SERVER_SOFTWARE"],
                  "REQUEST_METHOD": environ["REQUEST_METHOD"], "PATH_INFO": environ["PATH_INFO"],
                  "QUERY_STRING": environ["QUERY_STRING"], "REMOTE_ADDR": environ["REMOTE_ADDR"],
                  "CONTENT_TYPE": environ["CONTENT_TYPE"], "HTTP_HOST": environ["HTTP_HOST"],
                  "HTTP_CONNECTION": environ["HTTP_CONNECTION"], "HTTP_SEC_CH_UA": environ["HTTP_SEC_CH_UA"],
                  "HTTP_SEC_CH_UA_MOBILE": environ["HTTP_SEC_CH_UA_MOBILE"],
                  "HTTP_SEC_CH_UA_PLATFORM": environ["HTTP_SEC_CH_UA_PLATFORM"],
                  "HTTP_USER_AGENT": environ["HTTP_USER_AGENT"], "HTTP_ACCEPT": environ["HTTP_ACCEPT"],
                  "HTTP_SEC_FETCH_SITE": environ["HTTP_SEC_FETCH_SITE"],
                  "HTTP_SEC_FETCH_MODE": environ["HTTP_SEC_FETCH_MODE"],
                  "HTTP_SEC_FETCH_DEST": environ["HTTP_SEC_FETCH_DEST"],
                  "HTTP_ACCEPT_ENCODING": environ["HTTP_ACCEPT_ENCODING"],
                  "HTTP_ACCEPT_LANGUAGE": environ["HTTP_ACCEPT_LANGUAGE"], "wsgi.version": environ["wsgi.version"],
                  "wsgi.run_once": environ["wsgi.run_once"], "wsgi.url_scheme": environ["wsgi.url_scheme"],
                  "wsgi.multithread": environ["wsgi.multithread"], "wsgi.multiprocess": environ["wsgi.multiprocess"]}
    return environnew


class IEMP_Server:
    ClientDict = {}
    ClientDictLock = threading.Lock()

    def __init__(self):
        print("listenOK1")
        _thread.start_new_thread(self.ConListener, ('0.0.0.0', 48289))

    def ConListener(self, IP, Port):
        server = socket.socket()
        server.bind((IP, Port))
        server.listen()
        print("listenOK")
        while True:
            Conn, Addr = server.accept()
            Addr = IP2Bytes(Addr[0], Addr[1])
            EID = Conn.recv(4)
            _thread.start_new_thread(self.DataWait, (EID,))
            self.ClientDictLock.acquire()
            self.ClientDict[EID] = {"Conn": Conn, "Addr": Addr, "CommLock": threading.Lock()}
            self.ClientDictLock.release()
            print(self.ClientDict)

    def DataWait(self, EID):
        while True:
            time.sleep(1)  # 常规值为60

            try:
                self.ClientDict[EID]["CommLock"].acquire()  # 通讯锁
                self.ClientDict[EID]["Conn"].send(b"\x00")  # 发送通讯请求
                self.ClientDict[EID]["CommLock"].release()  # 通讯锁释放
                Data = self.ClientDict[EID]["Conn"].recv(4)
                if Data == b"\x00\x00\x00\x00":
                    pass
                else:
                    pass
            except:  # 收发包异常，认为客户端掉线
                print(EID, "Lost")
                try:
                    self.ClientDict[EID]["Conn"].close()
                finally:
                    self.ClientDictLock.acquire()
                    del self.ClientDict[EID]
                    self.ClientDictLock.release()
                    break

    def GetResponse(self, EID, request):
        # 预处理environ
        environ = EnvironSimplify(request.environ)
        JsonData = json.dumps(environ, ensure_ascii=False).encode(encoding="UTF-8")
        JsonData = zstd.compress(JsonData)
        # 压缩
        # 加密
        # print(self.ClientDict)
        self.ClientDict[EID]["CommLock"].acquire()  # 通讯锁
        try:
            self.ClientDict[EID]["Conn"].send(b"\x01")  # 发送通讯请求
            self.ClientDict[EID]["Conn"].send(struct.pack('<I', len(JsonData)))
            self.ClientDict[EID]["Conn"].send(JsonData)
        except:
            print(EID, "Lost")
            try:
                self.ClientDict[EID]["Conn"].close()
            finally:
                self.ClientDictLock.acquire()
                del self.ClientDict[EID]
                self.ClientDictLock.release()

        Order = self.ClientDict[EID]["Conn"].recv(1)  # 代表接受完毕
        if Order == b"\x00":  # 普通http返回
            DataLen = struct.unpack('<I', self.ClientDict[EID]["Conn"].recv(4))[0]  # 数据总长度
            ResponseJson = self.ClientDict[EID]["Conn"].recv(DataLen)  # .decode(encoding="UTF-8")
            print(len(ResponseJson))
            ResponseJson = zstd.decompress(ResponseJson)
            print(len(ResponseJson))
            ResponseJson = json.loads(ResponseJson)
            ReturnValue = HttpResponse(ResponseJson["_container"])

            if "cookies" in ResponseJson:
                for key in ResponseJson["cookies"]:
                    if key != "Path":
                        ReturnValue.set_cookie(key, ResponseJson["cookies"][key])
            # print(ResponseJson)
        if Order == b"\xff":
            ReturnValue = HttpResponse("404")
        self.ClientDict[EID]["CommLock"].release()  # 通讯锁释放
        return ReturnValue

# IEMP_Server1 = IEMP_Server()
# IEMP_Server1.ConListener()

# print(conn, addr)
# c_info = conn.recv(1024)         #将接受的消息存入到c_info变量中
# print(c_info)
# conn.send(b'hello word')         #向客户端发出消息
# conn.close()                     #关闭连接
# server.close()                   #关闭服务端
