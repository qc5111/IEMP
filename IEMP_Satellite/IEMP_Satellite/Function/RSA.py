import rsa
import base64
import MainDB.models as DB


def GenerateRSAkey():
    (pubkey, privkey) = rsa.newkeys(2048)  # 2048
    PriKey = base64.b64encode(privkey._save_pkcs1_der()).decode()
    PubKey = base64.b64encode(pubkey._save_pkcs1_der()).decode()
    return PriKey, PubKey


def RSAEncrypt(Data, PubKey=""):  # 不得大于245字节
    if PubKey == "":
        PubKey = DB.SateliteInfo.objects.get(Name="PubKey").Value

    PubKey = rsa.PublicKey._load_pkcs1_der(base64.b64decode(PubKey))
    return rsa.encrypt(Data, PubKey)


def RSADecrypt(Data, PriKey=""):
    if PriKey == "":
        PriKey = DB.SateliteInfo.objects.get(Name="PriKey").Value
    PriKey = rsa.PrivateKey._load_pkcs1_der(base64.b64decode(PriKey))
    return rsa.decrypt(Data, PriKey)

# PriKey, PubKey = GenerateRSAkey()

# Data1 = RSAEncrypt(b"AAAAAAAAAAAAAAAAAA")
# print(Data1)
# print(RSADecrypt(Data1))
