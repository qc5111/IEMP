set ws=WScript.CreateObject("WScript.Shell")
wscript.sleep 1000
Dim Fso,shell
Set Fso = WScript.CreateObject("Scripting.FileSystemObject")
Set shell = Wscript.createobject("wscript.shell")
Fso.DeleteFile"Update.vbs"
Fso.DeleteFile"IEMP_Client.exe"
Fso.MoveFile"IEMP_ClientNew.exe","IEMP_Client.exe"
shell.run "IEMP_Client.exe"
