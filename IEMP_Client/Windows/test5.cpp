#include <pthread.h>
#include <stdio.h>
#include <sys/signal.h>

#define NUMTHREADS 3
void sighand(int signo);

void *threadfunc(void *parm)
{
    pthread_t             tid = pthread_self();
    int                   rc;

    printf("Thread %u entered/n", tid);
    rc = sleep(30); /* 若有信号中断则返回剩余秒数 */
    printf("Thread %u did not get expected results! rc=%d/n", tid, rc);
    return NULL;
}

void *threadmasked(void *parm)
{
    pthread_t             tid = pthread_self();
    sigset_t              mask;
    int                   rc;

    printf("Masked thread %lu entered/n", tid);

    sigfillset(&mask); /* 将所有信号加入mask信号集 */

    /* 向当前的信号掩码中添加mask信号集 */
    rc = pthread_sigmask(SIG_BLOCK, &mask, NULL);
    if (rc != 0)
    {
        printf("%d, %s/n", rc, strerror(rc));
        return NULL;
    }

    rc = sleep(15);
    if (rc != 0)
    {
        printf("Masked thread %lu did not get expected results! rc=%d /n", tid, rc);
        return NULL;
    }
    printf("Masked thread %lu completed masked work/n", tid);
    return NULL;
}

int main(int argc, char **argv)
{
    int                     rc;
    int                     i;
    struct sigaction        actions;
    pthread_t               threads[NUMTHREADS];
    pthread_t               maskedthreads[NUMTHREADS];

    printf("Enter Testcase - %s/n", argv[0]);
    printf("Set up the alarm handler for the process/n");

    memset(&actions, 0, sizeof(actions));
    sigemptyset(&actions.sa_mask); /* 将参数set信号集初始化并清空 */
    actions.sa_flags = 0;
    actions.sa_handler = sighand;

    /* 设置SIGALRM的处理函数 */
    rc = sigaction(SIGALRM,&actions,NULL);

    printf("Create masked and unmasked threads/n");
    for(i=0; i<NUMTHREADS; ++i)
    {
        rc = pthread_create(&threads[i], NULL, threadfunc, NULL);
        if (rc != 0)
        {
            printf("%d, %s/n", rc, strerror(rc));
            return -1;
        }

        rc = pthread_create(&maskedthreads[i], NULL, threadmasked, NULL);
        if (rc != 0)
        {
            printf("%d, %s/n", rc, strerror(rc));
            return -1;
        }
    }

    sleep(3);
    printf("Send a signal to masked and unmasked threads/n");

    /* 向线程发送SIGALRM信号 */
    for(i=0; i<NUMTHREADS; ++i)
    {
        rc = pthread_kill(threads[i], SIGALRM);
        rc = pthread_kill(maskedthreads[i], SIGALRM);
    }

    printf("Wait for masked and unmasked threads to complete/n");
    for(i=0; i<NUMTHREADS; ++i) {
        rc = pthread_join(threads[i], NULL);
        rc = pthread_join(maskedthreads[i], NULL);
    }

    printf("Main completed/n");
    return 0;
}

void sighand(int signo)
{
    pthread_t             tid = pthread_self();

    printf("Thread %lu in signal handler/n", tid);
    return;
}