from django.db import models

# Create your models here.
from django.utils import timezone


class SateliteInfo(models.Model):
    Name = models.CharField(max_length=32, primary_key=True)
    Value = models.TextField(max_length=256)


class Users(models.Model):
    UserName = models.CharField(max_length=32, primary_key=True)
    Password = models.CharField(max_length=40)


class MachineAbstract(models.Model):
    Name = models.CharField(max_length=64)
    OPSystem = models.IntegerField(default=-1)  # 0 Windows 1 Linux 2 Android
    CPUArch = models.CharField(max_length=8, default="")
    OPSystemName = models.CharField(max_length=64, default="")
    IP = models.CharField(max_length=15)  # 自动生成
    Password = models.CharField(max_length=32, default="30313233343536373839616263646566")
    RootUsername = models.CharField(max_length=32, default="root")
    RootPassword = models.CharField(max_length=40, default="")
    Type = models.IntegerField()  # DeviceType # DeviceType # 设备类型 0电脑 1手机 2服务器 3路由器 4未知
    # User = models.CharField(max_length=16)  # Device user or owner
    Status = models.IntegerField(default=-1)  # 0不在线，1在线，2繁忙，3未知
    # Encoding = models.CharField(max_length=16, default="UTF-8")  # 编码
    LastUpdateTime = models.IntegerField(default=-1)  # TimeStamp
    TotalMemory = models.BigIntegerField(default=-1)
    Cores = models.IntegerField(default=-1)
    MotherBoardName = models.CharField(max_length=64, default="")
    CPUName = models.CharField(max_length=64, default="")
    UsingMemory = models.IntegerField(default=-1)
    UsingCPU = models.IntegerField(default=-1)  # 最大10000,输出时除以10000%
    Version = models.IntegerField(default=-1)

    def __unicode__(self):
        return self.title

    class Meta:
        abstract = True


class Machine(MachineAbstract):
    ID = models.AutoField(primary_key=True)
    MAC = models.CharField(max_length=12)  # 自动生成
    pass


class NoEIDMachine(MachineAbstract):
    MAC = models.CharField(max_length=12, primary_key=True)  # 自动生成


class TorrentList(models.Model):
    info_hash = models.CharField(max_length=40, primary_key=True)
    FileName = models.CharField(max_length=64, default="")
    FileSize = models.BigIntegerField(default=0)
    Status = models.IntegerField(default=0)  # 0正在做种，1文件完整，2文件损坏，3文件缺失，4正在检查
    AutoSeeding = models.BooleanField(default=False)
    UpdateTime = models.IntegerField(default=0)  # TimeStamp


class TrackerClientList(models.Model):
    peer_id = models.CharField(max_length=40, primary_key=True)
    IPAndPort = models.CharField(max_length=12)
    TotalUploaded = models.IntegerField(default=0)
    TotalDownloaded = models.IntegerField(default=0)
    key = models.CharField(max_length=16, default="")


class TorrentRunningList(models.Model):
    info_hash = models.CharField(max_length=40)
    peer_id = models.CharField(max_length=40)
    IPAndPort = models.CharField(max_length=12)
    left = models.BigIntegerField(default=0)
    Status = models.IntegerField()  # 0:stopped, 1:downloading, 2:seeding
    unique_together = (('info_hash', 'peer_id'),)
    LastUpdateTime = models.IntegerField(default=0)  # TimeStamp
