g++ main.cpp -lpthread -lz -o IEMP_Client -static -s -O2

#-static
upx IEMP_Client #arm64下请勿upx
python3 AddConfig.py IEMP_Client
echo "IEMP_Client Compile Success!"