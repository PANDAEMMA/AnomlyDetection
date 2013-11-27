#!/usr/bin/python

#---------------------------------------
#
# Input data definition and parse
#
#---------------------------------------

import sys
import re

MON = 0  # Month index
DAY = 1  # Day index
YEAR = 2 # Year index
HOUR = 4 # Hour index
MIN = 5  # Minute index
TEMPER = 8 # Temperature index
HUMID = 9  # Humidity index
PRESS = 10  # Pressure index

WEEK_DAY  = 7 # Number of day per week

RATE = 0.01	# The ratio of extreme data (ADAnRecord.py)
# Get data in a specific index
def get_data_all(fd, flag):
	arr = []
	for line in fd.readlines():
		a = re.split(',|\n| ', line)
		if (a[flag]):
			arr.append((float)(a[flag]))
	return arr

# Counting the number of data hourly, daily, yearly
def get_num_index(fd, flag):
	num_index = []
	count = 0
	temp = 0
	for line in fd.readlines():
		a = re.split(',|\n| ', line)
		if (temp != (int)(a[flag]) and temp != 0):
			num_index.append(count)
			count = 0
		count = count + 1
		temp = (int)(a[flag])
	num_index.append(count)
	return num_index	

# Get the number of year in the data
def get_num_year(fd, flag):
	count = 0
	temp = 0
	for line in fd.readlines():
                a = re.split(',|\n| ', line)
		if(temp != (int)(a[flag])):
			count = count + 1
		temp = (int)(a[flag])
	return count

# Get weekly index		
def get_num_week_index(fd, flag):
	count = 0
	result = get_num_index(fd, flag)
	step = WEEK_DAY
	week_index = []
	N = len(result)
	for i in range(0, N, step):
		if ((N - i) > step):
			for j in range(step):
				count = count + result[i + j]
			week_index.append(count)
			count = 0
			
		else:
			for k in range(i, N - i, 1):
				count = count + result[k]
			if (count != 0):
				week_index.append(count)
	return week_index

def get_year_daily_num(a, flag, start, stop):
        num_index = []
        count = 0
        temp = 0
        for i in range(start, stop):
                if (temp != (int)(a[flag]) and temp != 0):
                        num_index.append(count)
                        count = 0
                count = count + 1
                temp = (int)(a[flag])
        num_index.append(count)
        return num_index

	
