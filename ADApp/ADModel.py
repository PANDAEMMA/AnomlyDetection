#----------------------------------------------
#
# The anomaly data analysis model
# 1. FFT, 2 Golden section search
#
#----------------------------------------------
import math
import fileinput
import StringIO
import re

from numpy import *
from numpy.fft import *
import numpy as np
import heapq

from math import sqrt

from File import *


phi = (1 + math.sqrt(5)) / 2
resphi = 2 - phi
RANK = 5

# FFT calculation
def fft_model(signal, N):
        sp = fft(signal, N)
        return sp

# return the top k maximum index
def top_k_index(data, RANK):
        index = [t[0] for t in heapq.nlargest(RANK, enumerate((abs)(data)), lambda t: t[1])]
        return index

# return the top k maximum value
def top_k_value(data, RANK):
        value = heapq.nlargest(RANK, data)
        return value

# return max index
def max_index(data):
        return data.argmax()

# least square
def least_square(signal, Ind, RANK, N):
        a = []
        for j in range(RANK):
                sum_1 = 0.0
                sum_2 = 0.0
                for i in range(N):
                        x = (cos(2*pi*((i*Ind[j]))/N)+sin(2*pi*((i*Ind[j]))/N))
                        sum_1 = sum_1 + x * signal[i]
                        sum_2 = sum_2 + x * x
                a.append(sum_1/sum_2)
        return a

# Superposition
def superposition(a, Ind, RANK, N):
        r = [0]*int(N)
        for j in range(RANK):
                for i in range(N):
                     r[i] = r[i]+a[j]*(cos(2*pi*((i*Ind[j]))/N)+sin(2*pi*((i*Ind[j]))/N))
        return r

# Model builder
def FFT_Model(signal, N):
	# FFT: transform to frequency domain
        sp = fft_model(signal, N)

	# Obtain top _k frequency index
        index = top_k_index(sp, RANK)

	# Least square to obtain a -- y = ax + c
        a = least_square(signal, index, RANK, N)

	 # Superposition
        r = superposition(a, index, RANK, N)
        return r
    
# Maximizer Search algorithm
def goldenSectionSearch(f, a, b, c, tau):
    if (c - b > b - a):
        x = b + resphi * (c - b)
    else:
        x = b - resphi * (b - a)
    if (math.fabs(c - a) < tau * (math.fabs(b) + math.fabs(x))):
        return (c + a) /2
        assert f[x] != f[b]
        if(f[x] < f[b]):
            if (c - b > b - a):
                return goldenSectionSearch(f, b, x, c, tau)
            else:
                return goldenSectionSearch(f, a, x, b, tau)
        else:
            if (c - b > b - a):
                return goldenSectionSearch(f, a, b, x, tau)
            else:
                return goldenSectionSearch(f, x, b, c, tau) 


