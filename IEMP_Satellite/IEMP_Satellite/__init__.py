

import pymysql
from IEMP_Satellite.Client2Server import Client2Server
from . import EventReg

pymysql.install_as_MySQLdb()

Client2Server('127.0.0.1', 48289, b'\x00\x00\x00\x00')



