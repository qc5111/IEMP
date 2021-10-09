::objcopy -I binary -O elf64-x86-64 -B i386 config.txt config.o
::g++ -c .\main.cpp -s -O2
g++ main.cpp uac.res -lws2_32 -lpthread -lz -static   -o IEMP_Client.exe -s -O2
UPX IEMP_Client.exe
python AddConfig.py IEMP_Client.exe
::g++ .\main.cpp uac.res -lws2_32 -o a.exe  -mwindows config.o  
pause
::a.exe
::pause