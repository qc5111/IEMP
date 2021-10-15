from IEMP_Satellite.Function.ReinstallSystem import ReinstallSystem

from django.http import HttpResponse

from IEMP_Satellite.settings import DefaultFilePath


def test(request):
    # return HttpResponse(DefaultFilePath)
    ReinstallSystem1 = ReinstallSystem("10.0.1.123", 48281, b"0123456789abcdef")
    DiskLetter = ReinstallSystem1.CreateRecoverVolume(2048)  # MB
    ReinstallSystem1.CopyPEFile("WinPEAMD64.7z.file", DiskLetter)
    ReinstallSystem1.BootFromPE(DiskLetter)
    return HttpResponse("OK")
