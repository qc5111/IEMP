from django.db import models

# Create your models here.
from django.utils import timezone


class Users(models.Model):
    UserName = models.CharField(max_length=32, primary_key=True)
    Password = models.CharField(max_length=40)


class Machine(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=16)
    IP = models.CharField(max_length=15)
    MAC = models.CharField(max_length=12)
    Password = models.CharField(max_length=32, default="30313233343536373839616263646566")
    Type = models.IntegerField()  # DeviceType
    User = models.CharField(max_length=16)  # Device user or owner
    Status = models.IntegerField(default=0)
    LastUpdateTime = models.DateTimeField(default=timezone.now)  # TimeStamp


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
