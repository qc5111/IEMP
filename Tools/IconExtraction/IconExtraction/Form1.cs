using Microsoft.Win32;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace IconExtraction
{
    public partial class Form1 : Form
    {
        [DllImport("User32.dll")]
        public static extern int PrivateExtractIcons(
            string lpszFile, //文件名可以是exe,dll,ico,cur,ani,bmp
            int nIconIndex,  //从第几个图标开始获取
            int cxIcon,      //获取图标的尺寸x
            int cyIcon,      //获取图标的尺寸y
            IntPtr[] phicon, //获取到的图标指针数组
            int[] piconid,   //图标对应的资源编号
            int nIcons,      //指定获取的图标数量，仅当文件类型为.exe 和 .dll时候可用
            int flags        //标志，默认0就可以，具体可以看LoadImage函数
        );
        public Form1()
        {
            InitializeComponent();
        }
        private bool SaveICONAsPNG(string Path, int ID, string SavePath) {
            IntPtr[] hIcons = new IntPtr[1];
            PrivateExtractIcons(Path, ID, 256, 256, hIcons, null, 1, 0);
            if (hIcons[0] == IntPtr.Zero) {
                return false;
            }
            //MessageBox.Show(SuccessCount.ToString());

            Icon ico = Icon.FromHandle(hIcons[0]);
            Bitmap IconSave = ico.ToBitmap();
            IconSave.Save(SavePath, ImageFormat.Png);
            //MessageBox.Show("SaveOK");
            return true;
        }
        
        private void button1_Click(object sender, EventArgs e)
        {
            const string SavePath = "D:\\Desktop\\Desktop1_20210817\\图标提取\\temp\\";

            
            RegistryKey CLASSES_ROOT = Registry.LocalMachine.OpenSubKey(@"SOFTWARE\\Classes\\");
            object SubKeyValue;
            RegistryKey SubKeyValue2;
            string[] ICOPathListArray;
            foreach (string keyname in CLASSES_ROOT.GetSubKeyNames()) {
                //Console.WriteLine(keyname.Substring(0, 1));
                if (keyname.Substring(0, 1) == "."){
                    //Console.WriteLine("Pass");
                    SubKeyValue = CLASSES_ROOT.OpenSubKey(keyname).GetValue("");
                    if (SubKeyValue != null) {

                        SubKeyValue2 = CLASSES_ROOT.OpenSubKey(SubKeyValue.ToString() + "\\DefaultIcon");
                        if (SubKeyValue2 != null)
                        {
                            ICOPathListArray = SubKeyValue2.GetValue("").ToString().Replace("\"", "").Replace("@", "").Replace("\\\\", "\\").Split(',');
                            if (ICOPathListArray.Length == 2){
                                //Console.WriteLine(keyname);
                                //Console.WriteLine(ICOPathListArray[0]+"|||"+ ICOPathListArray[1]);
                                if (!SaveICONAsPNG(ICOPathListArray[0], int.Parse(ICOPathListArray[1]), SavePath + keyname + ".png")) {
                                    Console.WriteLine("Fail!:" + keyname + ", " + ICOPathListArray[0] + ", " + ICOPathListArray[1]);

                                }
                            }
                            else
                            {
                                //Console.WriteLine(ICOPathListArray[0]);
                                if (!SaveICONAsPNG(ICOPathListArray[0], 0, SavePath + keyname + ".png"))
                                {
                                    Console.WriteLine("Fail!:" + keyname + ", " + ICOPathListArray[0] + ", 0");

                                }
                            }


                        }
                        SaveICONAsPNG("C:\\Windows\\System32\\SHELL32.dll", 4, SavePath + ".folder.png");
                        
                        //Console.WriteLine();
                        //MessageBox.Show();
                    }

                }


            }
                







            string Path = "C:\\Program Files (x86)\\Microsoft Office\\Root\\VFS\\Windows\\Installer\\{90160000-000F-0000-0000-0000000FF1CE}\\xlicons.exe";
            int ID = 0;
            //SaveICONAsPNG(Path, ID, SavePath + "xlsx.png");



        }
    }
}
