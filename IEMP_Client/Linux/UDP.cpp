#include "PublicHead.h"
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

class UDP{
	private:
		int UDPClient;
        sockaddr_in ServerInfo;
		int ServerInfoLen;
	public:
	UDP(char * ServerIP){
			Init(ServerIP);
	}
	UDP(){
	}
	void Init(char * ServerIP){
        //printf("ServerIP:%s\n", ServerIP);
		UDPClient = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
		ServerInfo.sin_family = AF_INET;
		ServerInfo.sin_port = htons(48281);
		ServerInfo.sin_addr.s_addr = inet_addr(ServerIP);
		ServerInfoLen = sizeof(ServerInfo);
        //printf("INIT OK\n");
	}
	void SendData(char * Data,int Datalen){
		sendto(UDPClient, Data, Datalen, 0, (sockaddr *)&ServerInfo, ServerInfoLen);
	}
	void Close(){
        close(UDPClient);
	}
	~UDP(void)
	{
    	Close();
	}
};
/*int main(){
	UDP UDP;
	UDP.Init("127.0.0.1");
	UDP.SendData("test2",10);
}*/
