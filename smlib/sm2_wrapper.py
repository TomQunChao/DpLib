import os

def genKey():
    os.popen("gmssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:sm2p256v1 \
                -out signkey.pem")
    os.popen("gmssl pkey -pubout -in signkey.pem -out vrfykey.pem")

def userPlusFile(username:str,filename:str):
    result = os.popen("gmssl sm3 "+filename)
    result = result.read()
    result = username+result.split()[1]
    result = os.popen("echo -n "+ result+ " | gmssl sm3")
    result = result.read()
    result = result.split()[1]
    return result
def sign(username:str,filename:str):
    result = userPlusFile(username,filename)
    result = os.popen("echo -n "+result+" | gmssl pkeyutl -sign -pkeyopt ec_scheme:sm2 -inkey signkey.pem \
                -out "+filename+".sig")

def vertify(username:str,filename:str,sigfile:str):
    result = userPlusFile(username,filename)
    result = os.popen("echo -n "+result+" | gmssl pkeyutl -verify -pkeyopt ec_scheme:sm2 -pubin -inkey vrfykey.pem \
                -sigfile "+sigfile)
    result = result.read()
    return result

if __name__ == '__main__':
    genKey()
    sign("tom","sm2_wrapper.py")
    result = vertify("tom","sm2_wrapper.py","sm2_wrapper.py.sig")
    print(result)