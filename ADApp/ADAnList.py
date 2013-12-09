#!/usr/bin/python

#---------------------------------------
# ADAnList.py
# The information showing in record list window for data clean
# 1. Miss data, 2. Extreme data, 3. Delete function
#
#---------------------------------------
import re
import heapq
from numpy import *
from ADParse import *

def CleanAnalyze(fileObj, mis_flag, year, month):
	clean_data = []
	miss_data = got_clean_missdata_list(fileObj, mis_flag, year, month)
	max_data = got_clean_maxdata_list(fileObj, mis_flag, year, month)
	min_data = got_clean_mindata_list(fileObj, mis_flag, year, month)
	if (len(miss_data) > 0):
		clean_data.extend(miss_data)
	if (len(max_data) > 0):
		clean_data.extend(max_data)
	if (len(min_data) > 0):
		clean_data.extend(min_data)
	return clean_data

# List down all the miss data
# return miss data with (ID, YEAR, MON, DAY, HOUR, MIN)
# Usage: get_all_missdata_list(fd, TEMPER)

def got_clean_missdata_list(fileObj, mis_flag, year, month):
	if(month == -1):
		miss_data = clean_year_missdata(fileObj, year, mis_flag)
	else:
		miss_data = clean_year_mon_missdata(fileObj, year, month, mis_flag)
        return miss_data

def got_clean_maxdata_list(fileObj, mis_flag, year, month):
	if(month == -1):
                max_data = clean_year_max_data(fileObj, year, mis_flag)
        else:
                max_data = clean_year_mon_max_data(fileObj, year, month, mis_flag)
        return max_data

def got_clean_mindata_list(fileObj, mis_flag, year, month):
        if(month == -1):
                min_data = clean_year_min_data(fileObj, year, mis_flag)
        else:
                min_data = clean_year_mon_min_data(fileObj, year, month, mis_flag)
        return min_data

def clean_year_max_data(fileObj, year, cat_flag):
	avg = clean_year_max_data_avg(fileObj, year, cat_flag)
	fd = open(fileObj, 'r')
        buf = []
	buf1 = []
	buf2 = []
	count = 0
        for line in fd.readlines():
                a = re.split(',|\n| ', line)
                if (len(a[cat_flag]) != 0 and (int)(a[YEAR]) == year):
                        if ((float)(a[cat_flag]) > avg):
				buf.append(a[MON]+'/'+a[DAY]+'/'+a[YEAR])
                                buf1.append((float)(a[cat_flag]))
        			buf2.append(count)
		count = count + 1
       	index = [0]*int(len(buf))
        max_data = zip(index, buf1, buf, buf2)
        buf = []
        buf1 = []
	buf2 = []
        fd.close()
        return max_data

def clean_year_min_data(fileObj, year, cat_flag):
        avg = clean_year_min_data_avg(fileObj, year, cat_flag)
        fd = open(fileObj, 'r')
        buf = []
        buf1 = []
	buf2 = []
	count = 0
        for line in fd.readlines():
                a = re.split(',|\n| ', line)
                if (len(a[cat_flag]) != 0 and (int)(a[YEAR]) == year):
                        if ((float)(a[cat_flag]) < avg):
                                buf.append(a[MON]+'/'+a[DAY]+'/'+a[YEAR])
                                buf1.append((float)(a[cat_flag]))
				buf2.append(count)
		count = count + 1
        index = [0]*int(len(buf))
        min_data = zip(index, buf1, buf, buf2)
        buf = []
        buf1 = []
	buf2 = []
        fd.close()
        return min_data

def clean_year_mon_max_data(fileObj, year, mon, cat_flag):
        avg = clean_year_max_data_avg(fileObj, year, cat_flag)
        fd = open(fileObj, 'r')
        buf = []
        buf1 = []
	buf2 = []
	count = 0
        for line in fd.readlines():
                a = re.split(',|\n| ', line)
                if (len(a[cat_flag]) != 0 and (int)(a[YEAR]) == year and (int)(a[MON]) == mon):
                        if ((float)(a[cat_flag]) > avg):
                                buf.append(a[MON]+'/'+a[DAY]+'/'+a[YEAR])
                                buf1.append((float)(a[cat_flag]))
				buf2.append(count)
		count = count + 1
        index = [0]*int(len(buf))
        max_data = zip(index, buf1, buf, buf2)
        buf = []
        buf1 = []
	buf2 = []
        fd.close()
        return max_data

def clean_year_mon_min_data(fileObj, year, mon, cat_flag):
        avg = clean_year_min_data_avg(fileObj, year, cat_flag)
        fd = open(fileObj, 'r')
        buf = []
        buf1 = []
	buf2 = []
	count = 0
        for line in fd.readlines():
                a = re.split(',|\n| ', line)
                if (len(a[cat_flag]) != 0 and (int)(a[YEAR]) == year and (int)(a[MON]) == mon):
                        if ((float)(a[cat_flag]) < avg):
                                buf.append(a[MON]+'/'+a[DAY]+'/'+a[YEAR])
                                buf1.append((float)(a[cat_flag]))
				buf2.append(count)
		count = count + 1
        index = [0]*int(len(buf))
        min_data = zip(index, buf1, buf, buf2)
        buf = []
        buf1 = []
	buf2= []
        fd.close()
        return min_data

def clean_year_min_data_avg(fileObj, year, cat_flag):
        count = 0
        flag = 0
        year_data = []
        fd = open(fileObj, 'r')
        for line in fd.readlines():
                a = re.split(',|\n| ', line)
                # Notice the None value
                if ((int)(a[YEAR]) == year):
                        if (len(a[cat_flag]) != 0):
                                year_data.append((float)(a[cat_flag]))
                                count = count + 1
        length = (int)(count * RATE)
        value = heapq.nsmallest(length, year_data)
        avg = mean(value)
        year_data = []
        fd.close()
        return avg

def clean_year_max_data_avg(fileObj, year, cat_flag):
	count = 0
        flag = 0
        year_data = []
        fd = open(fileObj, 'r')
        for line in fd.readlines():
                a = re.split(',|\n| ', line)
                # Notice the None value
                if ((int)(a[YEAR]) == year):
                        if (len(a[cat_flag]) != 0):
                                year_data.append((float)(a[cat_flag]))
				count = count + 1
        length = (int)(count * RATE)
        value = heapq.nlargest(length, year_data)
        avg = mean(value)
        year_data = []
        fd.close()
        return avg

def clean_year_missdata(fileObj, year, mis_flag):
	temp = 0
        miss_count = 0
        flag = 0
        count = 0
        buf = []
	buf1 = []
	buf2 = []
        fd = open(fileObj, 'r')
        for line in fd.readlines():
                a = re.split(',|\n| ', line)
                if (len(a[mis_flag]) == 0 and (int)(a[YEAR]) == year):
                       buf.append(a[MON]+'/'+a[DAY]+'/'+a[YEAR])
                       buf1.append('')
		       buf2.append(count)
		count = count + 1
        index = [2]*int(len(buf))
        missdata = zip(index, buf1, buf, buf2)
        buf = []
        buf1 = []
	buf2 = []
        fd.close()
        return missdata

def clean_year_mon_missdata(fileObj, year, mon, mis_flag):
        temp = 0
        miss_count = 0
        flag = 0
        count = 0
        buf = []
        buf1 = []
	buf2 = []
        fd = open(fileObj, 'r')
        for line in fd.readlines():
                a = re.split(',|\n| ', line)
                if (len(a[mis_flag]) == 0 and (int)(a[YEAR]) == year and (int)(a[MON]) == mon):
                       buf.append(a[MON]+'/'+a[DAY]+'/'+a[YEAR])
                       buf1.append('')
		       buf2.append(count)
		count = count + 1
        index = [2]*int(len(buf))
        missdata = zip(index, buf1, buf, buf2)
        buf = []
        buf1 = []
        fd.close()
        return missdata


