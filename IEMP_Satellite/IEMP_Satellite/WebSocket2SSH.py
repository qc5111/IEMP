import threading
import time
import asyncio
import websockets
from socket import *
from urllib import parse
import paramiko
from asgiref.sync import sync_to_async

from IEMP_Satellite.Function import DynamicPassword
import MainDB.models as DB


async def WS():
    async with websockets.serve(WebSocket2SSH1.wsDeal, '0.0.0.0', 48285):
        await asyncio.Future()  # run forever


def Loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


class SSHInterface:
    def __init__(self, Host, Port, Username, Password, websocket):
        self.websocket = websocket
        self.sshc = paramiko.SSHClient()
        self.sshc.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshc.connect(Host, Port, Username, Password)
        self.InterChannel = self.sshc.invoke_shell(term='xterm')
        SSHRecv1 = self.SSHRecv()
        self.SSHRecvLoop = asyncio.new_event_loop()
        threading.Thread(target=Loop, args=(self.SSHRecvLoop,)).start()
        asyncio.run_coroutine_threadsafe(SSHRecv1, self.SSHRecvLoop)

    async def SSHRecv(self):
        while True:
            await asyncio.sleep(0.05)
            if self.InterChannel.recv_ready():
                await self.websocket.send(self.InterChannel.recv(1024))

    def Close(self):
        self.sshc.close()
        self.SSHRecvLoop.stop()


class CMDInterface:
    def __init__(self, IP, Port, InitInfo, websocket):
        self.websocket = websocket
        self.tcp_client_socket = socket(AF_INET, SOCK_STREAM)
        self.tcp_client_socket.connect((IP, Port))
        self.tcp_client_socket.send(InitInfo)
        CMDRecv1 = self.CMDRecv()
        self.CMDRecvLoop = asyncio.new_event_loop()
        threading.Thread(target=Loop, args=(self.CMDRecvLoop,)).start()
        asyncio.run_coroutine_threadsafe(CMDRecv1, self.CMDRecvLoop)

    async def CMDRecv(self):
        while True:
            RecvByte = self.tcp_client_socket.recv(1024)
            if RecvByte:
                RecvByte = RecvByte.replace(b"\r\n", b"\n")
                RecvByte = RecvByte.replace(b"\n", b"\r\n")
                await self.websocket.send(RecvByte.decode('GB2312').encode('utf-8'))
            else:
                break

    def Close(self):
        self.tcp_client_socket.close()
        self.CMDRecvLoop.stop()


class WebSocket2SSH:
    def __init__(self):
        self.websocket = None

    async def wsDeal(self, websocket, path):
        params = parse.parse_qs(parse.urlparse(path).query)
        Machine = await sync_to_async(DB.Machine.objects.get)(ID=int(params['EID'][0]))
        await websocket.send('{"OPSystem":%d}' % Machine.OPSystem)
        if Machine.OPSystem == 1:  # Linux
            Command = SSHInterface(Machine.IP, 22, Machine.RootUsername, Machine.RootPassword, websocket)
        elif Machine.OPSystem == 0:  # Windows
            Command = CMDInterface(Machine.IP, 48281,
                                   DynamicPassword.DynamicPassword("0123456789abcdef".encode(), 8) + "cmd.exe".encode(
                                       "GB2312"), websocket)
        async for message in websocket:
            try:
                if Machine.OPSystem == 1:  # Linux
                    Command.InterChannel.send(message)
                elif Machine.OPSystem == 0:  # Windows
                    message = message.replace("\r", "\n")
                    Command.tcp_client_socket.send(message.encode("GB2312"))
            except Exception as e:
                break

        Command.Close()


WebSocket2SSH1 = WebSocket2SSH()

# .SSHInit("10.7.0.1", 22, "root", "password")
