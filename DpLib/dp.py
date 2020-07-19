import numpy as np
import ctypes as ct
from matplotlib import pyplot as plt

def dp(data:list,scope:list,p:float):
    
    randGen = ct.cdll.LoadLibrary(r"./librandgen.so")
    randGen.readRand()
    callib = ct.cdll.LoadLibrary(r"./libcal.so")
    xlen = len(data)
    if xlen == 0:
        return None
    ylen = len(data[0])
    tdata = ct.c_uint32*(xlen*ylen)
    d = tdata()
    tlen = ct.c_uint32*xlen
    l = tlen()
    for i in range(xlen):
        l[i] = scope[i]
        for j in range(ylen):
            d[i*ylen+j] =data[i][j]
    callib.dpProcess(xlen,ylen,l,d,d,ct.c_float(p))
    dpDataNo = [[0 for j in range(ylen)] for i in range(xlen)]
    for i in range(xlen):
        for j in range(ylen):
            dpDataNo[i][j] = d[i*ylen+j]
    randGen.freeRand()
    # testAcc(data,dpDataNo,p)
    return dpDataNo

def genRand(rowSize:int):
    randGen = ct.cdll.LoadLibrary(r"./librandgen.so")
    randGen.genRand(rowSize)

def testAcc(data,dpData,p):
    s = 7
    h = [0 for i in range(s)]
    dph = [0 for i in range(s)]
    data = data[0]
    n = len(data)
    dpData = dpData[0]
    for i in range(n):
        h[data[i]]+=1
        dph[dpData[i]]+=1
    print(p)
    dif = [(h[i]*p+h[(i-1)%s]*(1-p)) for i in range(len(h))]
    dif = [dif[i]-dph[i] for i in range(len(dif))]
    print(sum(np.asarray(data)-np.asarray(dpData)))
    print("tessAcc:",np.asarray(dif)/n)

if __name__ == "__main__":
    s = 6
    n = 80000
    # np.random.seed(10)

    randArr = [np.random.normal() for i in range(n)]
    maxr = max(randArr)
    minr = min(randArr)
    scope = [0,1,2,3,4,5]
    l = len(scope)
    sl = (maxr-minr)/(l-1)
    data = [ scope[int((randArr[i]-minr)/sl)] for i in range(n)]

    dpData = []
    p = 0.7

    dpData = dp([data],[s],p)
    print(sum((np.asarray(dpData)-np.asarray([data])).tolist()[0]))
    h = [0 for i in range(s)]
    dph = [0 for i in range(s)]
    dpData = dpData[0]
    for i in range(n):
        h[data[i]]+=1
        dph[dpData[i]]+=1
    print(np.asarray(h)/n)
    print(np.asarray(dph)/n)
    dif = [(h[i]*p+h[(i-1)%s]*(1-p)) for i in range(len(h))]
    dif = [dif[i]-dph[i] for i in range(len(dif))]
    print(np.asarray(dif)/n)
    