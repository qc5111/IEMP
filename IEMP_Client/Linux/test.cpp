#include<stdio.h>
#include<pthread.h>
#include <stdlib.h>
#include <unistd.h>
void* start(void *p){
    char *Process=(char *)p;
    //printf("p:%s\n",p);
    system(Process);
    return 0;
}
int main(){
    pthread_t Thread;
    char Process[256] = "sh ./renew.sh";
    //"start rename.vbs"
    pthread_create(&Thread, NULL, start, Process);
    sleep(1);
    printf("OK!");
    return 0;
    //CreateProcess("notepad.exe", NULL,NULL, NULL,FALSE, NULL, NULL, NULL, NULL, NULL);
    //CreateProcess("notepad.exe", NULL, NULL, NULL, TRUE, NULL, NULL, NULL, NULL, NULL);
}