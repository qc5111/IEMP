import time

from IEMP_Satellite import BitTorrent
from IEMP_Satellite.EventReg import RegisterEvent
from IEMP_Satellite.Function.OrderSendToClient import Client


@RegisterEvent("EquipmentOnline")
def Test(Machine):
    print(Machine.MAC)
    Client1 = Client(Machine)
    # Client1.InitAria2c()
    # BitTorrent.CreateDownload(Machine.IP, BitTorrent.GetInfoHashFromFileName("Win11_EnglishInternational_x64v1.wim"))


@RegisterEvent("BTDownloadComplete")
def Test2(Machine, Torrent):
    print(Machine, Torrent)
