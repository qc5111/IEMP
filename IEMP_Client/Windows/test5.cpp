#include <windows.h>
#include <stdio.h>
#include <time.h>
#include "dirent.h"

int main()
{
    char *test;
    test = (char *)malloc(50);
    while(true){
        free(test);
        test = (char *)malloc(50);
        
    }
    printf("test");
}
