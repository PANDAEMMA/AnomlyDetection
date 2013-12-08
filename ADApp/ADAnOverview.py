#!/usr/bin/python
#---------------------------------------------
#
# ADAnOverview.py
# Show the overview data
# Plot: 1. monthly raw data 2. monthly model data
# 
#
#---------------------------------------------
import re
from ADParse import *

def get_miss_index_list(fileObj, cat_flag, year, month):
	if(month == -1):
		index = get_year_miss_index(fileObj, cat_flag, year)
	else:
		index = get_mon_miss_index(fileObj, cat_flag, year, month)
	return index

def get_mon_miss_index(fileObj, cat_flag, year, month):
        fd = open(fileObj, 'r')
        count = 0
	index = []
        for line in fd.readlines():
                a = re.split(',|\n| ', line)
		count = count + 1
                if (len(a[cat_flag]) == 0 and (int)(a[YEAR]) == year and (int)(a[MON]) == month):
                	index.append(count)
        fd.close()
        return index

def get_year_miss_index(fileObj, cat_flag, year):
        fd = open(fileObj, 'r')
        count = 0
	index = []
        for line in fd.readlines():
                a = re.split(',|\n| ', line)
		count = count + 1
                if (len(a[cat_flag]) == 0 and (int)(a[YEAR]) == year):
                        index.append(count)
        fd.close()
        return index

def get_year_size(fileObj, cat_flag, year):
	fd = open(fileObj, 'r')
	count = 0
	for line in fd.readlines():
                a = re.split(',|\n| ', line)
                if (len(a[cat_flag]) != 0 and (int)(a[YEAR]) == year):
			count = count + 1
	fd.close()
	return count
	
def get_x_axis(fileObj, cat_flag, year, month, length, chunk_num):
	if (month == -1):
		x_axis = get_year_x_axis(fileObj, cat_flag, year, length, chunk_num)
	else:
		x_axis = get_mon_x_axis(fileObj, cat_flag, year, month, length, chunk_num)
	return x_axis

def get_mon_x_axis(fileObj, cat_flag, year, month, length, chunk_num):
        fd = open(fileObj, 'r')
        file_len = 0
        count = 0
        count1 = 0
        index = []
        date = []
        for line in fd.readlines():
                a = re.split(',|\n| ', line)
                if (len(a[cat_flag]) != 0 and (int)(a[YEAR]) == year and (int)(a[MON]) == month):
                        file_len = file_len + 1
        fd.close()
        step = file_len / chunk_num
        fd = open(fileObj, 'r')
        for line in fd.readlines():
                a = re.split(',|\n| ', line)
                if (len(a[cat_flag]) != 0 and (int)(a[YEAR]) == year and (int)(a[MON]) == month):
                        if (count1 == count):
                                (int)((count1/file_len)*length)
                                ii = (int)(((float)(count1)/(float)(file_len))*length)
                                date.append(a[MON] + '/' + a[DAY] + '/' + a[YEAR])
                                index.append(ii)
                                count1 = count1 + step
                        count = count + 1
        zipp = zip(index, date)
        fd.close()
        return zipp

def get_year_x_axis(fileObj, cat_flag, year, length, chunk_num):
	fd = open(fileObj, 'r')
	file_len = 0
	count = 0
	count1 = 0
	index = []
	date = []
	for line in fd.readlines():
                a = re.split(',|\n| ', line)
                if (len(a[cat_flag]) != 0 and (int)(a[YEAR]) == year):
			file_len = file_len + 1
	fd.close()
	step = file_len / chunk_num
	fd = open(fileObj, 'r')
	for line in fd.readlines():
                a = re.split(',|\n| ', line)
                if (len(a[cat_flag]) != 0 and (int)(a[YEAR]) == year):
			if (count1 == count):
				(int)((count1/file_len)*length)
				ii = (int)(((float)(count1)/(float)(file_len))*length)
				date.append(a[MON] + '/' + a[DAY] + '/' + a[YEAR])
				index.append(ii)
				count1 = count1 + step
			count = count + 1
	zipp = zip(index, date)
	fd.close()
	return zipp
	

