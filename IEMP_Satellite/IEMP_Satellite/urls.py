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
# from django.contrib import admin
from django.urls import path
from . import index
from . import SystemOperation
from . import BitTorrent
from . import explorer
from . import ajax
from . import test
urlpatterns = [
    path('', index.index),
    path('index', index.index),
    path('SystemOperation/TurnOn', SystemOperation.TurnOn),
    path('SystemOperation/TurnOff', SystemOperation.TurnOff),
    path('announce', BitTorrent.announce),
    path('explorer', explorer.explorer),
    path('GetFileList', ajax.GetFileList),
    path('RPC', BitTorrent.test),
    path('Test', test.test),
]
