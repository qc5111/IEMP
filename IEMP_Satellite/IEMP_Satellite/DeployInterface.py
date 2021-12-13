import _thread
import time

from django.http import HttpResponse
import MainDB.models as DB
import rsa
import base64
import socket  # 网络编程需要用到socket模块
from django.utils import timezone

from IEMP_Satellite.Function import RSA, BytesAndString
from IEMP_Satellite.Function.GetMacFromIP import GetMacFromIP


def GetRSAPubKey(request):
    PubKey = DB.SateliteInfo.objects.get(Name="PubKey").Value
    return HttpResponse(PubKey)


def RegNewDevice(request):
    DeviceInfo = base64.b64decode(request.GET.get("info"))
    DeviceInfo = RSA.RSADecrypt(DeviceInfo)
    Password = BytesAndString.Bytes2HexString(DeviceInfo[0:16])
    Info = DeviceInfo[16:].decode().split(",")

    if request.META.get('HTTP_X_FORWARDED_FOR'):
        IP = request.META.get("HTTP_X_FORWARDED_FOR")
    else:
        IP = request.META.get("REMOTE_ADDR")
    Info[0] = Info[0].lower()
    if Info[0] == "windows":
        Info[0] = 0
    elif Info[0] == "linux":
        Info[0] = 1
    elif Info[0] == "android":
        Info[0] = 2
    else:
        Info[0] = 3

    NewMachine = DB.Machine(
        Name=Info[2],
        OPSystem=Info[0],  # 0 Windows 1 Linux 2 Android
        CPUArch=Info[1],
        IP=IP,
        MAC=GetMacFromIP(IP),
        LastUpdateTime=int(time.time()),
        Password=Password,
        Type=int(Info[3]),  # DeviceType # 设备类型 0电脑 1手机 2服务器 3路由器 4未知
    )
    print(Info)
    NewMachine.save()
    return HttpResponse(NewMachine.ID)


def TCPInterface(P):
    server = socket.socket()  # 创建一个用于监听连接的Socket对像（服务器端）
    server.bind(('0.0.0.0', 48280))  # 设置服务端的ip和端口号
    server.listen()  # 开始监听
    while True:
        conn, addr = server.accept()  # 接受服务器端发出的消息和地址信息
        Order = conn.recv(2)  # 接受指令
        print(Order)
        if Order == b"\x00\x00":
            PubKey = DB.SateliteInfo.objects.get(Name="PubKey").Value
            conn.send(PubKey.encode())
            conn.close()  # 关闭连接
        elif Order == b"\x00\x01":  # 接受经过RSA加密的数据
            Data = conn.recv(256)
            Data = RSA.RSADecrypt(Data)
            print(BytesAndString.Bytes2HexString(Data))
            print(Data)
            # 此处需要返回编码的EID

    server.close()  # 关闭服务端

# _thread.start_new_thread(TCPInterface, (0,))
