#!/usr/bin/env python3
import numpy as np

def printMap(list):
    y, x= np.shape(list)
    startLine = "+" + ("---+"*x)
    print(startLine)
    for i in range(y):
        print("|", end="")
        for j in range(x):
            print('{:>3}|'.format(list[i,j]), end="")
        print()
    print(startLine)
    print()


    printMap(np.array([[4,4,4],[3,3,3]]))
