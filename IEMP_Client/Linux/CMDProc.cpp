#include "PublicHead.h"

void CMDProc(char * Order,int Datalen, int TCPSocket){
    //for(int i=0;i<Datalen;i++){printf("%02x,",Order[i]);}printf("\n");

    long long int Translen;
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
                    //printf("revData:%s\n",revData+2);
                    system(Order+2);
                    break;
                case 0x07://执行连续命令,先打开cmd，但无返回值
                    break;

            }
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
                        Buffer = GetFileList((char *)"/");
                    }else{
                        //printf("GetFolders");
                        Buffer = GetFileList(Order+2);
                    }
                    //for(int i=0;i<(unsigned char)FileList[0]+((unsigned char)FileList[1]<<8)+((unsigned char)FileList[2]<<16)+((unsigned char)FileList[3]<<24);i++){printf("%02hx,",FileList[i]);}printf("\n");
                    Datalen = (unsigned char)Buffer[0]+((unsigned char)Buffer[1]<<8)+((unsigned char)Buffer[2]<<16)+((unsigned char)Buffer[3]<<24)-4;
                    Order -= 8;//传入地址做过处理，所以此处需要使其回到原地址
                    if(Datalen <= 0){
                        free(Buffer);
                        send(TCPSocket, "00", 2, 0);
                        free(Order);
                        return;
                    }


                    free(Order);

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


            }
    }
    //printf("free");
    free(Order-8);
}
