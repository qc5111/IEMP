#include <windows.h>
#include <stdio.h>
int main(){
    PROCESS_INFORMATION pi;
    STARTUPINFO si;      //隐藏进程窗口
    si.cb = sizeof(STARTUPINFO);
    si.lpReserved = NULL;
    si.lpDesktop = NULL;
    si.lpTitle = NULL;
    //si.dwFlags = STARTF_USESHOWWINDOW;
    //si.wShowWindow = SW_HIDE;
    si.cbReserved2 = NULL;
    si.lpReserved2 = NULL;
    //"python.exe C:\\IEMP_Client\\PyScript\\test.py"
    BOOL ret = CreateProcess(NULL,"cmd.exe",NULL,NULL,FALSE,CREATE_NEW_CONSOLE,NULL,NULL,&si,&pi);
    //BOOL ret = CreateProcess("cmd.exe","",NULL,NULL,FALSE,0,NULL,NULL,&si,&pi);
    printf("%d",ret);
}
