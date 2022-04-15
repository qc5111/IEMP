import os
import platform


# 此文件支持Windows与Linux
def GetMacFromIP(IP):  # MAC=GetMacFromIP("10.0.1.214")
    System = platform.system().lower()
    cmd = os.popen('arp -a')
    ARPInfo = cmd.read()
    cmd.close()
    ARPInfo = ARPInfo.split("\n")
    if System == "windows":
        for i in ARPInfo:
            SingleArpInfo = i.strip().split()
            if len(SingleArpInfo) > 1:
                if SingleArpInfo[0] == IP:
                    return SingleArpInfo[1].replace("-", "").replace(":", "").upper()
    elif System == "linux":
        for i in ARPInfo:
            SingleArpInfo = i.strip().split()
            if len(SingleArpInfo) > 4:
                if SingleArpInfo[1] == ("(" + IP + ")"):
                    return SingleArpInfo[3].replace("-", "").replace(":", "").upper()
    return ""
