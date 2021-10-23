#include "PublicHead.h"
long long GetFileSize(char * FilePath){
    struct stat64 File;
    //printf("Disk:%c:\n", buf.st_dev + 'A');
    //printf("CreaTimeStap:%d",buf.st_atime);
    if(stat64(FilePath, &File)<0){
        return -1;
    }
    //printf("DataLong:%d\n",sizeof(File.st_size));
    return File.st_size;

}
char * GetFileList(char * Path){//记得free
    struct dirent* entry;
    DIR *pDir;
    struct stat64 File;
    pDir = opendir(Path);
    int Pathlen = strlen(Path);
    char FileStyle;
    char NowFilePath[Pathlen+261];
    char *Flist;
    int MaxLen,Nowlen = 4;
    char Temp;
    int i;
    //初始化文件内存
    MaxLen = 1023;
    Flist = (char *)malloc(1024);
    if (access(Path,F_OK) == -1){
        Flist[0] = 0;
        Flist[1] = 0;
        Flist[2] = 0;
        Flist[3] = 0;
        free(entry);
        free(pDir);
        return Flist;
    }
    strcpy(NowFilePath,Path);
    strcat(NowFilePath,"/");
    Pathlen++;
    //int i = 0;
    while ((entry = readdir(pDir)) != NULL){
        NowFilePath[Pathlen] = 0;
        strcat(NowFilePath,entry->d_name);
        //printf("NowFilePath:%s\n",NowFilePath);
        stat64(NowFilePath, &File);
        //printf("%s,",NowFilePath);//entry->d_name
        //printf("File.st_mode:%d\n",File.st_mode);
        if((File.st_mode >> 14) % 2){//文件夹
            FileStyle = 4;
        }else if ((File.st_mode >> 15) % 2){//普通文件
            FileStyle = 8;
        }else{
            FileStyle = 1;
        }
        Temp = strlen(entry->d_name);
        if((Temp == 1 && entry->d_name[0] == 0x2e) || (Temp == 2 && entry->d_name[0] == 0x2e && entry->d_name[1] == 0x2e)){
            //为.或..，则跳过
            continue;
        }
        
        //文件名长度+文件类型1字节+分隔符1字节
        if(Nowlen+Temp+11>MaxLen){
            MaxLen+=1024;//延长1024字节的长度
            Flist = (char *) realloc(Flist, MaxLen+1);
        }
        
        Flist[Nowlen] = FileStyle;
        Nowlen++;
        memcpy(Flist+Nowlen,&File.st_mtime,4);
        Nowlen+=4;
        if(FileStyle == 8){
            Flist[Nowlen+9] = 0;
            //for(int i=0;i<70;i++){printf("%02hx,",Flist[i]);}printf("\n");
            memcpy(Flist+Nowlen+1,&File.st_size,8);
            //for(int i=0;i<70;i++){printf("%02hx,",Flist[i]);}printf("\n");
            //printf("Nowlen:%d,Lenlen:%d\n",Nowlen,strlen(Flist+Nowlen+1));
            Flist[Nowlen] = 1;
            for(i=Nowlen+1;i<Nowlen+9;i++){
                //printf("%02hx,",Flist[i]);
                if (Flist[i]!=0){
                    Flist[Nowlen] = i-Nowlen+1;
                    //printf("Flist[Nowlen]:%d\n",Flist[Nowlen]);
                }
            }
            //Flist[Nowlen] = strlen(Flist+Nowlen+1)+1;//为避免0x00，所以+1
            Nowlen += (unsigned char)Flist[Nowlen];
        }
        //printf("Nowlen:%d,",Nowlen);
        //printf("Temp:%d,\n",Temp);
        Flist[Nowlen] = Temp;
        Flist[Nowlen+1] = 0;
        Nowlen++;
        strcat(Flist+Nowlen,entry->d_name);
        //strcat(Flist+Nowlen,"/");
        Nowlen += Temp;
        //printf("Nowlen:%d,\n",Nowlen);
        //printf("Nowlen:%d,\n",Nowlen);
        //printf("Sizeof:%d\n",sizeof(File.st_size));
        //printf("File:%s,Style:%d,Size:%lld,mtime:%ld\n",entry->d_name,FileStyle,File.st_size,(int)File.st_mtime);
        //printf("%s\n",Flist);
        
        //printf("%s\n",Flist);
        
        
    }
    free(pDir);
    free(entry);
    //printf("Nowlen:%d,\n",Nowlen);
    memcpy(Flist,&Nowlen,4);
    //printf("%s\n",Flist);
    //free(Flist);
    //for(int i=0;i<strlen(Flist);i++){printf("%02x,",Flist[i]);}printf("\n");
    return Flist;
}
/*int main(){
    _ULARGE_INTEGER Size1,Size2;
    GetDiskFreeSpaceEx("C:\\",&Size1,&Size2,NULL);
    printf("Size1:%lld,Size2:%lld,Size3:%lld\n",Size1.QuadPart,Size2.QuadPart);
}*/
/*int main(int argc,char *argv[]){
    //char *FileList = GetDrivers();
    //char TestLongLong[16];
    
    //long long test = GetFileSize("D:\\TEST\\FantasyAllStar.rar");
    //memcpy(TestLongLong+8,&test,8);
    //printf("%d\n",strlen(TestLongLong));
    //for(int i=0;i<16;i++){printf("%02x,",TestLongLong[i]);}printf("\n");
    //TestLongLong[0] = test >> 64;
    //printf("%lld",test);
    //GetFileList("D:\\Desktop\\Desktop1_20210817\\IEMP_Client");
    char *FileList = GetFileList("/");// C:\\Windows\\System32  D:\\TEST
    //for(int i;i<10000;i++){
    //    char *Flist = GetFileList("D:\\TEST");// C:\\Windows\\System32
    //    free(Flist);
    //}
    //printf("%s\n",Flist+4);
    //printf("int:%d\n",Flist[0]+(Flist[1]<<8)+(Flist[2]<<16)+(Flist[3]<<24));//
    //printf("%d\n",strlen(Flist+4)+4);
    for(int i=0;i<(unsigned char)FileList[0]+((unsigned char)FileList[1]<<8)+((unsigned char)FileList[2]<<16)+((unsigned char)FileList[3]<<24);i++){printf("%02hx,",FileList[i]);}printf("\n");
    //free(Flist);

    return 0;

}*/