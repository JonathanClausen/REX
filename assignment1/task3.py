#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import random as rnd
import math

def n(x, mu, sig):
    n = 1/math.sqrt(2*math.pi)*sig*math.exp((-(1/2))*((x-mu)**2/sig**2))
    return n

def p(x):
    return 0.3*n(x, 2, 1)+0.4*n(x, 5, 2)+0.3*n(x, 9, 1)

def q(x):
    return 1/16

    # 0.3*np.random.normal(2,1)+0.4*np.random.normal(5,2)+0.3*np.random.normal(9,1)
    # return x

def sampler(Size):
    uni = np.random.uniform(low=0.0, high=15.0, size=Size)
    pVal   = np.zero(Size)
    w   = np.zero(Size)
    res = np.zero(Size)

    for i in range(Size):
        pVal[i] = p(uni[i])
        w[i] = pVal[i]/q(i)


        # her efter var jeg træt tag intet for givet
    sum = 0
    for i in range(Size):
        for j in range(Size):
            rand = rnd(0.0, 1.0)
            sum = sum + w[j]
            if (sum > rand):
                res[j] = res[j]+1



    plt.plot(uni, )
    plt.show()
