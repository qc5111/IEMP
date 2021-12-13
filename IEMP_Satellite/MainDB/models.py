from django.db import models

# Create your models here.
from django.utils import timezone


class SateliteInfo(models.Model):
    Name = models.CharField(max_length=32, primary_key=True)
    Value = models.TextField(max_length=256)


class Users(models.Model):
    UserName = models.CharField(max_length=32, primary_key=True)
    Password = models.CharField(max_length=40)


class Machine(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=64)
    OPSystem = models.IntegerField(default=0)  # 0 Windows 1 Linux 2 Android
    CPUArch = models.CharField(max_length=8, default="")
    OPSystemName = models.CharField(max_length=64, default="")
    IP = models.CharField(max_length=15)  # 自动生成
    MAC = models.CharField(max_length=12)  # 自动生成
    Password = models.CharField(max_length=32, default="30313233343536373839616263646566")

    Type = models.IntegerField()  # DeviceType # 操作系统类型
    # User = models.CharField(max_length=16)  # Device user or owner
    Status = models.IntegerField(default=0)  # 0不在线，1在线，2繁忙，3未知
    # Encoding = models.CharField(max_length=16, default="UTF-8")  # 编码
    LastUpdateTime = models.IntegerField(default=0)  # TimeStamp
    TotalMemory = models.BigIntegerField(default=0)
    Cores = models.IntegerField(default=0)
    MotherBoardName = models.CharField(max_length=64, default="")
    CPUName = models.CharField(max_length=64, default="")
    UsingMemory = models.IntegerField(default=0)
    UsingCPU = models.IntegerField(default=0)  # 最大10000,输出时除以10000%
    Version = models.IntegerField(default=-1)


class TorrentList(models.Model):
    info_hash = models.CharField(max_length=40, primary_key=True)
    HasTorrentFile = models.BooleanField()  # 是否有种子文件
    IsServerProvidesFiles = models.BooleanField()  # 服务器是否做种


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
    left = models.IntegerField()
    Status = models.IntegerField()  # 0:stopped, 1:downloading, 2:seeding
    unique_together = (('info_hash', 'peer_id'),)
