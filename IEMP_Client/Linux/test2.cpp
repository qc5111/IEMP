#include<stdio.h>
#include<unistd.h>
#include<string.h>
#include<stdlib.h>
#include <sys/wait.h>


#include <errno.h>
int system1(const char *cmdstring) /* version without signal handling */
{
    pid_t pid;
    int status;
    if (cmdstring == NULL)
        return(1); /* always a command processor with UNIX */
    if ((pid = fork()) < 0) {
        status = -1; /* probably out of processes */
    } else if (pid == 0) { /* child */
        //execl("/bin/sh", "sh", "-c", "cd /etc", (char *)0);
        execl("/bin/sh", "sh", "-c", cmdstring, (char *)0);
        _exit(127); /* execl error */
    } else { /* parent */
        while (waitpid(pid, &status, 0) < 0) {
            if (errno != EINTR) {
                status = -1; /* error other than EINTR from waitpid() */
                break;
            }
        }
    }
    return(status);
}

int main()
{
    int fpipe[2] = {0};
    pid_t fpid;
    char massage[1000] = {0};
    memset(massage, 0, 20);
    if (pipe(fpipe) < 0)
    {
        printf("Create pipe error!\n");
    }
    fpid = fork();
    if (fpid > 0)
    {
        close(fpipe[0]);
        dup2(fpipe[1],STDOUT_FILENO);
        //execl("/bin/sh", "sh", "-c", command, (char *) NULL);
        //system("bash");
        system1("ls");
    }
    else if (fpid == 0)
    {
        wait(NULL);
        printf("this is father,recieve:");
        fflush(stdout);
        close(fpipe[1]);
        read(fpipe[0], massage, 1000);
        printf("%s\n",massage);
    }
    else
    {
        printf("create fork error!\n");
    }
    return 0;
}