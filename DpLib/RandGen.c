#include "RandGen.h"

double *randArr;

void genRand(size_t rowSize){
    init_genrand64(time(NULL));
    FILE *f;
    char filenameBuf[1024];
    double r;
    for(int i=0;i<COL_SIZE;i++){
        sprintf(filenameBuf,"rands/dp_random%lld.dat",i);
        f = fopen(filenameBuf,"wb");
        fwrite(&rowSize,sizeof(size_t),1,f);
        for(int i=0;i<rowSize;i++){
            r = genrand64_real2();
            fwrite(&r,sizeof(double),1,f);
        }
        fclose(f);
    }
}
void readRand(){
    init_genrand64(time(NULL));
    double r = genrand64_real1();
    char selectedFileName[1024];
    sprintf(selectedFileName,"rands/dp_random%lld.dat",(size_t)(r*COL_SIZE));
    size_t rowSize;
    FILE *f = fopen(selectedFileName,"rb");
    fread(&rowSize,sizeof(size_t),1,f);
    randArr = (double *)malloc(sizeof(double)*rowSize);
    fread(randArr,sizeof(double),rowSize,f);
    fclose(f);
}
double getRand(size_t pos){
    return randArr[pos];
}
void freeRand(){
    free(randArr);
}