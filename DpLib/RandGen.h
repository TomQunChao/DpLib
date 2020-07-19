#include "mt64.h"
#include <time.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define COL_SIZE 10

double getRand(size_t pos);
void readRand();
void freeRand();
void genRand(size_t rowSize);