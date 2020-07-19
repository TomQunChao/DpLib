import numpy as np
from matplotlib import pyplot as plt

if __name__ =="__main__":
    s = 6
    n = 8000
    # np.random.seed(10)

    randArr = [np.random.normal() for i in range(n)]
    maxr = max(randArr)
    minr = min(randArr)
    scope = [0,1,2,3,4,5]
    l = len(scope)
    sl = (maxr-minr)/(l-1)
    data = [ scope[int((randArr[i]-minr)/sl)] for i in range(n)]

    dpData = []
    p = 0.9


    for d in data:
        if np.random.random()<p:
            dpData.append(d)
        else:
            dpData.append((d+1)%s)

    h = [0 for i in range(s)]
    dph = [0 for i in range(s)]
    for i in range(n):
        h[data[i]]+=1
        dph[dpData[i]]+=1
    print(np.asarray(h)/n)
    print(np.asarray(dph)/n)
    dif = [(h[i]*p+h[(i-1)%s]*(1-p)) for i in range(len(h))]
    dif = [dif[i]-dph[i] for i in range(len(dif))]
    print(np.asarray(dif)/n)
    # plt.show()
