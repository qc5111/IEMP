#include "PublicHead.h"
int charcmp(char * char1,char * char2, int len){
	for(int i;i<len;i++){
		if(char1[i]!=char2[i]){
			return 1;
		}
	}
	return 0;
}
void DynamicPassword(unsigned char * code,int len,int timeDiff)//unsigned char * encrypt,
{
	time_t t = time(NULL);
	unsigned char MD5Encrypted[16];
    unsigned char encrypt[20];
	int i2 = 0;
	int timestap = (int)((time(&t) + GLOBAL_TIME_DIFF)/ 30) + timeDiff;
    memcpy(encrypt,Configs,16);
    memcpy(encrypt+16,&timestap,4);
    MD5_CTX md5;
    MD5Init(&md5);
	
	//for(int i=0;i<20;i++){printf("%02x,",encrypt[i]);}printf("\n");
    MD5Update(&md5,encrypt,20);
	
    MD5Final(&md5,MD5Encrypted);
	memset(code, 0, len);//清空结果
	for(int i=0;i<16;i++){
		//printf("i2:%d,i:%d/n",i2,i);

		code[i2] += MD5Encrypted[i];
		//for(int i=0;i<8;i++){printf("%02x,",code[i]);}printf("\n");
		//printf("%d\n",MD5Encrypted[i]);
		//printf("1");
		i2++;
		if(i2==len){
			i2 = 0;
		}
	}

}
int CheckPassword(unsigned char * code,int len){// 0 True, 1 False unsigned char * encrypt,
	unsigned char CalcCode[8];
	DynamicPassword(CalcCode,8,0);
	if(charcmp((char*)code, (char*)CalcCode,8) == 0){
		return 0;
	}
	DynamicPassword(CalcCode,8,-1);// Time difference
	if(charcmp((char*)code, (char*)CalcCode,8) == 0){
		return 0;
	}
	DynamicPassword(CalcCode,8,1);
	if(charcmp((char*)code, (char*)CalcCode,8) == 0){
		return 0;
	}
	return -1;
}
/*
#include <stdio.h>
#include <sys/timeb.h>
#include <stdlib.h>
#if defined(WIN32)
# define  TIMEB    _timeb
# define  ftime    _ftime
typedef __int64 TIME_T;
#else
#define TIMEB timeb
typedef long long TIME_T;
#endif
int main (){
	unsigned char encrypt[20] ="0123456789abcdef";
	unsigned char code[8];
	
	struct TIMEB ts1,ts2;
	TIME_T t1,t2;
	ftime(&ts1);//开始计时
	for(int i=0;i!=999999;i++){
		DynamicPassword(encrypt,code,8);
	}
	ftime(&ts2);//停止计时
	t1=(TIME_T)ts1.time*1000+ts1.millitm;
	t2=(TIME_T)ts2.time*1000+ts2.millitm;
	printf("%d",t2-t1);
	//for(int i=0;i<8;i++){printf("%02x,",code[i]);}printf("\n");
	return 0;
}

int main (){
	TIME_ZONE_INFORMATION tzi;
    GetTimeZoneInformation(&tzi);
	GLOBAL_TIME_DIFF = tzi.Bias*60;
	printf("GLOBAL_TIME_DIFF:%d\n", GLOBAL_TIME_DIFF);
	unsigned char encrypt[20] ="0123456789abcdef";
	unsigned char code[8];

	DynamicPassword(encrypt,code,8,0);
	for(int i=0;i<8;i++){printf("%02x,",code[i]);}printf("\n");
	return 0;
}
*/