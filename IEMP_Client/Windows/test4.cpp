#include <stdio.h>
#include <string.h>
#include <malloc.h>

#include "zlib.h"

void data_compress(unsigned char *RawData, int RawDataLen,unsigned char *ResultData, int *ResultDataLen)
{
    z_stream z = {0};
    z.next_in = RawData;
    z.avail_in = RawDataLen;
    z.next_out = ResultData;
    z.avail_out = *ResultDataLen;
    deflateInit(&z, Z_BEST_COMPRESSION);
    deflate(&z, Z_NO_FLUSH);
    deflate(&z, Z_FINISH);
    deflateEnd(&z);
    printf("compressed data %d bytes.\n", z.avail_out);
    *ResultDataLen = *ResultDataLen - z.avail_out;
}


int data_decompress(unsigned char *idata, int ilen, unsigned char *odata, int *olen)
{
    z_stream z = {0};

    z.next_in = idata;
    z.avail_in = ilen;
    z.next_out = odata;
    z.avail_out = *olen;
    if (inflateInit(&z) != Z_OK) {
        printf("inflateInit failed!\n");
        return -1;
    }

    if (inflate(&z, Z_NO_FLUSH) != Z_STREAM_END) {
        printf("inflate Z_NO_FLUSH failed!\n");
        return -1;
    }

    if (inflate(&z, Z_FINISH) != Z_STREAM_END) {
        printf("inflate Z_FINISH failed!\n");
        return -1;
    }

    if (inflateEnd(&z) != Z_OK) {
        printf("inflateEnd failed!\n");
        return -1;
    }

    //*olen = strlen(odata);
    
    printf("decompressed data: %s\n", odata);

}

/*unsigned char data[]="\nYouth\n\nYouth is not a time of life; it is a state of mind; it is not a matter of rosy cheeks, red lips and supple knees; it is a matter of the will, a quality of the imagination, a vigor of the emotions; it is the freshness of the deep springs of life.\n\nYouth means a temperamental predominance of courage over timidity, of the appetite for adventure over the love of ease. This often exists in a man of 60 more than a boy of 20. Nobody grows old merely by a number of years. We grow old by deserting our ideals.\n\nYears may wrinkle the skin, but to give up enthusiasm wrinkles the soul. Worry, fear, self-distrust bows the heart and turns the spirit back to dust.\n\nWhether 60 or 16, there is in every human being's heart the lure of wonders, the unfailing appetite for what’s next and the joy of the game of living. In the center of your heart and my heart, there is a wireless station; so long as it receives messages of beauty, hope, courage and power from man and from the infinite, so long as you are young.\n\nWhen your aerials are down, and your spirit is covered with snows of cynicism and the ice of pessimism, then you’ve grown old, even at 20; but as long as your aerials are up, to catch waves of optimism, there’s hope you may die young at 80.";
 
int main(int argc, char **argv)
{
    int compress_len, decompress_len;
    unsigned char compress_buf[2048];
    unsigned char decompress_buf[4096];
    

    compress_len = sizeof(compress_buf);
    if (data_compress(data, strlen((char *)data),compress_buf, &compress_len) < 0) {
        return -1;
    }

    decompress_len = sizeof(decompress_buf);
    if (data_decompress(compress_buf, compress_len, 
                        decompress_buf, &decompress_len) < 0) {
        return -1;
    }
        
    return 0;
}*/
