package main

import (
	"fmt"
	"net"
)

func getMacAddrs() (macAddrs []string) {
	netInterfaces, err := net.Interfaces()
	if err != nil {
		fmt.Printf("fail to get net interfaces: %v", err)
		return macAddrs
	}
	//fmt.Println(netInterfaces)
	for _, netInterface := range netInterfaces {
		macAddr := netInterface.HardwareAddr.String()
		if len(macAddr) == 0 {
			continue
		}

		macAddrs = append(macAddrs, macAddr)
	}
	return macAddrs
}

func getIPs() (ips []string) {

	interfaceAddr, err := net.InterfaceAddrs()
	fmt.Println(interfaceAddr)
	if err != nil {
		fmt.Printf("fail to get net interface addrs: %v", err)
		return ips
	}

	for _, address := range interfaceAddr {
		ipNet, isValidIpNet := address.(*net.IPNet)
		if isValidIpNet && !ipNet.IP.IsLoopback() {
			if ipNet.IP.To4() != nil {
				ips = append(ips, ipNet.IP.String())
			}
		}
	}
	return ips
}
func getLocalIPv4Address() (ipv4Address string, err error){
	//获取所有网卡
	addrs, err := net.InterfaceAddrs()

	//遍历
	for _, addr := range addrs {
		//取网络地址的网卡的信息
		ipNet, isIpNet := addr.(*net.IPNet)
		//是网卡并且不是本地环回网卡
		if isIpNet && !ipNet.IP.IsLoopback() {
			ipv4 := ipNet.IP.To4()
			//能正常转成ipv4
			if ipv4 != nil {
				fmt.Println(ipv4)

			}
		}
	}
	return "", nil

	return
}


func main() {

	Data:=AndroidGetprop("persist.sys.device_name")
	fmt.Println("'"+Data+"'")
	//BytesOut := make([]byte, 2048)
	//Len,_ := stdout0.Read(BytesOut)
	//fmt.Println(Len)
	//outputBuf0.Write(BytesOut[:Len])


}