#include <Windows.h>   //使用HWND的头文件
int main(){
    HWND h;
    int mX = 0;
    int mY = 0;
    h = FindWindow("Notepad", NULL);
    SendMessage(h, WM_LBUTTONDOWN, VK_LBUTTON, mX + mY * 65536);
    SendMessage(h, WM_LBUTTONUP, 0, mX + mY * 65536);
}

