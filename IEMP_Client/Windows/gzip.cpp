//#include <stdio.h>
//#include <string.h>
//#include <malloc.h>

#include "zlib.h"

void data_compress(unsigned char *RawData, int RawDataLen,unsigned char *ResultData, int *ResultDataLen)
{
    
    z_stream z = {0};
    z.next_in = RawData;
    z.avail_in = RawDataLen;
    z.next_out = ResultData;
    z.avail_out = *ResultDataLen;
    if(z.avail_out<2048){
        z.avail_out = 2048;
        *ResultDataLen = 2048;
    }
    deflateInit(&z, Z_BEST_COMPRESSION);
    deflate(&z, Z_NO_FLUSH);
    deflate(&z, Z_FINISH);
    deflateEnd(&z);
    //printf("compressed data %d bytes.\n", z.avail_out);
    //z = {0};
    *ResultDataLen = *ResultDataLen - z.avail_out;
}
