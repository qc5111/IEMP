#include <stdio.h>
#include <pthread.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <dirent.h>
#include <cstdlib>
#include <time.h>
#include <cstring>
#include<sys/socket.h>
#include <sys/time.h>
int GetTimeDiff(){
    time_t UTCTimeStap, NowTimeStap;
    struct tm *UTCTm;
    NowTimeStap = time(NULL);
    UTCTm = gmtime(&NowTimeStap);
    UTCTimeStap = mktime(UTCTm);
    return UTCTimeStap-NowTimeStap;
}
int main (){
                    /* 获取本地utc时间 */
                    struct timeval tv;
                    struct timezone tz;
                    int ret=gettimeofday(&tv,  &tz);
    time_t NowTimeStap = time(NULL);
                    printf("NowTimeStap:%d\n",NowTimeStap);
                    printf("ret:%d\ntz.tz_minuteswest:%d\ntz.tz_dsttime:%d\n",ret,tz.tz_minuteswest,tz.tz_dsttime);
                    /* utc时间 单位 秒*/
                    long long timestamp = tv.tv_sec;
                    printf("timestamp:%lld\n",timestamp);

                    /* utc时间 单位 毫秒 */
                    timestamp = tv.tv_sec*1000 + tv.tv_usec/1000;

                    /* utc时间 单位 微秒 */
                    timestamp = tv.tv_sec*1000*1000 + tv.tv_usec;

                    /* utc时间字符串 */
                    char timeStr[20];
                    memset(timeStr, 0, sizeof(timeStr));
                    sprintf(timeStr, "%d", timestamp);		// int
                    sprintf(timeStr, "%ld", timestamp);		// long
                    sprintf(timeStr, "%lld", timestamp);	// long long

                    /* utc时间字符串转换为整型 */
                    int timeInt = atoi(timeStr);			// 转成整型 int
                    long timeLong = atol(timeStr);			// 转成长整型 long
                    long long timeLLong = atoll(timeStr);	// 转成长长整型 long long

}