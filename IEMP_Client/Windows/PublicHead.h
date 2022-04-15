#ifndef IncludeHeaders
#define IncludeHeaders
#include <winsock2.h>
#include <windows.h>
#include <stdio.h>
#include <pthread.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <dirent.h>
#include <cstdlib>
#include<time.h>
#pragma comment(lib,"ws2_32.lib")
//全局变量
int Version = 002; //0.0.2
static int GLOBAL_TIME_DIFF;
char EID[4];//EquipmentID
unsigned char Configs[32];
//本地程序
#include "md5.h"
#include "md5.c"
#include "zlib.h"
#include "gzip.cpp"
#include "FileOP.cpp"
#include "DynamicPassword.c"
#include "RemoteCMD.cpp"
RemoteCMD RemoteCMD;
#include "UDP.cpp"
UDP UDP;
#include "CMDProc.cpp"
#include "PerformanceMonitor.cpp"
#include "HeartBeat.cpp"
HeartBeat HeartBeat;
#include "TCPServer.cpp"
TcpServer TcpServer;
#endif
