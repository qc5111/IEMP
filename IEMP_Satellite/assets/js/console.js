function OpenConsole(EID){
    let TermDIV = document.getElementById('terminal')
    let term = new Terminal();
    let fitAddon = new FitAddon.FitAddon();
    let OPSystem = 1;
    term.loadAddon(fitAddon);
    ws = new WebSocket("ws://" + document.domain + ":48285/consolews/?EID="+EID);
    term.open(TermDIV);
    fitAddon.fit();

     term.onKey(e => {
         ws.send(e.key);
         //如果为退格键
         if (OPSystem === 0) {
             if(e.key === '\x7F') {
                 term.write('\b \b');

             }else if(e.key === "\x03"){

             }
             else{
                 term.write(e.key);
             }
         }



     })
    ws.onmessage = async function (evt) {
        //blob转换成字符串

        if (typeof(evt.data)=== "string"){//指令
            let Order = JSON.parse(evt.data);
            OPSystem = Order.OPSystem;
        }else if (typeof(evt.data) === "object"){//写入控制台
            let str = await evt.data.text();
            term.write(str);
        }


    };

     return{
         term:term,
         ws:ws
     }
}

function getQueryString(name) {
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
        var r = window.location.search.substr(1).match(reg);
        if (r != null) return unescape(r[2]);
        return null;
    }