#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", 48281))

while True:
    data, addr = s.recvfrom(1024)
    print("Receive from %s:%s" % addr)
    print("data:"+data.decode())