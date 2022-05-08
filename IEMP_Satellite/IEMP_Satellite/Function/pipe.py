from socket import *
import time

# import DynamicPassword
from IEMP_Satellite.Function.DynamicPassword import DynamicPassword


class RemotePipe:
    Encoding = ""

    def AutoRead(self, endsign):
        RecvBytes = []
        while True:
            RecvByte = self.tcp_client_socket.recv(512)
            # print(RecvByte)
            RecvBytes.append(RecvByte)
            for i in endsign:
                # print(RecvByte[-len(i):],i)
                if RecvByte[-len(i):] == i:
                    return b"".join(RecvBytes).decode(self.Encoding)

    def __init__(self, Machine, InitOrder, Encoding="GB2312", endsign=[b">", b"> "]):
        self.Machine = Machine
        self.Encoding = Encoding
        self.tcp_client_socket = socket(AF_INET, SOCK_STREAM)
        self.tcp_client_socket.connect((Machine.IP, 48281))
        self.tcp_client_socket.send(DynamicPassword(self.Machine.Password, 8)+InitOrder.encode(self.Encoding))
        self.AutoRead(endsign)  # text1 =
        # print(text1,end='')

    def AutoExec(self, order, endsign=[b">", b"> "]):
        # print(order)
        self.tcp_client_socket.send((order + "\n").encode(self.Encoding))
        recvtext = self.AutoRead(endsign)
        # print(recvtext)
        return recvtext

    def close(self):
        self.tcp_client_socket.send(b"\x00")

# p_cmd = RemotePipe("10.0.1.123",48281,DynamicPassword.DynamicPassword("0123456789abcdef".encode(),8)+"cmd.exe".encode("GB2312"))
# p_cmd.AutoExec("diskpart")
# DiskList = p_cmd.AutoExec("list disk")
# print(DiskList)
# print("'"+CMDresult+"'",end='')
# time.sleep(10)
