import sys

from .Function.RSA import GenerateRSAkey
from .HeartBeatServer import HeartBeatServer
from .WebSocket2SSH import WS, Loop
from . import Scripts, aria2c
import asyncio
import threading
import MainDB.models as DB


def ConfCheck():
    DBresult = DB.SateliteInfo.objects.filter(Name="PubKey")

    if not DBresult:
        PriKey, PubKey = GenerateRSAkey()
        DB.SateliteInfo.objects.create(Name="PriKey", Value=PriKey)
        DB.SateliteInfo.objects.create(Name="PubKey", Value=PubKey)
    DBresult = DB.SateliteInfo.objects.filter(Name="FileStoragePath")
    if not DBresult:
        DB.SateliteInfo.objects.create(Name="FileStoragePath", Value="IEMP_Satellite/Files")


def SoftInit():
    if sys.argv[1] == "runserver":
        # 判断基础配置是否存在
        ConfCheck()

        HeartBeatServer()
        ws1 = WS()
        aria2c.Aria2c()
        WSLoop = asyncio.new_event_loop()
        threading.Thread(target=Loop, args=(WSLoop,)).start()
        asyncio.run_coroutine_threadsafe(ws1, WSLoop)
