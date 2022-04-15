#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import struct
import socket
import _thread
import time

import MainDB.models as DB
from IEMP_Satellite.EventReg import ExcuteEvent
from IEMP_Satellite.Function.GetMacFromIP import GetMacFromIP


class HeartBeatServer:
    HeartBeatSpeed = 120

    def __init__(self):
        self.UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.UDP.bind(("0.0.0.0", 48281))
        _thread.start_new_thread(self.PackageDeal, (1,))
        _thread.start_new_thread(self.TimeoutCheck, (1,))

    def TimeoutCheck(self, p):
        while True:
            MachineList = DB.Machine.objects.filter(Status=1,
                                                    LastUpdateTime__lte=int(time.time()) - self.HeartBeatSpeed * 1.5)
            for i in MachineList:
                i.Status = 0
                i.save()
            time.sleep(self.HeartBeatSpeed)

    def PackageDeal(self, p):
        while True:
            data, addr = self.UDP.recvfrom(1024)
            # print(addr)
            # print(data)
            if data[0] == 0:
                Pos = 1
                # print(data[Pos:Pos + 4])
                EID = struct.unpack("<I", data[Pos:Pos + 4])[0]
                Pos += 4
                Version = struct.unpack("<I", data[Pos:Pos + 4])[0]
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
                if DB.Machine.objects.filter(ID=EID).exists():
                    NowMachine = DB.Machine(ID=EID, IP=addr[0], Version=Version, TotalMemory=TotalMemory, Cores=Cores,
                                            MAC=GetMacFromIP(addr[0]),
                                            MotherBoardName=MotherBoard, OPSystemName=SystemName, CPUName=CPUName,
                                            Status=1,
                                            LastUpdateTime=int(time.time()))
                    NowMachine.save()

                ExcuteEvent("EquipmentOnline", NowMachine)


            elif data[0] == 1:
                print(len(data))
                if len(data) != 13:
                    continue
                EID = struct.unpack("<I", data[1:5])[0]
                CPUUse = struct.unpack("<f", data[5:9])[0]
                MemoryUse = struct.unpack("<I", data[9:13])[0]
                try:
                    NowMachine = DB.Machine.objects.get(ID=EID)
                except:
                    continue
                NowMachine.UsingCPU = int(CPUUse * 10000)
                NowMachine.UsingMemory = MemoryUse
                NowMachine.LastUpdateTime = int(time.time())
                NowMachine.save()
            else:
                print(data)
