from . import pipe
from . import DynamicPassword
class DiskOP:
    DiskArray = []
    VolumeArray = []
    def __init__(self,IP,Port,Password):
        self.p_Diskpart = pipe.RemotePipe(IP,Port,DynamicPassword.DynamicPassword(Password,8)+"diskpart.exe".encode("GB2312"))
    def GetDiskList(self):
        CMDresult = self.p_Diskpart.AutoExec("list disk")
        DiskList = CMDresult[:CMDresult.find("\r\n\r\n")].strip().split("\r\n")
        self.DiskArray = []
        for i in DiskList:
            Disk = i.split()
            try:
                int(Disk[1])
                if Disk[2] == "联机" or Disk[2] == "Online":
                    Disk[2] = True
                elif Disk[2] == "脱机" or Disk[2] == "Offline":
                    Disk[2] = False
                if Disk[4] == "KB":
                    Disk[3] = int(Disk[3])/1024
                    pass
                elif Disk[4] == "MB":
                    Disk[3] = int(Disk[3])
                elif Disk[4] == "GB":
                    Disk[3] = int(Disk[3])*1024
                elif Disk[4] == "TB":
                    Disk[3] = int(Disk[3])*1048576
                
                if Disk[6] == "KB":
                    Disk[5] = int(Disk[5])/1024
                    pass
                elif Disk[6] == "MB":
                    Disk[5] = int(Disk[5])
                elif Disk[6] == "GB":
                    Disk[5] = int(Disk[5])*1024
                elif Disk[6] == "TB":
                    Disk[5] = int(Disk[5])*1048576
                self.DiskArray.append({"ID":int(Disk[1]),"Online":Disk[2],"Size":Disk[3],"FreeSize":Disk[5]})# All Size is MB
            except ValueError:
                pass  
        # print("DiskArray:",DiskArray)
    def GetVolumeList(self):
        CMDresult = self.p_Diskpart.AutoExec("list volume")
        VolumeList = CMDresult[:CMDresult.find("\r\n\r\n")].strip().split("\r\n")
        self.VolumeArray = []
        for i in VolumeList:
            Volume = i.split()
            try:
                int(Volume[1])
                LocateSign = 4
                while True:
                    if Volume[LocateSign] == "KB" or Volume[LocateSign] == "MB" or Volume[LocateSign] == "GB" or Volume[LocateSign] == "TB":
                        break
                    LocateSign += 1
                if Volume[LocateSign] == "KB":
                    Volume[LocateSign-1] = int(Volume[LocateSign-1])/1024
                    pass
                elif Volume[LocateSign] == "MB":
                    Volume[LocateSign-1] = int(Volume[LocateSign-1])
                elif Volume[LocateSign] == "GB":
                    Volume[LocateSign-1] = int(Volume[LocateSign-1])*1024
                elif Volume[LocateSign] == "TB":
                    Volume[LocateSign-1] = int(Volume[LocateSign-1])*1048576
                    
                if LocateSign == 7:
                    self.VolumeArray.append({"ID":int(Volume[1]),"Letter":Volume[2],"Name":Volume[3],"Format":Volume[LocateSign-3],"Size":Volume[LocateSign-1]})
                elif LocateSign == 6:
                    if len(Volume[2]) == 1:
                        self.VolumeArray.append({"ID":int(Volume[1]),"Letter":Volume[2],"Name":"","Format":Volume[LocateSign-3],"Size":Volume[LocateSign-1]})
                    else:
                        self.VolumeArray.append({"ID":int(Volume[1]),"Letter":"","Name":Volume[2],"Format":Volume[LocateSign-3],"Size":Volume[LocateSign-1]})
                elif LocateSign == 5:
                    self.VolumeArray.append({"ID":int(Volume[1]),"Letter":"","Name":"","Format":Volume[LocateSign-3],"Size":Volume[LocateSign-1]})
                
            except ValueError:
                pass
        #print(self.VolumeArray)
    def SelectDisk(self,Filter,Value):
        if self.DiskArray == []:
            self.GetDiskList()
        for i in self.DiskArray:
            if i[Filter] == Value:
                self.p_Diskpart.AutoExec("select disk %d" % i["ID"])
                break
    def SelectVolume(self,Filter,Value):
        if self.VolumeArray == []:
            self.GetVolumeList()
        for i in self.VolumeArray:
            if i[Filter] == Value:
                self.p_Diskpart.AutoExec("select volume %d" % i["ID"])
                break
    def CompressedVolume(self,size):
        self.p_Diskpart.AutoExec("shrink desired %d" % size)
    def CreatePartition(self,PartitionType,size):
        self.p_Diskpart.AutoExec("create partition %s size=%d" % (PartitionType,size))
    def Format(self,Format,label="",quick=True):
        if quick:
            quick = " quick"
        else:
            quick = ""
        self.p_Diskpart.AutoExec("format%s fs=%s label=%s" % (quick,Format,label))
    def ASSIGN(self,BestLetter="Z"):
        LetterASCII = ord(BestLetter.upper())
        while True:
            CMDresult = self.p_Diskpart.AutoExec("ASSIGN LETTER=%s" % chr(LetterASCII))
            if "error" in CMDresult or "错误" in CMDresult:
                LetterASCII += 1
                if LetterASCII>90:
                    LetterASCII = 65
                continue
            return chr(LetterASCII)#Return real disk letter
    def close(self):
        self.p_Diskpart.close()

