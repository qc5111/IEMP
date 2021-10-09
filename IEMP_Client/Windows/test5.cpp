#include <windows.h>
#include <stdio.h>
#include <time.h>
#include "dirent.h"

__int64 Filetime2Int64(const FILETIME &ftime)
{
    LARGE_INTEGER li;
    li.LowPart = ftime.dwLowDateTime;
    li.HighPart = ftime.dwHighDateTime;
    return li.QuadPart;
}
 
__int64 CompareFileTime2(const FILETIME &preTime, const FILETIME &nowTime)
{
    return Filetime2Int64(nowTime) - Filetime2Int64(preTime);
}


long long int GetMemoryFreeSize() {
    MEMORYSTATUSEX memStatus;
    memStatus.dwLength = sizeof(memStatus);
    
    GlobalMemoryStatusEx(&memStatus);
    long long int FreeMemory = memStatus.ullTotalPhys - memStatus.ullAvailPhys;
    return FreeMemory;
}
double getCpuUsage()
{
    FILETIME preIdleTime;
    FILETIME preKernelTime;
    FILETIME preUserTime;
    GetSystemTimes(&preIdleTime, &preKernelTime, &preUserTime);
 
    Sleep(1000);
 
    FILETIME idleTime;
    FILETIME kernelTime;
    FILETIME userTime;
    GetSystemTimes(&idleTime, &kernelTime, &userTime);
 
    auto idle = CompareFileTime2(preIdleTime, idleTime);
    auto kernel = CompareFileTime2(preKernelTime, kernelTime);
    auto user = CompareFileTime2(preUserTime, userTime);
 
    if (kernel + user == 0)
        return 0;
 
    return 1.0*(kernel + user - idle) / (kernel + user);
}

int main(){
    GetCPUTemp(1);
    double Testdouble,Memory;
    while (true){
        Testdouble = getCpuUsage();
        Memory = 1.0 * GetMemoryFreeSize() / 1024 / 1024 / 1024;
        printf("Testdouble:%llf%,",Testdouble*100);
        printf("GetMemoryFreeSize:%lf\n",Memory);
    }
    
    
}