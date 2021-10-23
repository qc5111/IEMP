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
int GetCPUOC(unsigned int * Idle){
    FILE *fp;
    char buff[128];
    unsigned int CPUData[6];

    fp = fopen ("/proc/stat", "r");
    fgets (buff, 128, fp);
    fclose(fp);
    sscanf (buff+4,"%u %u %u %u %u %u %u",&CPUData[0],&CPUData[1],&CPUData[2],Idle,&CPUData[3],&CPUData[4],&CPUData[5]);
    return (CPUData[0]+CPUData[1]+CPUData[2]+CPUData[3]+CPUData[4]+CPUData[5]+*Idle);
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
        float Result;
        struct sysinfo info;
        int cores;
        int Pos;
        char Success;
        struct utsname unameData;
        unsigned int Idle,preIdle;
        unsigned int OC,preOC;
        float CPUUse;

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
        Pos = SendLen;

        SendData[Pos] = strlen(unameData.sysname)+1;
        SendLen++;
        memcpy(SendData+SendLen,unameData.sysname,SendData[Pos]);
        SendLen += SendData[Pos];
        SendData[SendLen-1] = 32;

        SendData[Pos] += strlen(unameData.nodename)+1;
        memcpy(SendData+SendLen,unameData.nodename,strlen(unameData.nodename));
        SendLen += (strlen(unameData.nodename)+1);
        SendData[SendLen-1] = 32;

        SendData[Pos] += strlen(unameData.release)+1;
        memcpy(SendData+SendLen,unameData.release,strlen(unameData.release));
        SendLen += (strlen(unameData.release)+1);
        SendData[SendLen-1] = 32;

        SendData[Pos] += strlen(unameData.machine);
        memcpy(SendData+SendLen,unameData.machine,strlen(unameData.machine));
        SendLen += (strlen(unameData.machine));


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
        preOC = GetCPUOC(&preIdle);
        while(true){

            sleep(p->SleepTime);//120s
            if(p->Status == 0){
                return 0;
            }
            OC = GetCPUOC(&Idle);
            if(OC == preOC){
                CPUUse = 0;
            }else{
                CPUUse =1 - (Idle-preIdle)*1.0/(OC-preOC);
            }
            preIdle = Idle;
            preOC = OC;
            SendData[0] = 1;
            sysinfo(&info);
            Idle = (info.totalram-info.freeram)/1024/1024;;
            memcpy(SendData+1,&CPUUse,4);
            memcpy(SendData+5,&Idle,4);
            UDP.SendData(SendData,9);


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
    HeartBeat(int SleepTimeIn=120){
        SleepTime = SleepTimeIn;

    }
    void Start(){
        Status = 1;
        pthread_create(&ThreadMainServer,NULL,MainServer,(void *)this);
    }
    void Close(){
        Status = 0;
    }

};
