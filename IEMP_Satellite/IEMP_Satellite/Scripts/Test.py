import time

from IEMP_Satellite import BitTorrent
from IEMP_Satellite.EventReg import RegisterEvent
from IEMP_Satellite.Function.DiskOP import DiskOP
from IEMP_Satellite.Function.OrderSendToClient import Client
import MainDB.models as DB
from IEMP_Satellite.Function.pipe import RemotePipe

WimName = "Windows-Test-System.wim"


#@RegisterEvent("EquipmentOnline")
def Test(Machine):
    Client1 = Client(Machine)
    if Client1.OPSystem == 3:  # 判断系统为WinPE
        # 写入数据库
        Machine.Type = 0
        Machine.Status = 4  # 0不在线，1在线，2繁忙，3未知，4 PE初次连接
        Machine.save()
        DiskOP1 = DiskOP(Machine)
        SmallestDisk = DiskOP1.GetSmallestDisk()
        DiskOP1.SelectDisk("ID", SmallestDisk['ID'])
        DiskOP1.CleanDisk()
        DiskOP1.ConvertGPT()
        DiskInfoList = [
            {"PartitionType": "efi", "Size": 512, "Format": "FAT32", "BestLetter": "Y", "label": "EFI", "quick": True},
            {"PartitionType": "Primary", "Size": 30 * 1024, "Format": "NTFS", "BestLetter": "C", "label": "System",
             "quick": True},
            {"PartitionType": "Primary", "Size": 0, "Format": "NTFS", "BestLetter": "D", "label": "Data", "quick": True}
        ]
        EFI, System, Data = DiskOP1.OneKeyCeateMultiPartition(DiskInfoList)
        Client1.InitAria2c("%s:\\Download" % Data)
        BitTorrent.CreateDownload(Machine.IP,
                                  BitTorrent.GetInfoHashFromFileName(WimName))
        # 文件发送完成后根据事件信息调用系统
    # Client1.InitAria2c()
    # BitTorrent.CreateDownload(Machine.IP, BitTorrent.GetInfoHashFromFileName("Win11_EnglishInternational_x64v1.wim"))


#@RegisterEvent("BTDownloadComplete")
def Test2(IP, info_hash):
    try:
        Machine = DB.NoEIDMachine.objects.get(IP=IP)
    except DB.NoEIDMachine.DoesNotExist:
        return
    Machine.Type = 0
    Machine.Status = 5  # 0不在线，1在线，2繁忙，3未知，4 PE初次连接，5 PE第二次连接，6 已启动到Windows
    Machine.save()
    Client1 = Client(Machine)
    # 安装操作系统
    WimPath = BitTorrent.GetRemotePathFromInfoHash(IP, info_hash).replace("/", "\\")

    Client1.SendOneCMDOrder("Dism /Apply-Image /ImageFile:\"%s\" /Index:%s /ApplyDir:%s" % (WimPath, 1, "C:\\"))
    Client1.SendOneCMDOrder("Bcdboot C:\\Windows /s Y: /f UEFI")
    Client1.SendOneCMDOrder("start wpeutil reboot")


#@RegisterEvent("EquipmentOnline")
def Win11Online(Machine):
    Client1 = Client(Machine)
    if Client1.OPSystem == 0:  # 判断系统为Windows
        # 写入数据库
        Machine.Type = 0
        Machine.Status = 6  # 0不在线，1在线，2繁忙，3未知，4 PE初次连接，5 PE第二次连接，6 已启动到Windows
        Machine.save()
        Client1.SendFile("winget.appx","Temp\\winget.appx")
        Client1.SendFile("winget-depend.appx", "Temp\\winget-depend.appx")
        Client1.SendOneCMDOrder("powershell Add-AppxPackage -Path C:\\IEMP\\Temp\\winget-depend.appx")
        Client1.SendOneCMDOrder("powershell Add-AppxPackage -Path C:\\IEMP\\Temp\\winget.appx")
        #Pipe1 = RemotePipe(Machine,"cmd.exe")
        #Pipe1.AutoExec("winget install Google.Chrome\nY")
        #Pipe1.close()
        Client1.SendOneCMDOrder("winget install Google.Chrome")
        Client1.SendOneCMDOrder("winget install Python.Python.3")
        Client1.SendOneCMDOrder("winget install Notepad++.Notepad++")