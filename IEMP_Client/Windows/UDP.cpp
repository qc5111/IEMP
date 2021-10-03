#include <stdio.h>
#include <winsock2.h>

#pragma comment(lib, "ws2_32.lib") 
class UDP{
	private:
		SOCKET UDPClient;
		sockaddr_in ServerInfo;
		int ServerInfoLen;
	public:
	UDP(char * ServerIP){
			Init(ServerIP);
	}
	UDP(){
	}
	void Init(char * ServerIP){
		WORD socketVersion = MAKEWORD(2,2);
		WSADATA wsaData; 
		WSAStartup(socketVersion, &wsaData);
		UDPClient = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
		ServerInfo.sin_family = AF_INET;
		ServerInfo.sin_port = htons(48281);
		ServerInfo.sin_addr.S_un.S_addr = inet_addr(ServerIP);
		ServerInfoLen = sizeof(ServerInfo);
	}
	void SendData(char * Data,int Datalen){
		sendto(UDPClient, Data, Datalen, 0, (sockaddr *)&ServerInfo, ServerInfoLen);
	}
	void Close(){
		closesocket(UDPClient);
		WSACleanup();
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
