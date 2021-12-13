import time
from socket import *
from . import DynamicPassword
import os
import struct

import datetime

from ..settings import DefaultFilePath


class Client:
    RootPath = ""
    Encoding = ""

    def __init__(self, IP, Password):
        self.IP = IP
        self.Password = Password

    def NormalOrderSend(self, Order):
        tcp_client_socket = socket(AF_INET, SOCK_STREAM)
        tcp_client_socket.connect((self.IP, 48280))
        code = DynamicPassword.DynamicPassword(self.Password, 8)
        # print(Order)
        tcp_client_socket.send(struct.pack('<I', len(Order) + 8)[:2])
        tcp_client_socket.send(code + Order)
        return tcp_client_socket

    def SendFile(self, FilePath, RemoteSavePath):
        FilePath = DefaultFilePath + FilePath;
        FileSize = os.path.getsize(FilePath)
        tcp_client_socket = self.NormalOrderSend(
            b'\x01\x00' + RemoteSavePath.encode(self.Encoding) + b"\x00" + struct.pack('<Q', FileSize))
        fr = open(FilePath, "rb")
        tcp_client_socket.recv(1)
        while True:
            FileData = fr.read(1024)
            if FileData == b"":
                break
            tcp_client_socket.send(FileData)
        # tcp_client_socket.recv(10)
        tcp_client_socket.close()

    def SendOneCMDOrder(self, order):
        self.NormalOrderSend(b'\x00\x06' + order.encode(self.Encoding))

    def ExecMultipleOrder(self, orders):
        fw = open("Files\\order.temp.file", "wb")
        for i in orders:
            fw.write((i + "\n").encode(self.Encoding))
        fw.close()
        # print("Files\\order.temp.file", '"%sTemp\\order.bat"' % self.RootPath)
        self.SendFileToIEMPRoot("Files\\order.temp.file", 'Temp\\order.bat')
        # self.NormalOrderSend(b'\x00\x06' + ('"%sTemp\\order.bat"' % TestClient.RootPath).encode(TestClient.Encoding))
        self.SendOneCMDOrder('"%sTemp\\order.bat"' % self.RootPath)

    def StartNewProcess(self, order):
        self.NormalOrderSend(b'\x00\x08' + order.encode(self.Encoding))

    def ExitIEMP(self):
        self.NormalOrderSend(b"\x02\x00")

    def SendFileToIEMPRoot(self, FilePath, RemoteSavePath):
        self.SendFile(FilePath, "%s%s" % (self.RootPath, RemoteSavePath))


class WinClient(Client):
    RootPath = "C:\\IEMP_Client\\"
    Encoding = "GB2312"

    def SelfRenew(self, FileName):
        RenewScript = 'set ws=WScript.CreateObject("WScript.Shell")\n' \
                      + 'wscript.sleep 500\n' \
                      + 'Dim Fso,shell\n' \
                      + 'Set Fso = WScript.CreateObject("Scripting.FileSystemObject")\n' \
                      + 'Set shell = Wscript.createobject("wscript.shell")\n' \
                      + 'Fso.DeleteFile"Update.vbs"\n' \
                      + 'Fso.DeleteFile"IEMP_Client.exe"\n' \
                      + 'Fso.MoveFile"IEMP_ClientNew.exe","IEMP_Client.exe"\n' \
                      + 'shell.run "IEMP_Client.exe"\n'
        self.SendFileToIEMPRoot("Win\\IEMP_Client_Latest.exe.file", "IEMP_ClientNew.exe")
        self.NormalOrderSend(b'\x02\x01' + b"IEMP_ClientNew.exe" + b'\x00' + RenewScript.encode(self.Encoding))

    def Init7zip(self):  # 初始化7zip
        # self.NormalOrderSend(b'\x00\x06' + ('mkdir "%sTools\\"' % self.RootPath).encode(self.Encoding))
        self.SendOneCMDOrder('mkdir "%sTools\\"' % self.RootPath)
        # self.SendFile("Files\\7za.exe.file", "%sTools\\7za.exe" % self.RootPath)
        self.SendFileToIEMPRoot("7za.exe.file", "Tools\\7za.exe")

    def InitPython(self):
        # self.NormalOrderSend(b'\x00\x06' + ('mkdir "%sTemp\\"' % self.RootPath).encode(self.Encoding))
        self.SendOneCMDOrder('mkdir "%sTemp\\"' % self.RootPath)
        # self.SendFile("Files\\python39.run.7z.file", "%sTemp\\python39.run.7z" % self.RootPath)
        self.SendFileToIEMPRoot("Files\\python39.run.7z.file", "Temp\\python39.run.7z")
        self.ExecMultipleOrder(['"%sTools\\7za.exe" x "%sTemp\\python39.run.7z" -r -aoa -o"%sTools"' % (
            self.RootPath, self.RootPath, self.RootPath)])
        # self.SendFile("Files\\python39.lib.zip.file", "%sTools\\python\\python39.zip" % self.RootPath)
        self.SendFileToIEMPRoot("Files\\python39.lib.zip.file", "Tools\\python\\python39.zip")

# TestClient = WinClient("10.0.1.123", b"0123456789abcdef")
# TestClient.SendFile("Files\\7za.exe.file", "x:\\7za.exe")
# print("OK")
# TestClient = WinClient("10.0.1.250", "0123456789abcdef")
# TestClient.Init7zip()
# TestClient.InitPython()
# TestClient.ExecMultipleOrder(['"python.exe" "%sPyScript\\test.py"' % (TestClient.RootPath)])
# TestClient.ExecMultipleOrder(['C:\\IEMP_Client\\Test2\\RunAPP.exe'])
# TestClient.ExecMultipleOrder(['C:\\Windows\\notepad.exe'])
# TestClient.ExecMultipleOrder(['taskkill /im chrome.exe'])
# TestClient.ExecMultipleOrder(b'\x00\x06'+'taskkill /im wechat.exe'.encode(TestClient.Encoding))
# TestClient.NormalOrderSend(b'\x00\x06' + ('python C:\\IEMP_Client\\Test\\test.py').encode(TestClient.Encoding))
