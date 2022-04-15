#include <iostream>
#include <Windows.h>   //使用HWND的头文件
using namespace std;
int main()
{
    HWND h,h2,h3,h4;
    h = FindWindowExA(NULL, NULL, NULL,"BOOTICE v1.3.3 x64 - by Pauly");
    h2 = FindWindowExA(h, NULL, NULL,"UEFI");
    h3 = FindWindowExA(h2, NULL, NULL,"&Edit boot entries");

    PostMessage(h3, WM_LBUTTONDOWN, 0, 0);
    PostMessage(h3, WM_LBUTTONUP, 0, 0);


    cout << hex << h << endl;
    cout << hex << h2 << endl;
    cout << hex << h3 << endl;
}
