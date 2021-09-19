#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import random as rnd
import math

# ----------------
#   FUNCTIONS
# ----------------

def n(x, mu, sig):
    return 1/math.sqrt(2*math.pi)*sig*math.exp((-(1/2))*((x-mu)**2/sig**2))

def p(x):
    return 0.3*n(x, 2, 1)+0.4*n(x, 5, 2)+0.3*n(x, 9, 1)

def q_Uni(x):
    return 1/16

def cum_Normalize(w, k):
    res = np.zeros(k)
    wSum = sum(w)

    # calculate normalized weights and acummulate them
    res[0] = w[0]/wSum
    for i in range(1,k):
        res[i] = w[i]/wSum + res[i-1]
    return res

def uni_Sampler(k, proposal):
    w   = np.zeros(k)
    res = np.zeros(k)

    #Importance
    for i in range(k):
        w[i] = p(proposal[i])/q_Uni(proposal[i])
    w_norm = cum_Normalize(w, k)

    #Resampling
    for i in range(k):
        rand = np.random.sample(1)
        for j in range(k):
            if (rand <= w_norm[j]):
                res[i] = proposal[j]
                break
    res.sort()
    return res

def norm_Sampler(k, proposal):
    w   = np.zeros(k)
    x   = np.zeros(k)
    res = np.zeros(k)

    #Importance
    for i in range(k):
        w[i] = p(proposal[i])/n(proposal[i], 5, 4)
    w_norm = cum_Normalize(w, k)

    #Resampling
    for i in range(k):
        rand = np.random.sample(1)
        for j in range(k):
            if (rand <= w_norm[j]):
                res[i] = proposal[j]
                break
    res.sort()
    return res

# ----------------
#   END FUNCTIONS
# ----------------

# ----------------
#   Plotting spørgsmål 1
# ----------------
def make_Uni_plot(k, title):
    #Selecting positions from the uniform distribution
    proposal = np.random.uniform(low=0.0, high=15.0, size = k)
    res = uni_Sampler(k, proposal)
    #Plotting
    plt.figure(1)
    ax1 = plt.subplot(211)
    plt.hist(proposal, label='Uniform distribution', color='red')
    plt.hist(res, label='Nye samples', color='blue')
    plt.legend()
    plt.title(title)
    plt.subplot(212, sharex=ax1)
    y = np.zeros(100)
    x = np.linspace(0,15,100)
    for i in range(100):
        y[i] = p(x[i])
    plt.plot(x,y, label='Robottens potentielle position')
    plt.legend()
    plt.show()


make_Uni_plot(20, "20 particles, Uniform distribution")
make_Uni_plot(100, "100 particles, uniform distribution")
make_Uni_plot(1000, "1000 particles, Uniform distribution")

# ----------------
#   END Plotting spørgsmål 1
# ----------------

# ----------------
#   Plotting spørgsmål 2
# ----------------
def make_norm_plot(k, title):
    #Selecting positions from normal distribution
    proposal = np.random.normal(5, 4, size = k)
    res = norm_Sampler(k, proposal)

    plt.figure(1)
    ax1 = plt.subplot(211)
    plt.hist(proposal, label='Normal distribution', color='red')
    plt.hist(res, label='Nye samples', color='blue')
    plt.legend()
    plt.title(title)
    plt.subplot(212, sharex=ax1)
    y = np.zeros(100) 
    x = np.linspace(-10,20,100)
    for i in range(100):
        y[i] = n(x[i], 5, 4) 
    plt.plot(x,y, label='Robottens potentielle position')
    plt.legend()
    plt.show()

# ----------------
#   END Plotting spørgsmål 2
# ----------------

# ----------------
#   MAIN
# ----------------
make_norm_plot(20, "20 particles, normal distributed")
make_norm_plot(100, "100 particles, normal distributed")
make_norm_plot(1000, "1000 particles, normal distributed")
