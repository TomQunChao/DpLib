import numpy as np
from dp import *
import ctypes as ct

class DataProer(object):
    rawData = None
    typeList = None
    scope = None
    floatSeg = None
    dpData = None
    dataDict = None
    dataNo = None
    # 保存所有可能的取值
    nScope = None
    # 每一个数据类型范围的长度
    lScope = None
    isProc = None
    dpDataNo = None

    def __init__(self):
        pass
        
    def getScope(self,rawData:list,typeList:list):
        self.rawData = rawData
        self.typeList = typeList
        l1 = len(rawData[0])
        l2 = len(rawData)
        dpData = np.transpose(np.asarray(rawData)).tolist()
        scope = []
        for i in range(l1):
            scope.append([])
            if typeList[i] == "float":
                for j in range(l2):
                    dpData[i][j] = float(dpData[i][j])
                scope[i].append(min(dpData[i]))
                scope[i].append(max(dpData[i]))
            elif typeList[i] == "int":
                scope[i]=list(set(dpData[i]))
        self.dpData = dpData
        self.scope = scope
        return dpData,scope

    def getDict(self,typeList:list,scope:list,floatSeg:int):
        self.typeList = typeList
        self.scope = scope
        self.floatSeg = floatSeg
        dataDict = []
        nScope = []
        lScope = []
        l1 = len(scope)
        
        for i in range(l1):
            if typeList[i] == "float":
                scope[i].append(floatSeg)
                nScope.append([ j for j in range(floatSeg+1)])
                lScope.append(floatSeg+1)
            elif typeList[i] == "int":
                nScope.append(scope[i])
                lScope.append(len(scope[i]))
        # 随机置换
        for i in range(l1):
            l2 = len(nScope[i])
            for j in range(l2):
                p = np.random.randint(j,l2)
                tmp = nScope[i][p]
                nScope[i][p] = nScope[i][j]
                nScope[i][j] = tmp

        for i in range(l1):
            l2 = len(nScope[i])
            dataDict.append({})
            for j in range(l2):
                dataDict[i][nScope[i][j]] = j
        self.dataDict = dataDict
        self.lScope = lScope
        self.nScope = nScope
        return dataDict,lScope,nScope   # nScope供恢复数据用

    def getDataNo(self,dpData:list,typeList:list,scope:list,dataDict:dict):
        self.dpData = dpData
        self.typeList = typeList
        self.scope = scope
        self.dataDict = dataDict
        l1 = len(dpData)
        l2 = len(dpData[0])
        dataNo = []
        for i in range(l1):
            dataNo.append([])
            if typeList[i] == "float":
                sc = scope[i]
                sl = (sc[1]-sc[0])/sc[2]
                for j in range(l2):
                    dataNo[i].append(int((dpData[i][j]-sc[0])/sl))
            elif typeList[i] == "int":
                for j in range(l2):
                    dataNo[i].append(dataDict[i][dpData[i][j]])
        self.dataNo = dataNo
        return dataNo

    def parseDataNo(self,dataNo:list,typeList:list,nScope:list,scope:list):
        self.dataNo = dataNo
        self.typeList = typeList
        self.nScope = nScope
        self.scope = scope
        l1 = len(dataNo)
        l2 = len(dataNo[0])
        res = []
        for i in range(l1):
            res.append([])
            nsc = nScope[i]
            if typeList[i] == "float":
                sc = scope[i]
                sl = (sc[1]-sc[0])/sc[2]
                for j in range(l2):
                    res[i].append(nsc[int(dataNo[i][j])]*sl+sc[0])
            elif typeList[i] == "int":
                for j in range(l2):
                    res[i].append(nsc[dataNo[i][j]])
        # 转置
        res = np.transpose(np.asarray(res)).tolist()
        for i in range(l1):
            if typeList[i] == "float":
                for j in range(l2):
                    res[j][i] = float(res[j][i])
        return res
    def procAll(self,rawData:list,typeList:list,isProc:list,p:float,floatSeg:int):
        needProcData = []
        rawData = np.transpose(np.asarray(rawData)).tolist()
        for i in range(len(isProc)):
            if isProc[i]:
                needProcData.append(rawData[i])
        rawData = np.transpose(np.asarray(rawData)).tolist()
        needProcData = np.transpose(np.asarray(needProcData)).tolist()
        self.getScope(needProcData,typeList)
        self.getDict(self.typeList,self.scope,floatSeg)
        self.getDataNo(self.dpData,self.typeList,self.scope,self.dataDict)
        self.dpDataNo = dp(self.dataNo,self.lScope,p)
        return self.parseDataNo(self.dataNo,self.typeList,self.nScope,self.scope)


    
# if __name__ == "__main__":
#     rawData = [
#         [ i for i in range(10000)],
#         ["ok %d"%i for i in range(10000)],
#         [i+200 for i in range(10000)]
#     ]
#     rawData = np.transpose(np.asarray(rawData)).tolist()
#     typeList = ["float","int"]
#     isProc = [True,True,False]
#     # genRand(10000000) # 生成较多随机数时需要较长时间，只生成一次就可以了
#     readRand()
#     dproc = DataProer()
#     # print(rawData)
#     print(dproc.procAll(rawData,typeList,isProc,0.7))
#     freeRand()

    
