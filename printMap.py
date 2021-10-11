#!/usr/bin/env python3
import numpy as np
import os
from time import sleep

def printMap(list):
    os.system("clear")
    y, x= np.shape(list)
    startLine = "+" + ("-"*x) + "+"
    print(startLine)
    for i in range(y):
        print("|", end ="")
        for j in range(x):
            print(list[i,j], end ="")
        print("|")
    print(startLine)


printMap(np.array([[1,2,3],[4,5,6]]))
sleep(1)
printMap(np.array([[1,1,1],[2,2,2]]))
sleep(1)
printMap(np.array([[4,4,4],[3,3,3]]))
