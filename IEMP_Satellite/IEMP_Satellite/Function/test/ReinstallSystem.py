import DiskOP
import OrderSendToClient
import DynamicPassword
import pipe
class ReinstallSystem:
    def __init__(self,IP,Port,Password):
        self.IP = IP
        self.Port = Port
        self.Password = Password
    def CreateRecoverVolume(self,size):
        DiskOP1 = DiskOP.DiskOP(self.IP,self.Port,self.Password)
        DiskOP1.SelectVolume("Letter","C")
        DiskOP1.CompressedVolume(size)
        DiskOP1.CreatePartition("primary",size)
        DiskOP1.Format("FAT32","WinPE")
        return DiskOP1.ASSIGN("X")
    def CopyPEFile(self,PE7zFilePath,VolumeLetter):
        WinClient1 = OrderSendToClient.WinClient(self.IP, self.Password)
        WinClient1.Init7zip()
        WinClient1.SendOneCMDOrder('mkdir "%sTemp\\"' % WinClient1.RootPath)
        WinClient1.SendFileToIEMPRoot(PE7zFilePath,"Temp\\WinPEAMD64.7z")
        p_CMD = pipe.RemotePipe(self.IP,self.Port,DynamicPassword.DynamicPassword(self.Password,8)+"cmd.exe".encode("GB2312"))
        p_CMD.AutoExec('"%sTools\\7za.exe" x "%sTemp\\WinPEAMD64.7z" -r -aoa -o"%s:"\n' % (WinClient1.RootPath, WinClient1.RootPath, VolumeLetter))
        p_CMD.close()
    def BootFromPE(self,VolumeLetter):
        p_CMD = pipe.RemotePipe(self.IP,self.Port,DynamicPassword.DynamicPassword(self.Password,8)+"cmd.exe".encode("GB2312"))
        p_CMD.AutoExec('bcdedit /delete {ffffffff-8d96-11de-8e71-fffffffffffe}')#清除以前可能存在的启动项
        p_CMD.AutoExec('bcdedit /create {ffffffff-8d96-11de-8e71-ffffffffffff} /d "Windows10 PE" /device')
        p_CMD.AutoExec('bcdedit /create {ffffffff-8d96-11de-8e71-fffffffffffe} /d "Windows10 PE" /application osloader')
        p_CMD.AutoExec('bcdedit /set {ffffffff-8d96-11de-8e71-ffffffffffff} ramdisksdidevice partition=%s:' % VolumeLetter)
        p_CMD.AutoExec('bcdedit /set {ffffffff-8d96-11de-8e71-ffffffffffff} ramdisksdipath \\Boot\\boot.sdi')
        p_CMD.AutoExec('bcdedit /set {ffffffff-8d96-11de-8e71-fffffffffffe} device ramdisk=[%s:]\\Sources\\boot.wim,{ffffffff-8d96-11de-8e71-ffffffffffff}' % VolumeLetter)
        p_CMD.AutoExec('bcdedit /set {ffffffff-8d96-11de-8e71-fffffffffffe} path \\windows\\system32\\boot\\winload.efi')
        p_CMD.AutoExec('bcdedit /set {ffffffff-8d96-11de-8e71-fffffffffffe} description "Windows10 PE"')
        p_CMD.AutoExec('bcdedit /set {ffffffff-8d96-11de-8e71-fffffffffffe} locale en-US')
        p_CMD.AutoExec('bcdedit /set {ffffffff-8d96-11de-8e71-fffffffffffe} inherit {bootloadersettings}')
        p_CMD.AutoExec('bcdedit /set {ffffffff-8d96-11de-8e71-fffffffffffe} osdevice ramdisk=[%s:]\\Sources\\boot.wim,{ffffffff-8d96-11de-8e71-ffffffffffff}' % VolumeLetter)
        p_CMD.AutoExec('bcdedit /set {ffffffff-8d96-11de-8e71-fffffffffffe} systemroot \\windows')
        p_CMD.AutoExec('bcdedit /set {ffffffff-8d96-11de-8e71-fffffffffffe} detecthal Yes')
        p_CMD.AutoExec('bcdedit /set {ffffffff-8d96-11de-8e71-fffffffffffe} winpe Yes')
        p_CMD.AutoExec('bcdedit /set {ffffffff-8d96-11de-8e71-fffffffffffe} ems no')
        p_CMD.AutoExec("bcdedit /bootsequence {ffffffff-8d96-11de-8e71-fffffffffffe} /addfirst")
        WinClient1 = OrderSendToClient.WinClient(self.IP, self.Password)
        WinClient1.NormalOrderSend(b"\x00\x01")

ReinstallSystem1 = ReinstallSystem("10.0.1.123",48281,b"0123456789abcdef")
DiskLetter = ReinstallSystem1.CreateRecoverVolume(2048)# MB
ReinstallSystem1.CopyPEFile("Files\\WinPEAMD64.7z.file",DiskLetter)
ReinstallSystem1.BootFromPE(DiskLetter)