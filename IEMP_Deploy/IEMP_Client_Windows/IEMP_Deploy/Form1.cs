using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Net;
using System.Reflection;
using System.Security.Cryptography;
using System.Text;
using System.Windows.Forms;

namespace IEMP_Deploy
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            textBoxUsername.Text = ".\\" + Environment.UserName;
        }
        private string RunCmd(string Order)
        {
            Process p = new Process();
            p.StartInfo.FileName = "cmd.exe";
            p.StartInfo.UseShellExecute = false;
            p.StartInfo.RedirectStandardInput = true;
            p.StartInfo.RedirectStandardOutput = true;
            p.StartInfo.CreateNoWindow = true;
            p.Start();
            //p.StandardInput.WriteLine("echo off");
            p.StandardInput.WriteLine(Order+ "&exit");
            p.StandardInput.AutoFlush = true;
            string strOuput = p.StandardOutput.ReadToEnd();
            p.WaitForExit();
            p.Close();
            return strOuput;
        }
        public static String CreateGetHttpResponse(string url)
        {
            HttpWebRequest request = WebRequest.Create(url) as HttpWebRequest;
            request.Method = "GET";
            Stream ResultStream = request.GetResponse().GetResponseStream();
            StreamReader ResultReader = new StreamReader(ResultStream, Encoding.UTF8);
            return ResultReader.ReadToEnd();

            //return  as HttpWebResponse;
        }


        static public string RSA_Encrypt(string str_Plain_Text, out string str_Public_Key, out string str_Private_Key)
        {
            str_Public_Key = "";
            str_Private_Key = "";
            UnicodeEncoding ByteConverter = new UnicodeEncoding();
            byte[] DataToEncrypt = ByteConverter.GetBytes(str_Plain_Text);
            try
            {
                RSACryptoServiceProvider RSA = new RSACryptoServiceProvider();
                str_Public_Key = Convert.ToBase64String(RSA.ExportCspBlob(false));
                str_Private_Key = Convert.ToBase64String(RSA.ExportCspBlob(true));

                //OAEP padding is only available on Microsoft Windows XP or later. 
                byte[] bytes_Cypher_Text = RSA.Encrypt(DataToEncrypt, false);
                str_Public_Key = Convert.ToBase64String(RSA.ExportCspBlob(false));
                str_Private_Key = Convert.ToBase64String(RSA.ExportCspBlob(true));
                string str_Cypher_Text = Convert.ToBase64String(bytes_Cypher_Text);
                return str_Cypher_Text;
            }
            catch (CryptographicException e)
            {
                Console.WriteLine(e.Message);
                return null;
            }
        }










        private void button1_Click(object sender, EventArgs e)
        {
            String PubKey = CreateGetHttpResponse("http://127.0.0.1:800/GetRSAPubKey");

            //RSACryptoServiceProvider rsa = new RSACryptoServiceProvider();
            RSACryptoServiceProvider rsa = new RSACryptoServiceProvider();
            byte[] test = Convert.FromBase64String(PubKey);
            String PubKey1,PriKey1;
            RSA_Encrypt("Test", out PubKey1, out PriKey1);
            Console.WriteLine(PubKey1);
// rsa.ImportCspBlob(test);
// Console.WriteLine(rsa.ExportCspBlob(false));

            return;
            byte[] ConfigLocate;

            //Assembly assm = Assembly.GetExecutingAssembly();
            //Stream istr = assm.GetManifestResourceStream("IEMP_Deploy.Resources.config.txt");
            //BinaryReader Br = new BinaryReader(istr);
            //ConfigLocate = Br.ReadBytes(32);
            //Console.WriteLine(ConfigLocate);
            //Br.Close();
            ConfigLocate = global::IEMP_Deploy.Properties.Resources.config;
            foreach (byte b in ConfigLocate) {
                //Console.WriteLine(b.ToString("X2") + " ");
            }
            string subPath = "C:\\IEMP_Client";
            if (System.IO.Directory.Exists(subPath) == false)
            {
                System.IO.Directory.CreateDirectory(subPath);
            }

            byte[] Buffer;
            //assm = Assembly.GetExecutingAssembly();
            //istr = assm.GetManifestResourceStream("IEMP_Deploy.Resources.IEMP_Client.exe");
            //Br = new BinaryReader(istr);
            //System.IO.StreamReader sr = new System.IO.StreamReader(istr);
            //string str = sr.ReadLine();
            //MessageBox.Show(str);

            Buffer = global::IEMP_Deploy.Properties.Resources.IEMP_Client;
            int ConfLenNow, ConfLen, FileLenNow, FileLen, TheSameLen;
            ConfLen = ConfigLocate.Length;
            FileLen = Buffer.Length;
            FileLenNow = 0;
            ConfLenNow = 0;
            TheSameLen = 0;
            String Positions = "";
            String[] PositionsSplit;
            while (true) {

                if (ConfLenNow == ConfLen) {
                    //Console.WriteLine("Jump Out");
                    Positions += (FileLenNow - TheSameLen - 1).ToString() + "," + TheSameLen.ToString() + ",";
                    //Console.WriteLine(Positions);
                    break;
                }
                TheSameLen = 0;
                if (Buffer[FileLenNow] == ConfigLocate[ConfLenNow]) {
                    TheSameLen++;
                    while (true) {
                        FileLenNow++;
                        ConfLenNow++;
                        if (ConfLenNow == ConfLen) {
                            break;
                        }
                        if (Buffer[FileLenNow] == ConfigLocate[ConfLenNow])
                        {
                            TheSameLen++;
                            //Console.WriteLine(FileLenNow);
                            //Console.WriteLine(TheSameLen);
                        } else {
                            if (TheSameLen > 4) {
                                Positions += (FileLenNow - TheSameLen).ToString() + "," + TheSameLen.ToString() + ",";
                                TheSameLen = 0;
                                //Console.WriteLine(Positions);
                            }
                            if (Buffer[FileLenNow + 4] == ConfigLocate[ConfLenNow]) {
                                FileLenNow += 4;
                                TheSameLen++;
                                //Console.WriteLine(FileLenNow);
                            } else {
                                break;
                            }
                        }
                    }
                } else {
                    ConfLenNow = 0;
                }
                if (FileLenNow + 1 == FileLen) {
                    break;
                }
                FileLenNow++;
            }
            Console.WriteLine(Positions);

            /*for(int i = 47492; i < 47492 + 9; i++)
            {
                Console.WriteLine(Buffer[i].ToString("X2") + " ");

            }
            
            for (int i = 47505; i < 47505 + 23; i++)
            {
                Console.WriteLine(Buffer[i].ToString("X2") + " ");

            }*/











            PositionsSplit = Positions.Split(',');
            byte[] NewConfig = ConfigLocate;
            
            for(int i = 0; i < 32; i++)
            {
                NewConfig[i] = ((byte)i);

            }
            int PositionsSplitPOS = 0;
            int NowPos,RunPos;
            RunPos = 0;
            NowPos = int.Parse(PositionsSplit[PositionsSplitPOS]);
            for (int i = 0;i< NewConfig.Length; i++)
            {
                Console.WriteLine(NewConfig[i].ToString("X2") + " ");
                
                Buffer[NowPos] = NewConfig[i];
                Console.WriteLine(NowPos);
                RunPos += 1;
                NowPos += 1;
                if (RunPos == int.Parse(PositionsSplit[PositionsSplitPOS + 1])){
                    Console.WriteLine("Break1");
                    PositionsSplitPOS += 2;
                    if(PositionsSplitPOS + 1 == PositionsSplit.Length)
                    {
                        break;
                    }
                    NowPos = int.Parse(PositionsSplit[PositionsSplitPOS]);
                    RunPos = 0;
                }
            }

            Console.WriteLine("------------------------");



            BinaryWriter Bw = new BinaryWriter(new FileStream("C:\\IEMP_Client\\IEMP_Client.exe", FileMode.Create));
            Bw.Write(Buffer);
            /*while(true)
            {
                Buffer = Br.ReadBytes(8192);
                if(Buffer.Length == 0)
                {
                    break;
                }
                Bw.Write(Buffer);
            }
            Br.Close();
             */


            Bw.Close();
            MessageBox.Show("OK");
            return;
            string Result,Out1,Out2;
            if (textBoxPassword.Text == ""){
                Out1 = RunCmd("sc create IEMPClient binpath= \"C:\\IEMP_Client\\IEMP_Client.exe\" type= own start= auto displayname= IEMPClient obj= " + textBoxUsername.Text);
            }
            else{
                Out1 = RunCmd("sc create IEMPClient binpath= \"C:\\IEMP_Client\\IEMP_Client.exe\" type= own start= auto displayname= IEMPClient obj= " + textBoxUsername.Text + " password= " + textBoxPassword.Text);
            }
            //p.StandardInput.WriteLine();
            Out2 = RunCmd("net start IEMPClient");
            //MessageBox.Show(Out1);
            MessageBox.Show(Out1.Remove(0, Out1.IndexOf("[SC")));

        }


    }
}
