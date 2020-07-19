from Crypto.PublicKey import RSA
import json
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_PSS

'''
证书用json格式存储
证书结构：
{
    id:"",      //厂商ID
    pubKey:"",  //公钥
    vertified:"",//认证类型，可能为none/dp/(其他类型)
    ca:""       //认证机构
}
'''

class CA(object):
    def __init__(self,id):
        key = RSA.generate(2048)
        prv = key.exportKey()
        pub = key.publickey().exportKey()
        self.prv = prv
        self.pub = pub
        self.key = key
        self.id = id
    def sign(self,data):
        h = SHA256.new()
        h.update(data.encode('utf-8'))
        rsaSign = PKCS1_PSS.new(self.key)
        res = rsaSign.sign(h)
        return res

    def vertify(self,data,sign):
        h = SHA256.new()
        h.update(data.encode('utf-8'))
        rsaSign = PKCS1_PSS.new(self.key)
        res = rsaSign.verify(h,sign)

        return res

    def getPubKey(self):
        return self.pub

    def __str__(self):
        return self.id
