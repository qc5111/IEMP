from socket import *
from . import DynamicPassword
import os
import struct
import datetime
import zlib
import time


class FileOP:
    IP = ""
    Password = ""
    RootPath = "C:\\IEMP_Client\\"
    Encoding = "UTF-8"

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
        tcp_client_socket.recv(10)
        tcp_client_socket.close()

    def SendFileToIEMPRoot(self, FilePath, RemoteSavePath):
        self.SendFile(FilePath, "%s%s" % (self.RootPath, RemoteSavePath))

    def GetFile(self):
        tcp_client_socket = self.NormalOrderSend(b'\x01\x01')




"""
#TestClient = FileOP("10.0.1.123", b"0123456789abcdef")
#i = 0
#while True:
#    
#    TestResult=TestClient.GetFileList(r"D:\TEST")#C:\Windows\System32
#    #TestClient.GetFile()
#    #print(TestResult)
#    i+=1
#    print(i)
#    if i == 10000:
#        break;
    
    #time.sleep(0.05)
TestResult=TestClient.GetFileList(r"C:\Windows\System32")
print(TestResult)
TotalSize = 0
TotalFile = 0
exit()
for i in TestResult:
    
    if i["Type"] == 8:
        TotalSize+=i["Size"]
        TotalFile+=1
        if i["Size"] == 0:
            print(i)
    #print(i)
print(TotalSize)
print(TotalFile)
"""
