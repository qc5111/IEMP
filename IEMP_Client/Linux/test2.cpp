// IEMP_Deploy_Core.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//
//gcc .cpp -lcrypto

#include <stdio.h>
#include <openssl/rsa.h>//apt-get install libssl-dev
#include <openssl/pem.h>
#include <openssl/rand.h>
#include <string.h>
#if defined(_WIN32)
#include <winsock2.h>
#pragma comment(lib,"ws2_32.lib")
#else
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#endif
#define _WINSOCK_DEPRECATED_NO_WARNINGS

int main()
{
    BIO* bio;
    RSA* PubKey;
    int DataLen;
#if defined(_WIN32)
    SOCKET clientfd;
    printf("Win32");
#else
    int clientfd;
    printf("Linux");
#endif
    int ret;
    int addrlen;
    char Order[2];
    char Data[1024];
    char PubKeyPem[1024] = "-----BEGIN RSA PUBLIC KEY-----\n";
    char EnData[256];

#if defined(_WIN32)
    WSADATA wsaData;
    WSAStartup(MAKEWORD(2, 2), &wsaData);
#endif






    clientfd = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in seraddr = { 0 };
    seraddr.sin_family = AF_INET;
    seraddr.sin_port = htons(48280);
    seraddr.sin_addr.s_addr = inet_addr("10.0.1.123");
    addrlen = sizeof(seraddr);
    ret = connect(clientfd, (struct sockaddr*)&seraddr, addrlen);
    if (ret != 0) {
        printf("Error! Connect to satellite server error!");
        exit(-1);
    }
    Order[0] = 0;
    Order[1] = 0;
    send(clientfd, Order,2,0);
    DataLen = recv(clientfd, Data, 1024, 0);
    //closesocket(clientfd);
    Data[DataLen] = 0;

    //printf("ret:%d\n", ret);
    strcat(PubKeyPem, Data);
    strcat(PubKeyPem, "\n-----END RSA PUBLIC KEY-----\n");
    printf("PubKeyPem:%s\n", PubKeyPem);


    DataLen = 0;
    //加入随机密码
    RAND_bytes((unsigned char*)Data, 16);
    DataLen += 16;
    for (int i = 0;i < 16;i++) { printf("%02x,", (unsigned char)Data[i]); }printf("\n");

    //Data需要包含：文本编码，密码，当前操作系统
    //Data[33] = 0;
    //DataLen = strlen(Data);
    bio = BIO_new_mem_buf(PubKeyPem, -1);
    PubKey = PEM_read_bio_RSAPublicKey(bio, NULL, NULL, NULL);
    ret = RSA_public_encrypt(DataLen, (unsigned char*)Data, (unsigned char*)EnData, PubKey, RSA_PKCS1_PADDING);
    if (ret != 256) {
        printf("Error! RSA Encrypt Fail!");
        exit(-1);
    }


    clientfd = socket(AF_INET, SOCK_STREAM, 0);
    ret = connect(clientfd, (struct sockaddr*)&seraddr, addrlen);
    printf("ret:%d\n", ret);
    Order[1] = 1;
    send(clientfd, Order, 2, 0);
    send(clientfd, EnData, 256, 0);
    for (int i = 0;i < 256;i++) { printf("%02x,", (unsigned char)EnData[i]); }printf("\n");

}