#include <windows.h>
#include <stdio.h>


char * RegReadSZ(HKEY RootKey,char * Path, char * Key, int *ret){
    HKEY hKey;
    char *Data;
    DWORD Datalen;
    DWORD Type = REG_SZ;
    Data = (char *)malloc(128);
    Datalen = 128;
    *ret = RegGetValueA(RootKey,Path,Key,RRF_RT_ANY,&Type,Data,&Datalen);
    if(*ret == 234){
        free(Data);
        Data = (char *)malloc(Datalen);
        *ret = RegGetValueA(RootKey,Path,Key,RRF_RT_ANY,&Type,Data,&Datalen);
    }
    return Data;
}

long long int RegReadllInt(HKEY RootKey,char * Path, char * Key, int *ret){
    HKEY hKey;
    long long int Data;
    DWORD Datalen = 8;
    DWORD Type = REG_QWORD;
    *ret = RegGetValueA(RootKey,Path,Key,RRF_RT_ANY,&Type,&Data,&Datalen);
    return Data;
}


/*int main(){
    int ret;
    //char *Data = RegReadSZ(HKEY_CURRENT_USER,"Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Shell Folders","Desktop",&ret);
    char *Data = RegReadSZ(HKEY_LOCAL_MACHINE,"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion","ProductName",&ret);
    printf("ret:%d,Datalen:%d,Data:%s",ret,strlen(Data),Data);
    //unsigned long long int Data = RegReadllInt(HKEY_LOCAL_MACHINE,"Software\\Microsoft\\Windows\\CurrentVersion\\Run","test",&ret);
    //printf("ret:%d,Data:%llu",ret,Data);
}*/