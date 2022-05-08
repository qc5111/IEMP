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
from . import test
from . import DeployInterface
from . import console
from .SoftInit import SoftInit
from . import Authorization

SoftInit()

urlpatterns = [
    path('', index.index),
    path('index', index.index),
    path('SystemOperation/TurnOn', SystemOperation.TurnOn),
    path('SystemOperation/TurnOff', SystemOperation.TurnOff),
    path('console', console.console),
    # 种子操作
    path('Tracker', BitTorrent.Tracker),  # 无须授权
    path('TorrentManagement', BitTorrent.TorrentManagement),
    path('AjaxGetTorrentList', BitTorrent.AjaxGetTorrentList),
    path('TorrentOP', BitTorrent.TorrentOP),
    path('UploadFile', BitTorrent.UploadFile),
    path('TorrentDownload', BitTorrent.TorrentDownload),
    path('CreateBT', BitTorrent.CreateBT),
    path('AddTorrent', BitTorrent.AddTorrent),
    # 授权管理
    path('Login', Authorization.Login),  # 无须授权
    path('AjaxLogin', Authorization.AjaxLogin),  # 无须授权
    path('Logout', Authorization.Logout),  # 无须授权

    # 文件管理
    path('explorer', explorer.explorer),
    path('GetFileList', explorer.GetFileList),

    path('GetRSAPubKey', DeployInterface.GetRSAPubKey),  # 无须授权
    path('RegNewDevice', DeployInterface.RegNewDevice),  # 无须授权
    path('Test', test.test),  # 无须授权

]
