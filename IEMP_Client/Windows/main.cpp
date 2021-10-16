//Information equipment management platform
#include "PublicHead.h"

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
    //变量初始化
    int ret,DataLen;
    FILE *fp;
	//读取配置
    struct in_addr IP;
    fp = fopen(argv[0],"rb");
    fseek(fp, -32L, SEEK_END);
    fread(Configs,1,32,fp);
    fclose(fp);
    //读取EID
    memcpy(EID,Configs+16,4);
    //for(int i=0;i<32;i++){printf("%d,",i);printf("%02x\n",Configs[i]);}printf("\n");
    //读取IP
    IP.s_addr = Configs[20]+(Configs[21]<<8)+(Configs[22]<<16)+(Configs[23]<<24);
    UDP.Init(inet_ntoa(IP));
    //配置读取及初始化完成
    //初始化全局变量
    GLOBAL_TIME_DIFF = GetTimeDiff();
    //printf("GLOBAL_TIME_DIFF:%d",GLOBAL_TIME_DIFF);

    //初始化心跳和性能监控
    HeartBeat.start();//8KB Memory

    //初始化远程CMD
    RemoteCMD.start();//20KB Memory
    
    //初始化网络
    TcpServer.start();//20KB Memory

    //停住进程
    getchar();

    return 0;
}