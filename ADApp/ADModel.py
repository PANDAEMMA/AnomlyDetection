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

from File import *


phi = (1 + math.sqrt(5)) / 2
resphi = 2 - phi
RANK = 5

# Model builder
def FFT_Model(signal, N):
        sp = fft(signal, N)
        b = sorted(abs(sp), key=lambda x: (x.real),reverse=True)
        Ind = [0]*int(RANK)

        for i in range(RANK):
                for j in range(N):
                        if  (int)(b[i]) == (int)(abs(sp[j])):
                                if i > 0:
                                        if Ind[i - 1] != j:
                                                Ind[i] = j
                                else:
                                        Ind[i] = j

        a_1 = [0]*int(RANK)
        a_2 = [0]*int(RANK)
        r = [0]*int(N)
        sum_1 = 0.0
        sum_2 = 0.0
        for j in range(RANK):
                for i in range(N):
                        x = (cos(2*pi*((i*Ind[j]))/N)+sin(2*pi*((i*Ind[j]))/N))
			sum_1 = sum_1 + x * signal[i]
                        sum_2 = sum_2 + x * x
                a_2[j] = sum_1/sum_2
                sum_1 = 0.0
                sum_2 = 0.0

        for j in range(RANK):
                for i in range(N):
                        r[i] = r[i]+a_2[j]*(cos(2*pi*((i*Ind[j]))/N)+sin(2*pi*((i*Ind[j]))/N))

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


