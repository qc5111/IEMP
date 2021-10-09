//Information equipment management platform
#include <winsock2.h>
#include <windows.h>
#include <stdio.h>
#include <pthread.h>
#pragma comment(lib,"ws2_32.lib")
static int GLOBAL_TIME_DIFF;
#include "DynamicPassword.c"
#include "FileOP.cpp"
#include "RemoteCMD.cpp"
#include "UDP.cpp"
#include "gzip.cpp"
UDP UDP;
char EID[4];//EquiptmentID
#include "PerformanceMonitor.cpp"
#include "HeartBeat.cpp"
//全局变量声明


int GetTimeDiff(){
    TIME_ZONE_INFORMATION tzi;
    int ret = GetTimeZoneInformation(&tzi);
    //printf("ret:%d,tzi.DaylightBias:%d\n",ret,tzi.DaylightBias);
    if(ret == 2){//中国时区为0，斐济时区为1，伦敦时区为2
        return (tzi.Bias+tzi.DaylightBias)*60;
    }else{
        return tzi.Bias*60;
    }
    
	
}
int main(int argc,char *argv[])//RealMain main
{
    
    //隐藏窗体
    //HWND hwnd = GetForegroundWindow();	//获取程序启动时的窗口
    //ShowWindow(hwnd, SW_HIDE);
    //变量初始化
    int ret,DataLen;
    char SendData[2] = {0,0};
    FILE *fp;
	//读取配置
    unsigned char Configs[32];
    struct in_addr IP;
    fp = fopen(argv[0],"rb");
    fseek(fp, -32L, SEEK_END);
    fread(Configs,1,32,fp);
    //读取EID
    memcpy(EID,Configs+16,4);
    //for(int i=0;i<32;i++){printf("%d,",i);printf("%02x\n",Configs[i]);}printf("\n");
    //读取IP
    IP.s_addr = Configs[20]+(Configs[21]<<8)+(Configs[22]<<16)+(Configs[23]<<24);
    //printf("%s\n",inet_ntoa(IP));
	//unsigned char password[20] ="0123456789abcdef"; // 0123456789abcdef
    UDP.Init(inet_ntoa(IP));
    RemoteCMD RemoteCMD(Configs);
    //初始化全局变量
    GLOBAL_TIME_DIFF = GetTimeDiff();
    //printf("GLOBAL_TIME_DIFF:%d",GLOBAL_TIME_DIFF);
    //初始化心跳
    
    pthread_t ThreadHeartBeat;
    pthread_create(&ThreadHeartBeat,NULL,HeartBeat,NULL);
    
    //初始化远程CMD
    RemoteCMD.start();
    //初始化监控
    //pthread_t ThreadPerformanceMonitor;
    //pthread_create(&ThreadPerformanceMonitor,NULL,PerformanceMonitor,NULL);
    
    //初始化网络
    WORD sockVersion = MAKEWORD(2,2);
    WSADATA wsaData;
	WSAStartup(sockVersion, &wsaData);


    //创建套接字
    SOCKET slisten = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);

    //绑定IP和端口
    sockaddr_in sin;
    sin.sin_family = AF_INET;
    sin.sin_port = htons(48280);//Port
    sin.sin_addr.S_un.S_addr = INADDR_ANY;
	bind(slisten, (LPSOCKADDR)&sin, sizeof(sin));
    //开始监听
	listen(slisten, 5);
    //循环接收数据
    SOCKET sClient;
    sockaddr_in remoteAddr;
    int nAddrlen = sizeof(remoteAddr);
    char *revData;
    //revData = (char *)malloc(2);
    char *FileData;
    unsigned long long int Translen;
    char *FileList;
    while (true){
        //free(revData);
        sClient = accept(slisten, (SOCKADDR *)&remoteAddr, &nAddrlen);
        if(sClient == INVALID_SOCKET){
            printf("accept error !");
            continue;
        }
        //printf("接受到一个连接：%s \r\n", inet_ntoa(remoteAddr.sin_addr));

        //接收数据
		while(true){
            //接受数据长度
            
            revData = (char *)malloc(2);
            ret = recv(sClient, revData, 2, 0);
            if(ret == 0){
                break;
            }
            DataLen = revData[0] + revData[1] * 256;//struct.pack('<I', int)[:2]
            free(revData);
            revData = (char *)malloc(DataLen);//重新分配大小，最大为65535
			ret = 0;
            //printf("DataLen:%d\n",DataLen);
            while(ret != DataLen){
                ret += recv(sClient, revData+ret, 128, 0);
                if(ret == 0){
                    break;
                }
            }
            if(ret == 0){
                break;
            }
            revData[ret] = 0;
            //printf("%s\n",revData);
            if(ret>9){
                if(CheckPassword(Configs,(unsigned char*)revData,8)==0){
                    //run command
                    //printf("Pass\n");
                    switch(revData[8]){//大类区分
                        case 0x00://系统操作类
                            switch(revData[9]){
                                case 0x00://关机
                                    system("shutdown -p");
                                    break;
                                case 0x01://重启
                                    system("shutdown -r -t 0");
                                    break;
                                //02保留为开机指令
                                //03为睡眠
                                case 0x04://休眠
                                    system("shutdown -h");
                                    break;
                                case 0x06://执行cmd无返回值
                                    printf("revData:%s\n",revData+10);
                                    system(revData+10);
                                    break;
                                case 0x07://执行连续命令,先打开cmd，但无返回值
                                    fp = popen("cmd","w");
                                    send(sClient, SendData, 2, 0);
                                    while(true){
                                        ret = recv(sClient, revData, 127, 0);
                                        revData[ret] = 0;
                                        if(revData[0] == 0){
                                            break;
                                        }
                                        fputs(revData, fp);
                                    }
                                    pclose(fp);

                            }
                        case 0x01://文件操作类
                            switch(revData[9]){
                                case 0x00://上传文件到客户机
                                    fp = fopen(revData+10, "wb");//传入文件名
                                    Translen=0;
                                    //unsigned long long int Nowlen=0;
                                    //printf("ret:%d",ret);
                                    memcpy(&Translen,revData+ret-8,8);
                                    //for(int i=0;i<ret;i++){printf("%02x,",revData[i]);}printf("\n");
                                    //printf("Translen:%d\n",Translen);
                                    //printf("Fresh.Translen:%I64u\n",Translen);
                                    FileData = (char *)malloc(1024);
                                    send(sClient, SendData, 2, 0);
                                    while(true){
                                        ret = recv(sClient, FileData, 1024, 0);
                                        //printf("ret:%d\n",ret);
                                        fwrite(FileData, ret, 1, fp);
                                        Translen-=ret;
                                        //if(ret!=512){
                                        //    printf("ret:%d\n",ret);
                                        //    printf("Translen:%d,Nowlen:%d\n",Translen,Nowlen);
                                        //}
                                       // printf("Translen:%d\n",Translen);
                                        //printf("Translen:%I64u\n",Translen);
                                        if(Translen < 1){
                                            //printf("Normal Break");
                                            break;
                                        }
                                    }
                                    free(FileData);
                                    fclose(fp);
                                    break;
                                case 0x01://从客户机下载文件
                                    break;
                                case 0x02://列出文件列表
                                    if(ret == 10){
                                        //printf("GetDrivers");
                                        FileList = GetDrivers(); 

                                    }else{
                                        //printf("GetFolders");
                                        FileList = GetFileList(revData+10); 
                                    }
                                    //for(int i=0;i<(unsigned char)FileList[0]+((unsigned char)FileList[1]<<8)+((unsigned char)FileList[2]<<16)+((unsigned char)FileList[3]<<24);i++){printf("%02hx,",FileList[i]);}printf("\n");
                                    free(revData);
                                    ret = (unsigned char)FileList[0]+((unsigned char)FileList[1]<<8)+((unsigned char)FileList[2]<<16)+((unsigned char)FileList[3]<<24)-4;
                                    //printf("ret:%d\n",ret);
                                    if(ret>2048){
                                        revData =  (char *)malloc(ret);
                                    }else{
                                        revData =  (char *)malloc(2048);
                                    }
                                    //printf("ret:%d\n",ret);
                                    data_compress((unsigned char *)(FileList+4),ret,(unsigned char *)revData, &ret);
                                    //printf("ret:%d\n",ret);
                                    free(FileList);
                                    
                                    //printf("ALlLen:%d\n",(unsigned char)FileList[0]);//+(FileList[1]<<8)+(FileList[2]<<16)+(FileList[3]<<24)
                                    //for(int i=0;i<8;i++){printf("%02hx,",FileList[i]);}printf("\n");
                                    //printf("FileList[2]:%d\n",FileList[2]);
                                    send(sClient, revData, ret, 0);
                                    //free(revData);
                                    break;
                                
                            }
                    }
                    SendData[0] = 0;
                    send(sClient, SendData, 2, 0);
                }else{
                    //printf("UnPass\n");//密码错误
                    SendData[0] = 1;
                    send(sClient, SendData, 2, 0);
                }
                break;
            }
		}
        //发送数据
        //printf("free!");
        free(revData);
        closesocket(sClient);
    }

    closesocket(slisten);
    WSACleanup();
    return 0;
}