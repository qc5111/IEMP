#include <windows.h>
#include <stdio.h>
#include <time.h>
int main(){
    time_t t = time(NULL);
    printf("t:%d\n",t);
}