import sys
def IPPort2Bytes(IP):
    #Port = int(Port)
    IPSplited = IP.split(".")
    #IPSplited.append(int(Port / 256))
    #IPSplited.append(Port % 256)
    ReturnData = []
    for i in IPSplited:
        HexData = hex(int(i))[2:]
        if len(HexData) == 1:
            HexData = "0" + HexData
        ReturnData.append(HexData)

    return bytes.fromhex("".join(ReturnData))
#默认配置开始
Code = b"0123456789abcdef"
ServerIP = "10.0.1.4"
#心跳汇报
HeartBeatAuto = 1;
HeartBeatAllow = 1;
#监控汇报
PerformanceMonitorAuto = 1;
PerformanceMonitorAllow = 1;
#远程CMD
RemoteCMDAuto = 1;
RemoteCMDAllow = 1;
#默认配置结束
WriteData = b""
WriteData += Code #写到第16位
# print(IPPort2Bytes(ServerIP))
WriteData += IPPort2Bytes(ServerIP) #写到第20位
Conf1 = HeartBeatAuto
Conf1 += HeartBeatAllow << 1
Conf1 += PerformanceMonitorAuto << 2
Conf1 += PerformanceMonitorAllow << 3
Conf1 += RemoteCMDAuto << 4
Conf1 += RemoteCMDAllow << 5
WriteData += bytes([Conf1]) #写到第21位
WriteData += bytes(32-len(WriteData)) #补齐到32位
#print(WriteData)
#print(len(WriteData))

Fw = open(sys.argv[1],"ab")
Fw.write(WriteData)
Fw.close()