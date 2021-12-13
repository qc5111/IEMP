g++ main.cpp -lpthread -lz -o IEMP_Client -static -s -O2

#-static
upx IEMP_Client.out #arm64下请勿upx
python3 AddConfig.py IEMP_Client.out
./IEMP_Client.out