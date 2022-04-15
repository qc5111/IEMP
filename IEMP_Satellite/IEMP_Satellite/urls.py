"""IEMP_Satellite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import index
from . import SystemOperation
from . import BitTorrent
from . import explorer
from . import ajax
from . import test
from . import DeployInterface
from . import console
from .SoftInit import SoftInit

SoftInit()

urlpatterns = [
    path('', index.index),
    path('index', index.index),
    path('SystemOperation/TurnOn', SystemOperation.TurnOn),
    path('SystemOperation/TurnOff', SystemOperation.TurnOff),
    path('console', console.console),
    path('consolews', console.Test),
    path('Tracker', BitTorrent.Tracker),
    path('TorrentManagement', BitTorrent.TorrentManagement),
    path('AjaxGetTorrentList', BitTorrent.AjaxGetTorrentList),
    path('TorrentOP', BitTorrent.TorrentOP),
    path('UploadFile', BitTorrent.UploadFile),
    path('TorrentDownload', BitTorrent.TorrentDownload),
    path('CreateBT', BitTorrent.CreateBT),


    path('AddTorrent', BitTorrent.AddTorrent),
    path('explorer', explorer.explorer),
    path('GetFileList', ajax.GetFileList),


    path('GetRSAPubKey', DeployInterface.GetRSAPubKey),
    path('RegNewDevice', DeployInterface.RegNewDevice),
    path('Test', test.test),

]
