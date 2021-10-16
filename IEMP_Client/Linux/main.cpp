#include "PublicHead.h"


int GetTimeDiff(){
    time_t UTCTimeStap, NowTimeStap;
    struct tm *UTCTm;
    NowTimeStap = time(NULL);
    UTCTm = gmtime(&NowTimeStap);
    UTCTimeStap = mktime(UTCTm);
    return UTCTimeStap-NowTimeStap;
}

int main(int argc,char *argv[])
{
    FILE *fp;
    //读取配置
    in_addr IP;
    fp = fopen(argv[0],"rb");
    fseek(fp, -32L, SEEK_END);
    fread(Configs,1,32,fp);
    fclose(fp);
    //读取EID
    memcpy(EID,Configs+16,4);
    //读取IP
    IP.s_addr = Configs[20]+(Configs[21]<<8)+(Configs[22]<<16)+(Configs[23]<<24);
    UDP.Init(inet_ntoa(IP));
    //for(int i=0;i<32;i++){printf("%02x,",Configs[i]);}printf("\n");
    //配置读取及初始化完成


    //初始化全局变量
    GLOBAL_TIME_DIFF = GetTimeDiff();


    //测试
    HeartBeat.start();

    getchar();
    return 0;
}