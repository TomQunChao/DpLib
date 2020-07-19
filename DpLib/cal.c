#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "RandGen.h"

#define DATA_BLOCK 8096
#define THRES_HOLD 8096

struct {
    int xlen;
    int ylen;
    int *lenList;
    int *data;
    int *res;
    double p;
}d;
typedef struct{
    size_t x;
    size_t len;
} ProArg;

// 用这个函数处理一小片x:起始地址，len：长度
void *pro(void *v){
    ProArg *pa = (ProArg *)v;
    // printf("x=%d,len=%d,lenlist=%d\n",pa->x,pa->len,d.lenList[(pa->x)/d.ylen]);
    for(int i=0;i<pa->len;i++){
        double r = getRand(pa->x+i);
        // printf("random[%d]=%f\n",pa->x+i,r);
        if(r>=d.p){
            d.res[pa->x+i] = (d.data[pa->x+i]+1)%d.lenList[(pa->x+i)/d.ylen];
        }else{
            d.res[pa->x+i] = d.data[pa->x+i];
        }
    }
}
void multiPro(){
    size_t len = ((d.ylen+DATA_BLOCK-1)/DATA_BLOCK)*d.xlen;
    printf("Thread units: %d\n",len);
    fflush(stdout);
    pthread_t *proThreads = (pthread_t *)malloc(sizeof(pthread_t)*len);
    ProArg *threadsArgs = (ProArg *)malloc(sizeof(ProArg)*len);
    size_t rowThreaNum = (d.ylen+DATA_BLOCK-1)/DATA_BLOCK;
    for(size_t i=0;i<len;i++){
        size_t threadX = i%rowThreaNum;
        threadsArgs[i].x = i%rowThreaNum*DATA_BLOCK+i/rowThreaNum*d.ylen;
        if(i%rowThreaNum==rowThreaNum-1){
            threadsArgs[i].len = d.ylen-i%rowThreaNum*DATA_BLOCK;
        }else{
            threadsArgs[i].len = DATA_BLOCK;
        }
        pthread_create(&proThreads[i],NULL,pro,&threadsArgs[i]);
    }
    for(size_t i=0;i<len;i++){
        pthread_join(proThreads[i],NULL);
    }
    free(proThreads);
    free(threadsArgs);

}
void dpProcess(int xlen,int ylen,int lenList[],int data[],int res[],float p){
    d.xlen = xlen;
    d.ylen = ylen;
    d.lenList = lenList;
    d.data = data;
    d.res = res;
    d.p = p;
    // printf("xlen=%d,ylen=%d,len[0]=%d,d.p=%f,p=%f\n",d.xlen,d.ylen,d.lenList[0],d.p,p);
    // printf("%d %d\n",d.xlen,d.ylen);
    // for(int i=0;i<xlen;i++){
    //     printf("%d\n",lenList[i]);
    // }
    fflush(stdout);
    if(xlen*ylen<THRES_HOLD){
        ProArg pa;
        pa.x = 0;
        pa.len = xlen*ylen;
        pro((void *)&pa);
    }else{
        multiPro();
    }
}