using Microsoft.Win32;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading;
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

            Icon ico = Icon.FromHandle(hIcons[0]);
            
            Bitmap IconSave = ico.ToBitmap();
            
            //pictureBox1.Image = IconSave;
            IconSave.Save(SavePath, ImageFormat.Png);
            //MessageBox.Show("SaveOK");
            ico.Dispose();
            IconSave.Dispose();
            return true;
        }
        
        private void button1_Click(object sender, EventArgs e)
        {
            string SavePath = "D:\\Desktop\\Desktop1_20210817\\Pygame\\";
            SaveICONAsPNG("D:\\Desktop\\Desktop1_20210817\\Pygame\\Graphics\\y.ico", 0, SavePath + "test.png");

            return;
            SavePath = ".\\Icons\\";
            if (!Directory.Exists(SavePath)){
                Directory.CreateDirectory(SavePath);
            }
            

            
            RegistryKey CLASSES_ROOT = Registry.LocalMachine.OpenSubKey(@"SOFTWARE\\Classes\\");
            object SubKeyValue;
            RegistryKey SubKeyValue2;
            string[] ICOPathListArray;
            //SaveICONAsPNG("C:\\Windows\\System32\\imageres.dll", 85, SavePath + ".pdf.png");
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




                        //Console.WriteLine();
                        //MessageBox.Show();
                    }

                }


            }
            SaveICONAsPNG("C:\\Windows\\System32\\SHELL32.dll", 4, SavePath + ".folder.png");
            SaveICONAsPNG("C:\\Windows\\System32\\imageres.dll", 2, SavePath + ".empty.png");
            SaveICONAsPNG("C:\\Windows\\System32\\imageres.dll", 11, SavePath + ".exe.png");
            SaveICONAsPNG("C:\\Windows\\System32\\imageres.dll", 85, SavePath + ".pdf.png");
            SaveICONAsPNG("C:\\Windows\\System32\\SHELL32.dll", 29, SavePath + ".lnk.png");







        }
    }
}
