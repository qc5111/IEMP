import time
import zlib
from socket import *
from . import DynamicPassword
import os
import struct
import MainDB.models as DB
import datetime


class Client:
    CPUArch = ""
    RootPath = ""
    Encoding = ""
    Slash = "/"

    def __init__(self, Machine):
        self.Machine = Machine
        self.OPSystem = -1  # 0 Windows 1 Linux 2 Android 3 Windows PE 4 Openwrt
        self.IsLinux = True
        # 系统类型判断
        if self.Machine.OPSystem > 0:  # 通过部署器获取的系统类型判断 0 Windows 1 Linux 2 Android
            self.OPSystem = self.Machine.OPSystem
        else:
            if "windows" in self.Machine.OPSystemName.lower():  # Windows系
                if "Preinstallation Environment" in self.Machine.OPSystemName:  # Windows PE
                    self.OPSystem = 3
                else:
                    self.OPSystem = 0  # Windows
            # Linux部署未添加
            if "linux" in self.Machine.OPSystemName.lower():  # Linux系
                self.OPSystem = 1
            if "wrt" in self.Machine.OPSystemName.lower():  # Openwrt系
                self.OPSystem = 4
        if self.OPSystem == 0:  # Windows
            self.RootPath = "C:\\IEMP\\"
            self.Encoding = "GB2312"
            self.IsLinux = False
            self.Slash = "\\"
        elif self.OPSystem == 1:  # Linux
            self.RootPath = "/opt/IEMP/"
            self.Encoding = "UTF-8"
        elif self.OPSystem == 2:  # Android
            self.RootPath = "/sdcard/IEMP/"
            self.Encoding = "UTF-8"
        elif self.OPSystem == 3:  # Windows PE
            self.RootPath = "X:\\IEMP\\"
            self.Encoding = "GB2312"
            self.IsLinux = False
            self.Slash = "\\"
        elif self.OPSystem == 4:  # Openwrt
            self.RootPath = "/opt/IEMP/"
            self.Encoding = "UTF-8"
        self.BaseFilePath = DB.SateliteInfo.objects.get(Name="FileStoragePath").Value + "/"

    def NormalOrderSend(self, Order):
        tcp_client_socket = socket(AF_INET, SOCK_STREAM)
        tcp_client_socket.connect((self.Machine.IP, 48280))
        code = DynamicPassword.DynamicPassword(self.Machine.Password, 8)
        tcp_client_socket.send(struct.pack('<I', len(Order) + 8)[:2])
        tcp_client_socket.send(code + Order)
        return tcp_client_socket

    def EnsureRemoteDir(self, RemotePath):
        if self.IsLinux:
            self.SendOneCMDOrder("mkdir -p " + RemotePath[:RemotePath.rfind("/")])
        else:
            self.SendOneCMDOrder("mkdir " + RemotePath[:RemotePath.rfind("\\")])

    def SendFile(self, FilePath, RemoteRelativelyPath, RawData=b"", IsAbsolutePath=False):
        if not IsAbsolutePath:
            FilePath = self.BaseFilePath + FilePath
        # 创建目录
        RemotePath = self.RootPath + RemoteRelativelyPath
        self.EnsureRemoteDir(RemotePath)
        if not RawData:
            FileSize = os.path.getsize(FilePath)
        else:
            FileSize = len(RawData)

        # 初始化发送文件，传输文件大小，文件名
        tcp_client_socket = self.NormalOrderSend(
            b'\x01\x00' + RemotePath.encode(self.Encoding) + b"\x00" + struct.pack('<Q', FileSize))
        tcp_client_socket.recv(1)
        if not RawData:
            fr = open(FilePath, "rb")

            while True:
                FileData = fr.read(1024)
                if not FileData:
                    break
                tcp_client_socket.send(FileData)
            fr.close()
        else:
            tcp_client_socket.send(RawData)

        tcp_client_socket.close()

    def SendOneCMDOrder(self, order):
        self.NormalOrderSend(b'\x00\x06' + order.encode(self.Encoding))

    def ExecMultipleOrder(self, orders):
        fw = open("Files/order.temp.file", "wb")
        for i in orders:
            fw.write((i + "\n").encode(self.Encoding))
        fw.close()
        if self.IsLinux:
            self.SendFile("Files/order.temp.file", "Temp/order.sh")
            self.SendOneCMDOrder("sh Temp/order.sh")
        else:
            self.SendFileToIEMPRoot("Files/order.temp.file", 'Temp/order.bat')
            self.SendOneCMDOrder('"Temp\\order.bat"')

    def StartNewProcess(self, order):
        self.NormalOrderSend(b'\x00\x08' + order.encode(self.Encoding))

    def ExitIEMP(self):
        self.NormalOrderSend(b"\x02\x00")

    def SelfRenew(self):  # 只写了Windows
        RenewScript = 'set ws=WScript.CreateObject("WScript.Shell")\n' \
                      + 'wscript.sleep 500\n' \
                      + 'Dim Fso,shell\n' \
                      + 'Set Fso = WScript.CreateObject("Scripting.FileSystemObject")\n' \
                      + 'Set shell = Wscript.createobject("wscript.shell")\n' \
                      + 'Fso.DeleteFile"Update.vbs"\n' \
                      + 'Fso.DeleteFile"IEMP_Client.exe"\n' \
                      + 'Fso.MoveFile"IEMP_ClientNew.exe","IEMP_Client.exe"\n' \
                      + 'shell.run "IEMP_Client.exe"\n'
        self.SendFile("IEMP/IEMP.Windows.exe.file", "IEMP_ClientNew.exe")
        self.NormalOrderSend(b'\x02\x01' + b"IEMP_ClientNew.exe" + b'\x00' + RenewScript.encode(self.Encoding))

    def GetFileList(self, Path):
        tcp_client_socket = self.NormalOrderSend(b'\x01\x02' + Path.encode(self.Encoding))
        Data = ""
        ByteArr = []
        while Data != b"":
            Data = tcp_client_socket.recv(1024)
            ByteArr.append(Data)
        data = b"".join(ByteArr)
        if data == b"00":
            return []
        FileList = zlib.decompress(data)
        FileDictArr = []
        Pos = 0
        MaxPos = len(FileList)
        while True:
            if Pos == MaxPos:
                return FileDictArr
            if FileList[Pos] == 4:
                Mtime = struct.unpack("<I", FileList[Pos + 1:Pos + 5])[0]
                Pos += 4
                FileDictArr.append(
                    {"Type": 4, "Name": FileList[Pos + 2:Pos + 2 + FileList[Pos + 1]].decode(self.Encoding),
                     "Mtime": Mtime})
                Pos += FileList[Pos + 1] + 2
            elif FileList[Pos] == 8:
                Mtime = struct.unpack("<I", FileList[Pos + 1:Pos + 5])[0]
                Pos += 4
                Size = \
                    struct.unpack("<Q",
                                  FileList[Pos + 2:Pos + 1 + FileList[Pos + 1]] + b"\x00" * (9 - FileList[Pos + 1]))[
                        0]
                Pos += FileList[Pos + 1]
                FileDictArr.append(
                    {"Type": 8, "Name": FileList[Pos + 2:Pos + 2 + FileList[Pos + 1]].decode(self.Encoding),
                     "Mtime": Mtime, "Size": Size})
                Pos += FileList[Pos + 1] + 2
            elif FileList[Pos] > 128:
                FileDictArr.append(
                    {"Type": FileList[Pos],
                     "Name": FileList[Pos + 2:Pos + 2 + FileList[Pos + 1]].decode(self.Encoding)})
                Pos += FileList[Pos + 1] + 2

    def InitAria2c(self, DownloadPath=""):
        if DownloadPath == "":
            DownloadPath = self.RootPath + "Download"
        if self.IsLinux:
            System = "Linux"
            # 获取CPU架构
            if "x86_64" in self.Machine.OPSystemName:
                self.CPUArch = "x86_64"
            elif "aarch64" in self.Machine.OPSystemName:
                self.CPUArch = "aarch64"
            Suffix = ""
        else:
            System = "Windows"
            self.CPUArch = "AMD64"
            Suffix = ".exe"
        Aria2cRootPath = "Tools" + self.Slash + "Aria2c" + self.Slash
        Aria2cName = 'aria2c' + '-' + System.lower() + '-' + self.CPUArch.lower()
        Aria2Structure = self.GetFileList(self.RootPath + "Tools" + self.Slash + "Aria2c")
        FileComplete = {"Executable": False, "Session": False, "Config": False, "VBS": False}
        for i in Aria2Structure:
            if i["Name"] == Aria2cName + Suffix:
                if os.stat(self.BaseFilePath + "Aria2c/" + Aria2cName + Suffix) == i["Size"]:
                    FileComplete["Executable"] = True
            elif i["Name"] == "aria2.session":
                FileComplete["Session"] = True
            elif i["Name"] == "aria2.conf":
                FileComplete["Config"] = True
            elif i["Name"] == "Start.vbs":
                FileComplete["VBS"] = True

        if not FileComplete["Executable"]:
            self.SendFile("Aria2c/" + Aria2cName + Suffix, Aria2cRootPath + Aria2cName + Suffix)
        if not FileComplete["Session"]:
            if self.IsLinux:
                self.SendOneCMDOrder(
                    "touch " + self.RootPath + Aria2cRootPath + "aria2.session")
            else:
                self.SendOneCMDOrder(
                    "copy nul " + self.RootPath + Aria2cRootPath + "aria2.session")
        if not FileComplete["Config"]:
            Fr = open(self.BaseFilePath + 'Aria2c/aria2-template.conf', 'r')
            ConfTemplate = Fr.read()
            Fr.close()
            ConfTemplate = ConfTemplate.replace('{{BasePath}}', DownloadPath)
            ConfTemplate = ConfTemplate.replace('{{Aria2cDir}}',
                                                self.RootPath + Aria2cRootPath)
            self.SendFile("", Aria2cRootPath + "aria2.conf", ConfTemplate.encode("utf-8"))
        if not self.IsLinux and not FileComplete["VBS"]:
            VBS = 'CreateObject("WScript.Shell").Run "%s --conf-path=%saria2.conf",0,True' % (self.RootPath + Aria2cRootPath + Aria2cName, self.RootPath + Aria2cRootPath)
            self.SendFile("", Aria2cRootPath + "Start.vbs", VBS.encode(self.Encoding))
        if self.IsLinux:
            self.SendOneCMDOrder("chmod +x " + self.RootPath + Aria2cRootPath + Aria2cName)
            self.SendOneCMDOrder(self.RootPath + Aria2cRootPath + Aria2cName + " --conf-path=" + self.RootPath + Aria2cRootPath + "aria2.conf")
        else:
            if self.OPSystem == 0: #Windows
                self.SendOneCMDOrder(self.RootPath + Aria2cRootPath + "Start.vbs")
            elif self.OPSystem == 3: #WinPE
                self.StartNewProcess(self.RootPath + Aria2cRootPath + Aria2cName + " --conf-path=" + self.RootPath + Aria2cRootPath + "aria2.conf")

    def Init7zip(self):  # 初始化7zip，只写了Windows
        # self.NormalOrderSend(b'\x00\x06' + ('mkdir "%sTools\\"' % self.RootPath).encode(self.Encoding))
        self.SendOneCMDOrder('mkdir "%sTools\\"' % self.RootPath)
        # self.SendFile("Files\\7za.exe.file", "%sTools\\7za.exe" % self.RootPath)
        self.SendFileToIEMPRoot("7za.exe.file", "Tools\\7za.exe")

    def InitPython(self):  # 初始化Python，只写了Windows
        # self.NormalOrderSend(b'\x00\x06' + ('mkdir "%sTemp\\"' % self.RootPath).encode(self.Encoding))
        self.SendOneCMDOrder('mkdir "%sTemp\\"' % self.RootPath)
        # self.SendFile("Files\\python39.run.7z.file", "%sTemp\\python39.run.7z" % self.RootPath)
        self.SendFileToIEMPRoot("Files\\python39.run.7z.file", "Temp\\python39.run.7z")
        self.ExecMultipleOrder(['"%sTools\\7za.exe" x "%sTemp\\python39.run.7z" -r -aoa -o"%sTools"' % (
            self.RootPath, self.RootPath, self.RootPath)])
        # self.SendFile("Files\\python39.lib.zip.file", "%sTools\\python\\python39.zip" % self.RootPath)
        self.SendFileToIEMPRoot("Files\\python39.lib.zip.file", "Tools\\python\\python39.zip")
