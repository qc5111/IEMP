#include<stdio.h>
#include<unistd.h>
#include<string.h>
#include<stdlib.h>
#include <sys/wait.h>
int main()
{
    execl("/bin/sh", "sh", "-c", cmdstring, (char *)0);
}