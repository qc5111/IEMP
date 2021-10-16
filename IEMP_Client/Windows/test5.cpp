#include <windows.h>
#include <stdio.h>
int main(){
    SYSTEM_INFO si;
    char Test[2];
    GetSystemInfo(&si);
    printf("si.dwNumberOfProcessors:%d\n",si.dwNumberOfProcessors);
    memcpy(Test,&si.dwNumberOfProcessors,2);
    for(int i=0;i<2;i++){printf("%02x,",Test[i]);}printf("\n");

}