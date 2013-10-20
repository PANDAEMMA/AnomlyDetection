import math

phi = (1 + math.sqrt(5)) / 2
resphi = 2 - phi

#This function should return a list of anomaly datas, if there is only 1, only one image will show
#TODO need to deliver multiple possible data ranges
def AnalyzeData(filePath):
    anomalies = []
    arr = []
    index = []
    signal = []
    threadhold = 20
    # OpenFile, and read data out
    fd = open(filePath, 'r')
    for line in fd.readlines():
        arr.append(line.strip('\n'))
    # Convert data into float
    N = len(arr)
    for i in range(N):
        signal.append(float(arr[i]))
    
    # Search the extreme
    result = goldenSectionSearch(signal, 1, N/2, N, 1)

    zipped = zip(index, signal)
    temp = []
    count = 0
    for i in range(result - threadhold, result + threadhold, 1):
        index.append(count)
        count = count + 1
        temp.append(signal[i])
    zipped = zip(index, temp)

    #zipped is only one anomaly
    anomalies.append(zipped)
    
    return anomalies
        
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