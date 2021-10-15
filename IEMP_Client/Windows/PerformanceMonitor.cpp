#include "PublicHead.h"
void* PerformanceMonitor(void* args){
    char Buff[256];
    FILE *fp;
    fp=popen("typeperf \"\\processor(_total)\\% processor time\" -si 2","r");
    while(true){
        fgets(Buff,256,fp);
        if(Buff[25]==44){//ASCII 44为逗号
            //printf("Buff:%s",Buff+25);
            UDP.SendData(Buff+25,strlen(Buff+25));
        }
        
    }
    pclose(fp); 
}