#include "PublicHead.h"
#include <sys/sysinfo.h>
#include <sys/utsname.h>

#define MBPath "/sys/class/dmi/id/board_name"
#define CPUPath "/proc/cpuinfo"
char * ReadLine(FILE * fp,char *Success){//此函数自动移动指针
    int Pos = 0, MaxLen = 128;
    char size;
    char * Line;
    Line = (char *)malloc(MaxLen);
    while(true){
        size = fread(Line+Pos,1,1,fp);
        if(size == 0){
            *Success = 1;
            return Line;
        }
        if(Line[Pos] == 10){
            //printf("Pos:%d\n",Pos);
            Line[Pos] = 0;
            //printf("Line(InFunction):%s\n",Line);
            *Success = 0;
            return Line;
        }
        Pos++;
        if(Pos==MaxLen){
            MaxLen += 128;
            Line = (char *)realloc(Line,MaxLen);


        }
    }

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
        char * Line;
        int SendLen=0;
        long long int idle,kernel,user;
        float Result;
        struct sysinfo info;
        int cores;
        int Pos;
        char Success;
        struct utsname unameData;
        FILE *fp;

        SendData = (char *)malloc(1024);
        SendData[0] = 0;//初始化事件
        SendLen++;
        memcpy(SendData+SendLen,EID,4);
        SendLen += 4;
        sysinfo(&info);


        memcpy(SendData+SendLen,&info.totalram,8);
        SendLen += 8;

        //cores = get_nprocs_conf();
        //printf("cores_conf:%d\n",cores);
        cores = get_nprocs();
        //printf("cores:%d\n",cores);

        memcpy(SendData+SendLen,&cores,2);
        SendLen += 2;
        if(access(MBPath,R_OK) == -1){
            SendData[SendLen] = 6;
            SendLen++;
            memcpy(SendData+SendLen,"Unknow",6);
            SendLen += 6;
        }else{
            fp = fopen(MBPath,"r");
            Line = (char *)malloc(512);
            fread(Line,1,512,fp);
            SendData[SendLen] = strlen(Line)-1;
            SendLen++;
            memcpy(SendData+SendLen,Line,SendData[SendLen-1]);
            SendLen += SendData[SendLen-1];
            free(Line);
            fclose(fp);
        }


        uname(&unameData);
        SendData[SendLen] = strlen(unameData.version);
        SendLen++;
        memcpy(SendData+SendLen,unameData.version,SendData[SendLen-1]);
        SendLen += SendData[SendLen-1];





        fp = fopen(CPUPath,"r");
        while(true){
            Line=ReadLine(fp,&Success);
            if(Success != 0){
                SendData[SendLen] = 6;
                SendLen++;
                memcpy(SendData+SendLen,"Unknow",6);
                SendLen += 6;
                break;
            }
            Line[8] = 0;
            //printf("Line:%s\n",Line);
            if(strcmp("model na",Line)==0 || strcmp("Hardware",Line)==0){
                if (Line[0] == 'm'){
                    Pos = 13;
                }else{
                    Pos = 11;
                }
                //printf("strlen(Line+13):%d\n",strlen(Line+13));
                SendData[SendLen] = strlen(Line+Pos);
                SendLen++;
                memcpy(SendData+SendLen,Line+Pos,SendData[SendLen-1]);
                SendLen+=SendData[SendLen-1];
                free(Line);
                break;
            }

            free(Line);
        }

        fclose(fp);



        //while(ReadLine(fp,Line) == 0){
        //    printf("Line:%s",Line);
        //    free(Line);
        //}







        UDP.SendData(SendData,SendLen);
        free(SendData);
        SendData = (char *)malloc(9);
        //GetSystemTimes(&preIdleTime, &preKernelTime, &preUserTime);
        while(true){
            sleep(p->SleepTime);//120s
            if(p->Status == 0){
                return 0;
            }
            /*GetSystemTimes(&idleTime, &kernelTime, &userTime);
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
            SendData[0] = 1;//心跳事件
            GlobalMemoryStatusEx(&memStatus);
            memcpy(SendData+1,&Result,4);
            idle = (memStatus.ullTotalPhys-memStatus.ullAvailPhys)/1024/1024;
            memcpy(SendData+5,&idle,4);
            UDP.SendData(SendData,9);*/
        }
    }
    HeartBeat(int SleepTimeIn=1000){
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
