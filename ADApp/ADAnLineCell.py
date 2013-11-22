#!/usr/bin/python
#---------------------------------------------
#
# ADAnLineCell.py
# Anonamly data analysis in line graph cell
# Plot: 1. anomaly data 
# Label: 1. std, 2. avg, 3. date, 4. corr
#
#---------------------------------------------

import math
import fileinput
import StringIO
import re

from ADModel import *
from File import *
from ADParse import *

#from scipy.stats.stats import pearsonr

# the anomaly data in each cell (top_k = 6, partition = 10)
# dataObj_i is the category of data index. e.g. TEMPER = 8
def AnalyzeData(fileObj, dataObj_i):
    anomalies = []
    index = []
    signal = []

    top_k = 4
    chunk_num = 4

    fd = open(fileObj, 'r')
    # N is the total number of data in a file
    N = calc_file(fileObj)

    # chunkComp is the number of data in one chunk
    chunkComp = N / chunk_num

    # Divide
    # d_list is the bytes of each data chunk
    d_list = calc_chunk(fd, chunkComp, N)
    # Note: Should close the file, and open it again
    fd.close()

    fd = open(fileObj, 'r')
    std_list = []
    for i in range(chunk_num):
    # Conquer
        result = readInChunks(fd, d_list[i])
        buf = StringIO.StringIO(result)
        input_data = []
        for i in range(chunkComp):
                a = re.split(',|\n| ', buf.readline())
                if (a[dataObj_i]):
                        input_data.append(float(a[dataObj_i]))

        N1 = len(input_data)
        #Calculate model
        model = FFT_Model(input_data, N1)
        #Calculate std between real data and model data
        std = stderr(input_data, model, N1)
        std_list.append(std)
    #Merge
    # Get the number of top k index of std data
    rank_i = getTopKIndex(std_list, top_k)
    fd.close()

    index = range(N1)
    # Read out the suspect data
    temp_anomaly = []
    for i in range(top_k):
        fd = open(fileObj, 'r')
        # seek to the particular file position, and read data out
        out_data = read_out(fd, d_list, rank_i[i])
        buff = StringIO.StringIO(out_data)
	date = []
        for j in range(N1):
                a = re.split(',|\n| ', buff.readline())
                temp_anomaly.append(float(a[dataObj_i]))
		date.append(a[YEAR]+'-'+a[MON]+'-'+a[DAY]+'-'+a[HOUR]+':'+a[MIN])
        zipped = zip(index, temp_anomaly, date)
        # clean the temp buffer
        temp_anomaly = []
	date = []
        # return the number of top_k data chunk
        anomalies.append(zipped)
        fd.close()

    return anomalies


# avg calculation in each line graph cell
def avg(data, N):
	aveg = 0.0
	for i in range(N):
		aveg = aveg + data[i]
	return aveg/N

# std calculation in each line graph cell
def stdcal(data, N):
	average = avg(data, N)
	std_sum = 0.0
	for i in range(N):
		std_sum = std_sum + math.pow((data[i] - average), 2.0)
	return math.sqrt(std_sum/(N - 1))

# Calculate pearson correlation 
'''def corr(x, y):
	cov = pearsonr(x, y)
	return cov[0]'''
	
	
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
