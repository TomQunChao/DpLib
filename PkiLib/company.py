
from ca import *
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
import os

'''
厂商软件的结构：
{
    id:"",
    data:"",//软件
    sign:"",//签名
    cert:"",//证书
}
'''
class company(object):
    def __init__(self,id,ca):
        self.id = id
        self.software = "This is a software"
        # 向CA申请证书
        self.ca = ca
        sign = ca.sign(self.software)
        self.sign = sign
    
    # 用户调用此方法下载软件
    def download(self,name):
        
        return self.software,self.sign
    def getCa(self):
        return self.ca

if __name__ == "__main__":
    # ca = CA("ca1")
    # c = company("comp1",ca)
    # software,sign= c.download("")
    # print(software,sign)
    # ca = c.getCa()
    # res = ca.vertify(software,sign)
    # print(res)
    res = os.popen("gmssl version").read()
    print(res)
    