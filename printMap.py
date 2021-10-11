#!/usr/bin/env python3
import numpy as np

def printMap(list):
    y, x= np.shape(list)
    startLine = "+" + ("---+"*x)
    print(startLine)
    for i in range(y):
        print("|", end="")
        for j in range(x):
            print(round(list[i,j],1), end ="|")
        print()
    print(startLine)
    print()

printMap(np.array([[4.555,4.555,4.555],[3.555,3.555,3.555]]))
