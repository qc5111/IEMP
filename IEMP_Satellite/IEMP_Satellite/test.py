import base64

from IEMP_Satellite.Function.ReinstallSystem import ReinstallSystem

from django.http import HttpResponse

from .Function import OrderSendToClient, RSA


def test(request):
    # OrderSendToClient1 = OrderSendToClient.WinClient("10.0.1.214", b"0123456789abcdef")
    # OrderSendToClient1 = OrderSendToClient.WinClient("10.0.1.123", b"0123456789abcdef")
    # OrderSendToClient1.SelfRenew("IEMP_Client_Latest.exe")
    # Data1 = RSA.RSAEncrypt(b"Test")
    # print(Data1)
    # OrderSendToClient1.StartNewProcess("notepad.exe")
    # OrderSendToClient1.ExitIEMP()
    # OrderSendToClient1.SendOneCMDOrder('dumpsys location|grep "Location\\[" > test.log')
    # OrderSendToClient1.SendOneCMDOrder('start adbd')
    # OrderSendToClient1.SendOneCMDOrder('reboot fastboot')
    # print(Data1)
    Data = "knYRitLjTdi5z/Qi8dLTMopA8DZB3Z7/+E6X5dhWmeiUPjX3MQBh/CQm0pU/Sz4uoVwUkeUaJz/aVWPI4WnxcAiEdgQkJfbNKlJwzZ6bITGHbB4hpXMQN2yXlm4VvxPuJVY31I1I51B3guq232Nk1yqfhyGEKn9sSt0KkKezm/HAiYDP6LSgzXJFfQ4Gu2FPXi2r6IHAqetKwIuarIqLA5umPCM43H9hrb5V/8PWTsULdDeF8uTTLMCvv0M86zMxFIE0zl7ImdammYhF2TeDviplJBvjIRzDqrmJIGYrU6jyBM8XkbRnW+YNcB82ks2p5YpWF2tnNB5mJN542KZK7A=="
    Data = base64.b64decode(Data)
    print(Data)
    Data2 = RSA.RSADecrypt(Data)
    print(Data2)
    # print(len(Data2),Data2)
    return HttpResponse("OK")

    # return HttpResponse(DefaultFilePath)

    # ReinstallSystem1 = ReinstallSystem("10.0.1.123", 48281, b"0123456789abcdef")
    # DiskLetter = ReinstallSystem1.CreateRecoverVolume(2048)  # MB
    # ReinstallSystem1.CopyPEFile("WinPEAMD64.7z.file", DiskLetter)
    # ReinstallSystem1.BootFromPE(DiskLetter)
    # return HttpResponse("OK")
