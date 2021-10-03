/** @file 
* @brief 进程统计信息函数的测试 
* @author 张亚霏 
* @date 2009/05/03 
* @version 0.1 
* 
*/  
  
#include "process_stat.h"  
#include <stdio.h>  
#include <Windows.h>  
  
int main()   
{   
    while(1)   
    {  
        int cpu;  
        uint64_t mem, vmem, r, w;  
  
  
        cpu = get_cpu_usage();  
        get_memory_usage(&mem, &vmem);  
        get_io_bytes(&r, &w);  
  
        printf("CPU使用率: %u\n",cpu);  
        printf("内存使用: %u 字节\n", mem);  
        printf("虚拟内存使用: %u 字节\n", vmem);  
        printf("总共读: %u 字节\n", r);  
        printf("总共写: %u 字节\n", w);   
  
        Sleep(1000);   
    }   
    return 0;   
}  