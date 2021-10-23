#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

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
int main(){
    unsigned int Idle,preIdle;
    unsigned int OC,preOC;
    float cpu_use;
    preOC = GetCPUOC(&preIdle);
    while(true){
        //printf("OC:%u,idle:%u\n",OC,Idle);
        sleep(5);
        OC = GetCPUOC(&Idle);
        //printf("OC:%u,PreOC:%u,Idle:%u,PreIdle:%u\n",OC,preOC,Idle,preIdle);
        if(OC == preOC){
            cpu_use = 0;
        }else{

            cpu_use =1 - (Idle-preIdle)*1.0/(OC-preOC);
        }
        preIdle = Idle;
        preOC = OC;
        printf("cpu_use:%f\n",cpu_use);
    }


}