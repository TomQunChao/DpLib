from data import *
import pandas as pd
import numpy as np
from dp import *
from matplotlib import pyplot as plt

def dpProcList(data:list,typeList:list,isProc:list,p:float,floatSeg:int):
    dproc = DataProer()
    return dproc.procAll(data,typeList,isProc,p,floatSeg),dproc

def dpProcFile(data:str,typeList:str,isProc:str,p,floatSeg:int):
    data = pd.read_csv(data)
    data = np.array(data).tolist()
    # print(data)
    typeList = pd.read_csv(typeList)
    typeList = np.array(typeList).tolist()[0]
    # print(typeList)
    isProc = pd.read_csv(isProc)
    isProc = np.array(isProc).tolist()[0]
    # print(isProc)
    for i in range(len(isProc)):
        isProc[i] = bool(isProc[i])
    return dpProcList(data,typeList,isProc,p,floatSeg)

def testDp(dpProc,p,n):
    dpData = dpProc.dpDataNo
    data = dpProc.dataNo
    lScope = dpProc.lScope
    
    nScope = dpProc.nScope

    xlabels = ["ip","segment no.","segment no.","segment no."]
    ylabel = "rate"
    print("The difference between theoretical and experimental values")
    for i in range(len(lScope)):
        h = [0 for i in range(lScope[i])]
        dph = [ 0 for i in range(lScope[i])]
        difh = []
        for j in range(len(data[i])):
            h[data[i][j]]+=1
            dph[dpData[i][j]]+=1
        for j in range(len(h)):
            difh.append(h[j]*p+h[(j-1)%lScope[i]]*(1-p))
        h = np.asarray(h)/n
        dph = np.asarray(dph)/n
        difh = np.asarray(difh)/n-dph
        
        print(difh)
        
        plt.subplot(1,2,1)
        x = [nScope[i][k] for k in range(len(h))]
        plt.bar(x,h)
        plt.xlabel(xlabels[i])
        plt.ylabel(ylabel)
        plt.subplot(1,2,2)
        plt.bar(x,dph)
        plt.xlabel(xlabels[i])
        plt.ylabel(ylabel)
        plt.show()

if __name__ == "__main__":
    n = 10000
    p=0.7
    genRand(1000000) # 生成随机数耗时较长，生成一次就可以了
    scope = [
        ["ip1","ip2","ip3","ip4","ip5","ip6","ip7"],
        [0,200],
        [-90,90],
        [-180,180]
    ]
    typeList = ["int","float","float","float"]
    randArr = [[np.random.normal() for i in range(n)] for j in range(len(scope))]
    rawData = [[] for i in range(len(scope))]

    for i in range(len(scope)):
        rarr = randArr[i]
        l = len(rarr)
        maxr = max(rarr)
        minr = min(rarr)

        if typeList[i]=="int":
            sl = (maxr-minr)/len(scope[i])
            for j in range(l):
                ind = (rarr[j]-minr)/sl
                if ind >= len(scope[i]):
                    ind-=1
                rawData[i].append(scope[i][int(ind)])
        elif typeList[i] == "float":
            for j in range(l):
                ind = (rarr[j]-minr)/(maxr-minr)*(scope[i][1]-scope[i][0])+scope[i][0]
                rawData[i].append(ind)
    isProc = [True,True,True,True]

    rawData = np.transpose(np.asarray(rawData)).tolist()
    print("rawData:")
    print(rawData)
    res,dpProc = dpProcList(rawData,typeList,isProc,p,20)
    print("resData:")
    print(res)
    testDp(dpProc,p,n)

    
    