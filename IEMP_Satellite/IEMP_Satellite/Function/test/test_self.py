from socket import *
import time
import DynamicPassword
def CMDRecv(tcp_client_socket):
    global Order;
    while True:
        recvData=tcp_client_socket.recv(512)
        # print("Order:"+Order+",recvData:"+recvData.decode("GB2312")+",")
        if Order != recvData.decode("GB2312"):
            print(recvData.decode("GB2312"),end='')
        if recvData[-1] == 62 or recvData[-2] == 62:
            break
    # return recvBytes.join(recvdataArr).decode("GB2312")
    
    
Order = ""
tcp_client_socket = socket(AF_INET, SOCK_STREAM)
tcp_client_socket.connect(("10.0.1.130", 48281))

#tcp_client_socket.connect(("10.0.1.193", 48281))
CMDRecv(tcp_client_socket)
# tcp_client_socket.send("ping 114.114.114.114 -t\n".encode("GB2312"))
# CMDRecv(tcp_client_socket)

while True:
    Order = input()
    if Order == "exit":
        break
    Order += "\n"
    tcp_client_socket.send(DynamicPassword.DynamicPassword("0123456789abcdef".encode(),8)+Order.encode("GB2312"))
    CMDRecv(tcp_client_socket)



tcp_client_socket.send(b"\x00")
