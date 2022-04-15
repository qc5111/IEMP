import _thread
import platform
import os
import subprocess
import MainDB.models as DB


class Aria2c:
    def __init__(self):
        self.BasePath = DB.SateliteInfo.objects.get(Name="FileStoragePath").Value
        self.System = platform.system().lower()
        self.ExecName = self.BasePath + '/Aria2c/aria2c' + '-' + self.System + '-' + platform.machine().lower()
        if self.System == 'windows':
            Slash = '\\'
        else:
            Slash = '/'
        # 读取配置模板
        Fr = open(self.BasePath + '/Aria2c/aria2-template.conf', 'r')
        ConfTemplate = Fr.read()
        Fr.close()
        ConfTemplate = ConfTemplate.replace('{{BasePath}}', os.path.abspath(self.BasePath))
        ConfTemplate = ConfTemplate.replace('{{Aria2cDir}}', os.path.abspath(self.BasePath+"/Aria2c")+Slash)
        Fw = open(self.BasePath + '/Aria2c/aria2.conf', 'w')
        Fw.write(ConfTemplate)
        Fw.close()
        #检查session
        if not os.path.exists(self.BasePath + '/Aria2c/aria2.session'):
            open(self.BasePath + '/Aria2c/aria2.session', "w").close()
        # 启动新线程
        _thread.start_new_thread(self.StartAria2c, (self.ExecName,))

    def StartAria2c(self, ExecName):
        # 启动aria2c

        # os.system(ExecName + ' --conf-path=' + self.BasePath + '/Aria2c/aria2.conf')
        subprocess.run([os.path.abspath(ExecName), '--conf-path=' + os.path.abspath(self.BasePath + "/Aria2c/aria2.conf")], shell=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=1)
