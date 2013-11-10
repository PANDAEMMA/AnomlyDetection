#! /usr/bin/env python

import sys
import os
import math 
import fileinput
import StringIO

from numpy import *
from numpy.fft import *
import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt
from time import clock, time

from ADParse import *

phi = (1 + math.sqrt(5)) / 2
resphi = 2 - phi
RANK = 5

#def f(x):
#        return x * sin(x) - 2 * cos(x)

def goldenSectionSearch(f, a, b, c, tau):
	if(c - b > b - a):
		x = b + resphi * (c - b)
	else:
		x = b - resphi * (b - a)
#	print a, b, c, x, f[(int)(x)], f[(int)(b)]
	if (math.fabs(c - a)) < tau * (math.fabs(b) + math.fabs(x)):
		return (c + a) /2
	assert f[x] != f[b]
	if(f[x] < f[b]):
		if (c - b > b - a):
			return goldenSectionSearch(f, b, x, c, tau)
		else:
			return goldenSectionSearch(a, x, b, tau)
	else:
		if (c - b > b - a):
			return goldenSectionSearch(a, b, x, tau)
		else:
			return goldenSectionSearch(x, b, c, tau)

# Calc the number of data in a big data, and not read in all data once
def calc_file(f_Obj):
	data_num = 0
	for line in fileinput.input(f_Obj):
		data_num = data_num + 1
	return data_num

# Calc the number of chunk in one file
def calc_numC(chunkComp, N):
        if ((N % chunkComp) == 0):
                N1 = (int)(N/chunkComp)
        else:
                N1 = (int)(N/chunkComp) + 1
	return N1

# Calc the bytes of each chunk
def calc_chunk(f_Obj, chunkComp, N1):
	# d_Size is used to record the bytes of each chunk
	d_Size=[]
	for i in range(N1):
		dataSize = 0
		for j in range(chunkComp):
			dataSize = len(f_Obj.readline()) + dataSize
		d_Size.append(dataSize)
	return d_Size
def readInChunks(f_Obj, dataSize):
	# Calc data size of one chunk line by line
	data = f_Obj.read(dataSize)
	return data

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

def stderr(raw, model, N):
	std_k = 0.0
	for i in range(N):
		std_k = std_k + math.pow((raw[i] - model[i]), 2.0)
	return math.sqrt(std_k/(N - 1))

def getTopKIndex(data, k):
        maxIndex = 0
	lst = []
	buf = []
	N = len(data)
	for x in range(N):
		buf.append(data[x])
	for j in range(k):
        	lenn = len(data)
        	for i in range(lenn):
            		if((float)(data[i])>(float)(data[maxIndex])):
				maxIndex = i
		flag = 0
		for t in range(N):
			if ((float)(buf[t]) == (float)(data[maxIndex])):
				NN = len(lst)
				if (flag == 0):
               				lst.append(t)
					flag = 1
					data.pop(maxIndex)
		maxIndex = 0
	buf =[]
        return lst

def getMaxIndex(data):
        maxIndex = 0
        lenn = len(data)
        for i in range(lenn):
            if(data[i]>data[maxIndex]):
                maxIndex = i
        return maxIndex

def getMaxValue(data, maxIndex):
        return data[maxIndex]

def getExtremedata_index(anomaly, chunk_index, k):
	temp = []
	#it = [item[2] for item in res_data[chunk_index]]
	#an = [item[3] for item in res_data[chunk_index]]
	#top = getTopKIndex(an, 3)
	#for i in range(len(top)):
	#	temp.append(an[top[i]])
	#zipped = zip(top, temp)
	#temp = []
	#return zipped

def read_out(fd, d_list, k):
	seek_size = 0
	for i in range(k):
        	seek_size = seek_size + d_list[i]
        fd.seek(seek_size)
        res_data = readInChunks(fd, d_list[k])
	return res_data

def miss_data_count(data, N):
	count = 0
	for i in range(N):
		if (data[i] == None):
			count = count + 1
	return count

if __name__ == '__main__':
	fileObj = 'slcc.txt'
	fd = open(fileObj, 'r')
	signal=[]

	# N is the total number of data in a file
        N = calc_file(fileObj)
	# The assigned number of data group
	chunk_num = 9
        # chunkComp is the number of data in one chunk
        chunkComp = N / chunk_num
	# top k
	top_k = 3
	# Divide
	# d_list is the bytes of each data chunk
        d_list = calc_chunk(fd, chunkComp, chunk_num)

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
			if (a[TEMPER]):
				input_data.append((float)(a[TEMPER]))
        
		N1 = len(input_data)
		#Calculate model
		model = FFT_Model(input_data, N1)
		#Calculate std between real data and model data
		std = stderr(input_data, model, N1)
		std_list.append(std)
	#Merge
	# Get the top k index of std data
	rank_i = getTopKIndex(std_list, top_k)
        fd.close()
	index = range(N1)
	anomalies = []
	res_data = []
	# Read out the suspect data
	for i in range(top_k):
		fd = open(fileObj, 'r')
		out_data = read_out(fd, d_list, rank_i[i])
		buff = StringIO.StringIO(out_data)
                for j in range(N1):
			a = re.split(',|\n| ', buff.readline())
                        anomalies.append(float(a[TEMPER]))
#		t = [i] * N1
#		r = [rank_i[i]] * N1
                zipped = zip(index, anomalies)
		anomalies = []
		res_data.append(zipped)
		fd.close()
	it = getExtremedata_index(res_data, 2, 1)
	print res_data[0]
	# Got the max Index in one certain range of data
'''
	max_data = []
	buff = StringIO.StringIO(out_data)
	for i in range(chunkComp):
		max_data.append(float(buff.readline()))
	max_i = getMaxIndex(max_data)
	max_v = getMaxValue(max_data, max_i)
'''
