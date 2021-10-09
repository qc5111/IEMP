#include "RegOprations.cpp"
int AddStringInfo(char * SendData,int SendLen,HKEY RootKey,char * Path,char * Key){
    char * RegData;
    int ret;
    int i;
    RegData = RegReadSZ(RootKey,Path,Key,&ret);
    if(ret == 0){
        memcpy(SendData+SendLen,RegData,strlen(RegData));
        SendLen+=strlen(RegData);
        for(i=strlen(RegData)-1;i>4;i--){
            //printf("RegData[i]:%d",RegData[i]);
            if(RegData[i]!=0x20){
                break;
            }
            SendLen--;
        }
    }else{
        memcpy(SendData+SendLen,"Unknow",6);
    }
    SendData[SendLen] = 0;
    SendLen++;
    free(RegData);
    return SendLen;
}
void* HeartBeat(void* args){
    char * SendData;
    int SendLen=0;
    MEMORYSTATUSEX memStatus;
    
    SendData = (char *)malloc(1024);
    memcpy(SendData+SendLen,EID,4);
    SendLen += 4;
    memStatus.dwLength = sizeof(memStatus);
    GlobalMemoryStatusEx(&memStatus);
    printf("memStatus.ullTotalPhys:%lld\n",memStatus.ullTotalPhys);
    
    memcpy(SendData+SendLen,&memStatus.ullTotalPhys,8);
    SendLen += 8;
    SendLen = AddStringInfo(SendData,SendLen,HKEY_LOCAL_MACHINE,(char*)"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion",(char*)"ProductName");
    SendLen = AddStringInfo(SendData,SendLen,HKEY_LOCAL_MACHINE,(char*)"HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0",(char*)"ProcessorNameString");
    
    UDP.SendData(SendData,SendLen);
    free(SendData);
    while(true){



        

        
        
        Sleep(10000);
    }
}