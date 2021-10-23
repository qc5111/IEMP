#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import struct
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", 48281))

while True:
    data, addr = s.recvfrom(1024)
    print("Receive from %s:%s" % addr)
    print(data)
    if data[0] == 0:
        Pos = 1
        EID = data[Pos:Pos + 4]
        Pos += 4
        TotalMemory = struct.unpack("<Q", data[Pos:Pos + 8])[0]
        Pos += 8
        Cores = data[Pos] + data[Pos + 1] * 256
        Pos += 2
        MotherBoard = data[Pos + 1:Pos + 1 + data[Pos]].decode()
        Pos += 1 + data[Pos]
        SystemName = data[Pos + 1:Pos + 1 + data[Pos]].decode()
        Pos += 1 + data[Pos]
        CPUName = data[Pos + 1:Pos + 1 + data[Pos]].decode()
        print("EID:", EID)
        print("TotalMemory:", TotalMemory)
        print("Cores:", Cores)
        print("MotherBoard:", MotherBoard)
        print("SystemName'"+SystemName+"'")
        print("CPUName:", CPUName)

        # print(data)
    elif data[0] == 1:
        CPUUse = struct.unpack("<f", data[1:5])[0]
        MemoryUse = struct.unpack("<I", data[-4:])[0]
        print("CPU:%.2f%%" % (CPUUse * 100))
        print("Memory:%.2fGB" % (MemoryUse / 1024))
    else:

        print(data)
