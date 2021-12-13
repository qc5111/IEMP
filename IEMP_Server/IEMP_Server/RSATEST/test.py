import rsa
import base64
 
# rsa加密
def rsaEncrypt(str):
    # 生成公钥、私钥
    print("KeyStart")
    (pubkey, privkey) = rsa.newkeys(1024)
    print(pubkey._save_pkcs1_pem())
    
    print(base64.b64encode(pubkey._save_pkcs1_der()).decode())
    
    print(len(pubkey._save_pkcs1_der()))
    print(privkey._save_pkcs1_der())
    print(len(privkey._save_pkcs1_der()))
    # rsa.key.PublicKey
    print(type(pubkey))
    print("公钥:\n%s\n私钥:\n:%s" % (pubkey, privkey))
    # 明文编码格式
    content = str.encode("utf-8")
    # 公钥加密
    crypto = rsa.encrypt(content, pubkey)
    return (crypto, privkey)
 
 
# rsa解密
def rsaDecrypt(str, pk):
    # 私钥解密
    content = rsa.decrypt(str, pk)
    con = content.decode("utf-8")
    return con
 
 
if __name__ == "__main__":
 
    str, pk = rsaEncrypt("hello")
    print("加密后密文：\n%s" % str)
    content = rsaDecrypt(str, pk)
    print("解密后明文：\n%s" % content)