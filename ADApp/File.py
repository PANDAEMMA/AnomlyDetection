import sys
import fileinput
import StringIO

def FileRead(path):
	arr = []
	signal = []
	fd = open(path, 'r')
	for line in fd.readlines():
                arr.append(line.strip('\n'))
        # Convert data into float
        N = len(arr)
        for i in range(N):
                signal.append(float(arr[i]))
	return signal
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
        data = f_Obj.read(dataSize).strip('\n')
        return data
	
# Seek to file position, and read it out
def read_out(fd, d_list, k):
        seek_size = 0
	for i in range(k):
        	seek_size = seek_size + d_list[i]
        fd.seek(seek_size)
        res_data = readInChunks(fd, d_list[k])
        return res_data
