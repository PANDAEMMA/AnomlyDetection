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
#This function should return a list of anomaly datas, if there is only 1, only one image will show
#TODO need to deliver multiple possible data ranges -- done
# top_k is the number of data which we want to return
# chunk_num is the number of partitions
# dataObj_i is the category of data index. e.g. TEMPER = 8
def AnalyzeData(fileObj, top_k, chunk_num, dataObj_i):
    anomalies = []
    index = []
    signal = []

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
	for j in range(N1):
		a = re.split(',|\n| ', buff.readline())
		temp_anomaly.append(float(a[dataObj_i]))
#	t = [i] * N1
#	r = [rank[i]] * N1
	# t is the index of top_k, e.g. 1, 2, 3, ...
	# index is the x-axis
	# r is the index of data chunk
	# temp_anomaly is the temperature in one data chunk
	# zipped output: e.g. (1, 0, 0, 23.2) (1, 0, 1, 24.2)
	zipped = zip(index, temp_anomaly)
	# clean the temp buffer
	temp_anomaly = []
	# return the number of top_k data chunk
	anomalies.append(zipped)
        fd.close()
    
    return anomalies

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

# Get the Top K index
def getTopKIndex(data, k):
        maxIndex = 0
        lst = []
        for j in range(k):
                lenn = len(data)
                for i in range(lenn):
                        if(data[i]>data[maxIndex]):
                                maxIndex = i
                lst.append(maxIndex)
                data.pop(i)
                maxIndex = 0
        return lst 

# Get Max Index
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
                                print NN
                                if (flag == 0):
                                        lst.append(t)
                                        flag = 1
                                        data.pop(maxIndex)
                maxIndex = 0
                print lst
        buf =[]
        return lst

def getMaxValue(data, maxIndex):
        return data[maxIndex]

# Standard Deviation calc.
def stderr(raw, model, N):
        std_k = 0.0
        for i in range(N):
                std_k = std_k + math.pow((raw[i] - model[i]), 2.0)
        return math.sqrt(std_k/(N - 1))

# Count the miss data
def miss_data_count(data, N):
        count = 0
        for i in range(N):
                if (data[i] == None):
                        count = count + 1
        return count

