import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = ("127.0.0.1", 48281)
s.sendto("test".encode(), addr)