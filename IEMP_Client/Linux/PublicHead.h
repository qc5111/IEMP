#ifndef IncludeHeaders
#define IncludeHeaders
#include <stdio.h>
#include <pthread.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <dirent.h>
#include <cstdlib>
#include <time.h>
#include <cstring>
#include <zlib.h>//apt install zlib1g-dev
//全局变量
static int GLOBAL_TIME_DIFF;
char EID[4];//EquipmentID
unsigned char Configs[32];//
//本地程序
#include "md5.h" //Pass
#include "md5.c" //Pass

#include "gzip.cpp"
//#include "FileOP.cpp"
#include "DynamicPassword.c" //Pass
//#include "RemoteCMD.cpp"
//RemoteCMD RemoteCMD;
#include "UDP.cpp" //Pass
UDP UDP;
//#include "CMDProc.cpp"
//#include "PerformanceMonitor.cpp"
#include "HeartBeat.cpp"
HeartBeat HeartBeat;
//#include "TCPServer.cpp"
//TcpServer TcpServer;
#endif
