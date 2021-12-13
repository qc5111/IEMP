package main
import (
	"fmt"
	"os/exec"
	"strconv"
	"strings"
	"syscall"
)
import "time"
import "os"
import "bytes"
import "runtime"
import "net/http"
import "net/url"
import "crypto/x509"
import "crypto/rsa"
import "encoding/pem"
import "encoding/base64"
import mrand "math/rand"
import crand "crypto/rand"


func HttpGet(url string) string{
	var Buff [512]byte
	Buff2 := bytes.NewBuffer(nil)
	client := &http.Client{Timeout: 5 * time.Second}
	resp, err := client.Get("https://"+url)

	if err != nil{
		resp, err = client.Get("http://"+url)
		if err != nil{
			return ""
		}

	}
	Datalen,_ := resp.Body.Read(Buff[0:])
	defer resp.Body.Close()
	client.CloseIdleConnections()
	Buff2.Write(Buff[0:Datalen])
	return Buff2.String()
}

func RSAEncrypt(Data []byte, PubKeyString string) string{
	PubKeyPem, _ := pem.Decode([]byte("-----BEGIN RSA PUBLIC KEY-----\n"+PubKeyString+"\n-----END RSA PUBLIC KEY-----"))
	PubKey, _ := x509.ParsePKCS1PublicKey([]byte(PubKeyPem.Bytes))
	EnData, _ := rsa.EncryptPKCS1v15(crand.Reader,PubKey, []byte(Data))
	EnDataBase64 := base64.StdEncoding.EncodeToString(EnData)
	return EnDataBase64
}

func GetRandCode() [16]byte{
	var Buff [16]byte
	mrand.Seed(time.Now().UnixNano())

	for i := 0; i < 16; i ++ {
		mrand.NewSource(time.Now().UnixNano())
		Buff[i] = byte(mrand.Int63()%256)
	}
	return Buff
}

func Int2Bytes(intData int32) [4]byte{
	var ByteData [4]byte
	ByteData[0] = uint8(intData)
	ByteData[1] = uint8(intData >> 8)
	ByteData[2] = uint8(intData >> 16)
	ByteData[3] = uint8(intData >> 24)
	return ByteData
}

func IPPort2Bytes(IP string) [4]byte{
	var ByteData [4]byte
	IPSplited := strings.Split(IP,".")
	for i :=  range IPSplited{
		IntData,_ := strconv.Atoi(IPSplited[i])
		ByteData[i] = byte(IntData)
	}


	return ByteData
}

func AndroidGetprop(SubName string) string{
	var outputBuf0 bytes.Buffer
	cmd := exec.Command("getprop",SubName)
	cmd.Stdout = &outputBuf0
	cmd.Start()
	cmd.Wait()

	return strings.TrimRight(outputBuf0.String(), "\n")
}

func WriteConf(FilePath string,WriteData []byte) string{
	var Buff []byte = make([]byte, 16)
	var DataCheck = []byte{48,49,50,51,52,53,54,55,56,57,97,98,99,100,101,102}
	file, err := os.OpenFile(FilePath,syscall.O_RDWR,0777) //file.Seek()
	if err!=nil{
		return "Error! File open error!"
	}
	file.Seek(-32,2)
	file.Read(Buff)
	for i:=0;i<16;i++{
		if Buff[i]!=DataCheck[i]{
			return "Error! Executable file is not an IEMP Client!"
		}
	}

	file.Seek(-32,2)
	file.Write(WriteData)
	defer file.Close()
	return "OK"
}
func main () {
	Args := os.Args
	var ConfInfo map[string]string
	NecessaryConf := strings.Fields("server execfile")
	ConfData := bytes.NewBuffer(nil)
	ConfInfo = make(map[string]string)

	for _,data := range Args {
		if data[:2] == "--"{
			Arr:=strings.Split(data[2:],"=")
			ConfInfo[Arr[0]] = Arr[1]
		}
	}
	for _,data :=range NecessaryConf{
		if ConfInfo[data] == ""{
			fmt.Printf("Error! \"--%s\" is necessary!\n",data)
			os.Exit(1)
		}
	}

	DeviceInfo := bytes.NewBuffer(nil)
	Code := GetRandCode()
	var DeviceName string
	if runtime.GOOS == "android"{
		DeviceName = AndroidGetprop("persist.sys.device_name")
	}else{
		DeviceName,_ = os.Hostname()
	}
	if ConfInfo["type"] == "" || len(ConfInfo["type"]) != 1{
		if runtime.GOOS == "windows"{
			ConfInfo["type"] = "0"
		}else if runtime.GOOS == "linux"{
			ConfInfo["type"] = "2"
		}else if runtime.GOOS == "android"{
			ConfInfo["type"] = "1"
		}else{
			ConfInfo["type"] = "4"
		}
	}


	DeviceInfo.Write(Code[0:16])
	DeviceInfo.Write([]byte(runtime.GOOS+","))
	DeviceInfo.Write([]byte(runtime.GOARCH+","))
	DeviceInfo.Write([]byte(DeviceName+","))
	DeviceInfo.Write([]byte(ConfInfo["type"]))

	PubKeyString := HttpGet(ConfInfo["server"]+"/GetRSAPubKey")
	EnDataBase64 := RSAEncrypt(DeviceInfo.Bytes(), PubKeyString)
	ID := HttpGet(ConfInfo["server"]+"/RegNewDevice?info=" + url.QueryEscape(EnDataBase64))
	IDInt,_ := strconv.Atoi(ID)
	EID := Int2Bytes(int32(IDInt))

	server := ConfInfo["server"]
	Pos :=strings.Index(server,":")
	if Pos!=-1{
		server = server[:Pos]
	}

	ServerIP := IPPort2Bytes(server)
	ConfData.Write(Code[0:16])//写到第16位
	ConfData.Write(EID[0:4])//写到第20位
	ConfData.Write(ServerIP[0:4])//写到第24位
	EmptyBytes := make([]byte, 32-ConfData.Len())
	ConfData.Write(EmptyBytes[0:32-ConfData.Len()])//补齐到32位
	result := WriteConf(ConfInfo["execfile"],ConfData.Bytes())
	fmt.Println(result)







}

