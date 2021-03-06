#include "RegOprations.cpp"
long long int Filetime2Int64(const FILETIME &ftime)
{
    LARGE_INTEGER li;
    li.LowPart = ftime.dwLowDateTime;
    li.HighPart = ftime.dwHighDateTime;
    return li.QuadPart;
}
 
long long int CompareFileTime2(const FILETIME &preTime, const FILETIME &nowTime)
{
    return Filetime2Int64(nowTime) - Filetime2Int64(preTime);
}

int AddStringInfo(char * SendData,int SendLen,HKEY RootKey,char * Path,char * Key){
    char * RegData;
    int ret;
    int i;
    RegData = RegReadSZ(RootKey,Path,Key,&ret);
    //printf("ret:%d\n",ret);
    if(ret == 0){
        for(i=strlen(RegData)-1;i>4;i--){
            //printf("RegData[i]:%d",RegData[i]);
            if(RegData[i]!=0x20){
                break;
            }
            RegData[i] = 0;
        }
        SendData[SendLen] = strlen(RegData);
        //printf("SendLen:%d,RegData[SendLen]:%d\n",SendLen,RegData[SendLen]);
        SendLen++;

        memcpy(SendData+SendLen,RegData,SendData[SendLen-1]);
        SendLen+=SendData[SendLen-1];

    }else{
        SendData[SendLen] = 6;
        SendLen++;
        memcpy(SendData+SendLen,"Unknow",6);
        SendLen+=6;
    }
    //SendData[SendLen] = 0;
    
    free(RegData);
    return SendLen;
}

class HeartBeat{
private:
    char Status = 0;
    int SleepTime;
    pthread_t ThreadMainServer;

public:
    static void* MainServer(void *ClassName){
        HeartBeat *p=(HeartBeat *)ClassName;
        //变量声明
        char * SendData;
        int SendLen=0;
        MEMORYSTATUSEX memStatus;
        FILETIME preIdleTime;
        FILETIME preKernelTime;
        FILETIME preUserTime;
        FILETIME idleTime;
        FILETIME kernelTime;
        FILETIME userTime;
        long long int idle,kernel,user;
        SYSTEM_INFO si;
        float Result;

        SendData = (char *)malloc(1024);
        SendData[0] = 0;//初始化事件
        SendLen++;
        memcpy(SendData+SendLen,EID,4);
        SendLen += 4;
        memcpy(SendData+SendLen,&Version,4);//版本号
        SendLen += 4;
        memStatus.dwLength = sizeof(memStatus);
        GlobalMemoryStatusEx(&memStatus);
        //printf("memStatus.ullTotalPhys:%lld\n",memStatus.ullTotalPhys);

        memcpy(SendData+SendLen,&memStatus.ullTotalPhys,8);
        SendLen += 8;
        GetSystemInfo(&si);
        memcpy(SendData+SendLen,&si.dwNumberOfProcessors,2);
        SendLen += 2;
        SendLen = AddStringInfo(SendData,SendLen,HKEY_LOCAL_MACHINE,(char*)"HARDWARE\\DESCRIPTION\\System\\BIOS",(char*)"BaseBoardProduct");//MotherBoardName
        SendLen = AddStringInfo(SendData,SendLen,HKEY_LOCAL_MACHINE,(char*)"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion",(char*)"ProductName");//WindowsVersion
        SendLen = AddStringInfo(SendData,SendLen,HKEY_LOCAL_MACHINE,(char*)"HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0",(char*)"ProcessorNameString");//CPUName123

        UDP.SendData(SendData,SendLen);
        free(SendData);
        SendData = (char *)malloc(13);
        SendData[0] = 1;//心跳事件
        memcpy(SendData+1,EID,4);
        GetSystemTimes(&preIdleTime, &preKernelTime, &preUserTime);
        while(true){
            Sleep(p->SleepTime);//120s
            if(p->Status == 0){
                return 0;
            }
            GetSystemTimes(&idleTime, &kernelTime, &userTime);
            idle = CompareFileTime2(preIdleTime, idleTime);
            kernel = CompareFileTime2(preKernelTime, kernelTime);
            user = CompareFileTime2(preUserTime, userTime);
            preIdleTime = idleTime;
            preKernelTime = kernelTime;
            preUserTime = userTime;
            if (kernel + user == 0)
                Result = 0;
            Result = 1.0*(kernel + user - idle) / (kernel + user);
            //printf("Result:%lf%\n",Result*100);

            GlobalMemoryStatusEx(&memStatus);
            memcpy(SendData+5,&Result,4);
            idle = (memStatus.ullTotalPhys-memStatus.ullAvailPhys)/1024/1024;
            memcpy(SendData+9,&idle,4);
            UDP.SendData(SendData,13);
        }
    }
    HeartBeat(int SleepTimeIn=120000){
        SleepTime = SleepTimeIn;

    }
    void start(){
        Status = 1;
        pthread_create(&ThreadMainServer,NULL,MainServer,(void *)this);
    }
    void close(){
        Status = 0;
    }

};
