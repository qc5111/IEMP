from django.http import HttpResponse
import socket
import binascii


def Wol(mac, ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    mac = mac.upper()
    ip = ip.split(':')
    if len(ip) == 1:
        ip.append("9")
    iPSpilt = ip[0].split(".")
    ip[0] = iPSpilt[0] + "." + iPSpilt[1] + "." + iPSpilt[2] + ".255"  # BroadCast
    mac = mac.replace(":", "")
    mac = mac.replace("-", "")
    s.sendto(binascii.unhexlify('FF' * 6 + mac * 16), (ip[0], int(ip[1])))
    s.close()


def WolWithDjango(request):
    Wol("244BFE56E6D2", "10.0.1.123")
    return HttpResponse("OK")
