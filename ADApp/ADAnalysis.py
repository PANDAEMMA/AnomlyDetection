#!/usr/bin/python
#---------------------------------------------
#
# Anonamly data analysis
#
#---------------------------------------------

import math
import fileinput
import StringIO
import re


# Objective: Residual calc. to determinate k possible abnormal regions
def stderr(raw, model, N):
        std_k = 0.0
        for i in range(N):
                std_k = std_k + math.pow((raw[i] - model[i]), 2.0)
        return math.sqrt(std_k/(N - 1))

# Return (index, extreme_data) in each chunk of data
# anomaly: the anomaly list
# chunk_index: the index of ceil (index of top_k)
# k: the number of exetreme data
# usage: getExtremedata_index(anomaly, 0, 2) 
def getExtremedata_index(anomaly, chunk_index, k):
        temp = []
        it = [item[2] for item in res_data[chunk_index]]
        an = [item[3] for item in res_data[chunk_index]]
        top = getTopKIndex(it, k)
        for i in range(len(top)):
                temp.append(an[top[i]])
        zipped = zip(top, temp)
        temp = []
        return zipped

def getTopKIndex(data, k):
        lst = []
        N = len(data)
        buf = []
        for i in range(N):
                buf.append((float)(data[i]))
        for j in range(k):
                maxdata = max(buf)
                for t in range(N):
                        if (data[t] == maxdata):
                                lst.append(t)
                buf.remove(maxdata)
        buf = []
        return lst

def getMaxIndex(data):
        maxIndex = 0
        lenn = len(data)
        for i in range(lenn):
            if(data[i]>data[maxIndex]):
                maxIndex = i
        return maxIndex

def getMaxIndex(data):
        maxIndex = 0
        lenn = len(data)
        for i in range(lenn):
            if(data[i]>data[maxIndex]):
                maxIndex = i
        return maxIndex

def getMinIndex(data):
        minIndex = 0
        lenn = len(data)
        for i in range(lenn):
            if(data[i] < data[minIndex]):
                minIndex = i
        return minIndex

def getMaxValue(data, maxIndex):
        return data[maxIndex]
