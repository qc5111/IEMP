on_install() {
	ui_print "欢迎安装IEMP安卓客户端"
	ui_print "- 正在释放文件"
	unzip -o "$ZIPFILE" "system/*" -d $MODPATH >&2
	unzip -o "$ZIPFILE" "service.sh" -d $MODPATH >&2
	chmod +x $MODPATH/system/IEMP_Client
	chmod +x $MODPATH/service.sh
}