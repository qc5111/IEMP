#include "PublicHead.h"
class TcpServer{
    private:
        SOCKET sClient;
        SOCKET slisten;
        pthread_t ThreadMainServer;
        char Status = 0;
    public:
        static void* MainServer(void *ClassName){
            TcpServer *p=(TcpServer *)ClassName;
            int revDatalen,DataLen;
            WSADATA wsaData;

            sockaddr_in sin;

            char *revData;
            WSAStartup(MAKEWORD(2,2), &wsaData);
            //创建套接字
            p->slisten = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
            //绑定IP和端口
            sin.sin_family = AF_INET;
            sin.sin_port = htons(48280);//Port
            sin.sin_addr.S_un.S_addr = INADDR_ANY;
            if (bind(p->slisten, (LPSOCKADDR)&sin, sizeof(sin)) == SOCKET_ERROR){
                printf("BindFail");
                return 0;
            }
            //开始监听
            listen(p->slisten, 5);
            //循环接收数据
            while (true){
                if(p->Status == 0){
                    printf("SystemStop\n");
                    break;
                }
                //等待连接
                p->sClient = accept(p->slisten, NULL, NULL);
                if(p->sClient == INVALID_SOCKET){continue;}
                revData = (char *)malloc(2);
                DataLen = recv(p->sClient, revData, 2, 0);
                if(DataLen == 0){continue;}
                DataLen = revData[0] + (revData[1] << 8);//struct.pack('<I', int)[:2]
                free(revData);
                revData = (char *)malloc(DataLen);//重新分配大小，最大为65535
                revDatalen = 0;//已收到的数据长度
                while(revDatalen != DataLen){
                    revDatalen += recv(p->sClient, revData+revDatalen, 128, 0);
                    if(DataLen == 0){
                        break;
                    }
                }
                if(revDatalen == 0){
                    continue;
                }
                //数据接受完毕，截断数据

                revData[revDatalen] = 0;
                if(CheckPassword((unsigned char*)revData,8)==0){//密码验证
                    //run command
                    CMDProc(revData+8,revDatalen-8,p->sClient);
                }else{
                    //告诉客户端密码错误
                    send(p->sClient, "ff", 2, 0);
                }
                closesocket(p->sClient);
            }
            return 0;
        }
    void start(){
        Status = 1;
        pthread_create(&ThreadMainServer, NULL, MainServer, (void *)this);

    }
    void close(){
        Status = 0;
        //closesocket(sClient);
        closesocket(slisten);
        WSACleanup();
        //pthread_kill(ThreadMainServer);
    }
};