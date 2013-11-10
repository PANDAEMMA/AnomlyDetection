import math
import fileinput
import StringIO

from numpy import *
from numpy.fft import *

from File import *

phi = (1 + math.sqrt(5)) / 2
resphi = 2 - phi

#This function should return a list of anomaly datas, if there is only 1, only one image will show
#TODO need to deliver multiple possible data ranges -- done
# top_k is the number of data which we want to return
# chunk_num is the number of partitions
def AnalyzeData(fileObj, top_k, chunk_num):
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
                input_data.append(float(buf.readline()))

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
		temp_anomaly.append(float(buff.readline()))
	t = [i] * N1
	r = [rank[i]] * N1
	# t is the index of top_k, e.g. 1, 2, 3, ...
	# index is the x-axis
	# r is the index of data chunk
	# temp_anomaly is the temperature in one data chunk
	zipped = zip(t, r, index, temp_anomaly)
	# clean the temp buffer
	temp_anomaly = []
	# return the number of top_k data chunk 
	anomalies.append(zipped)
        fd.close()
    
    return anomalies

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
def getMaxIndex(data):
        maxIndex = 0
        lenn = len(data)
        for i in range(lenn):
            if(data[i]>data[maxIndex]):
                maxIndex = i
        return maxIndex

# Get Max Value
def getMaxValue(data, maxIndex):
        return data[maxIndex]

# Standard Deviation calc.
def stderr(raw, model, N):
        std_k = 0.0
        for i in range(N):
                std_k = std_k + math.pow((raw[i] - model[i]), 2.0)
        return math.sqrt(std_k/(N - 1))

