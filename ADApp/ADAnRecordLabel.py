#!/usr/bin/python

import heapq
from numpy import *
from ADParse import *

#-----------------------------------------------
# ADAnRecordLabel.py
# The analysis results showing in each Record cells
# Data: 1. Miss data count. 2. Max data avg. count 3. Min data avg count
# Plot: 1. x-axis ratio of each item in one month
#
#------------------------------------------------

# Objective: Count the number of maximum data each year
# Usage: count_year_max_data_avg(fileObj, max_data_avg, cat_flag)
# Return: [12, 3, 53, 21]
def count_year_max_data(fileObj, aa, cat_flag):
	fd = open(fileObj, 'r')
        count = 0
        flag = 0
        ccount = 0
        count_data = []
        for line in fd.readlines():
                a = re.split(',|\n| ', line)
                if (len(a[cat_flag]) != 0):
                        if ((float)(a[cat_flag]) > (float)(aa[ccount])):
                                count = count + 1
                if (flag == 0):
                        temp = (int)(a[YEAR])
                        flag = 1
                if(temp != (int)(a[YEAR])):
                        count_data.append(count)
                        count = 0
                        ccount = ccount + 1
                temp = (int)(a[YEAR])
	fd.close()
        return count_data

# Objective: Count the number of minimum data each year
# Usage: count_year_min_data_avg(fileObj, max_data_avg, cat_flag)
# Return: [12, 3, 53, 21]
def count_year_min_data(fileObj, aa, cat_flag):
	fd = open(fileObj, 'r')
        count = 0
        flag = 0
        ccount = 0
        count_data = []
        for line in fd.readlines():
                a = re.split(',|\n| ', line)
                if (len(a[cat_flag]) != 0):
                        if ((float)(a[cat_flag]) < (float)(aa[ccount])):
                                count = count + 1
                if (flag == 0):
                        temp = (int)(a[YEAR])
                        flag = 1
                if(temp != (int)(a[YEAR])):
                        count_data.append(count)
                        count = 0
                        ccount = ccount + 1
                temp = (int)(a[YEAR])
	fd.close()
        return count_data

# Objective: List down the year
# Usage: get_year(fileObj, YEAR)
# Return: [1997, 1998, 1999, 2000]
def get_year(fileObj, cat_flag):
        year = []
        temp_year = 0
        for line in fd.readlines():
                a = re.split(',|\n| ', line)
                if (len(a[cat_flag]) != 0):
                        if ((int)(a[cat_flag]) != temp_year):
                                year.append((int)(a[cat_flag]))
                        temp_year = (int)(a[cat_flag])
        year.append((int)(a[cat_flag]))
        return year

# Objective: Show max data avg of each year
# Calculate 1% maximum data average
# Usage: count_year_max_data_avg(fileObj, TEMPER)
# Return : [94.97, 95.64, 95.23, ...]
def count_year_max_data_avg(fileObj, cat_flag):
	fd = open(fileObj, 'r')
        count = 0
        flag = 0
        avg_data = []
        year_data = []
        for line in fd.readlines():
                a = re.split(',|\n| ', line)
                # Notice the None value
                if (len(a[cat_flag]) != 0):
                        year_data.append((float)(a[cat_flag]))
                        count = count + 1
                if (flag == 0):
                        temp = (int)(a[YEAR])
                        flag = 1
                if(temp != (int)(a[YEAR])):
                        length = (int)(count * RATE)
                        value = heapq.nlargest(length, year_data)
                        avg = mean(value)
                        avg_data.append(avg)
                        year_data = []
                        count = 0
                temp = (int)(a[YEAR])
        length = (int)(count * RATE)
        value = heapq.nlargest(length, year_data)
        avg = mean(value)
        avg_data.append(avg)
        year_data = []
        fd.close()

        return avg_data


# Objective: Be one of label in each cell, show the min data avg of each year
# Calculate 1% minimum data
# Usage: count_year_mix_data_avg(fd, TEMPER)
# Return: [13.3, 12.2, .....]
def count_year_min_data_avg(fileObj, cat_flag):
	fd = open(fileObj, 'r')
        count = 0
        flag = 0
        avg_data = []
        year_data = []
        for line in fd.readlines():
                a = re.split(',|\n| ', line)
                # Notice the None value
                if (len(a[cat_flag]) != 0):
                        year_data.append((float)(a[cat_flag]))
                        count = count + 1
                if (flag == 0):
                        temp = (int)(a[YEAR])
                        flag = 1
                if(temp != (int)(a[YEAR])):
                        length = (int)(count * RATE)
                        value = heapq.nsmallest(length, year_data)
                        avg = mean(value)
                        avg_data.append(avg)
                        year_data = []
                        count = 0
                temp = (int)(a[YEAR])
        length = (int)(count * RATE)
        value = heapq.nlargest(length, year_data)
        avg = mean(value)
        avg_data.append(avg)
        year_data = []
        fd.close()

        return avg_data

# Objective: Show the max data avg each month in one year
# Counting the max data average monthly in one specific year
# Usage: count_mon_max_data_avg(fd, 2010, TEMPER)
# Return: [94.2, 92.2, ....] the max data avg 12 months in one year
def count_mon_max_data_avg(fd, year, cat_flag):
        count = 0
        flag = 0
        avg_data = []
        year_data = []
        for line in fd.readlines():
                a = re.split(',|\n| ', line)
                # Notice the None value
                if ((int)(a[YEAR]) == year):
                        if (flag == 0):
                                temp = (int)(a[MON])
                                flag = 1
                        if (len(a[cat_flag]) != 0):
                                year_data.append((float)(a[cat_flag]))
                                count = count + 1
                        if(temp != (int)(a[MON])):
				length = (int)(count * RATE)
                        	value = heapq.nlargest(length, year_data)
                       	 	avg = mean(value)
                        	avg_data.append(avg)
                        	year_data = []
                        	count = 0
                        temp = (int)(a[MON])
	length = (int)(count * RATE)
        value = heapq.nlargest(length, year_data)
        avg = mean(value)
        avg_data.append(avg)
        year_data = []

	return avg_data

# Objective: Show the min data avg each month in one year
# Counting the min data average monthly in one specific year
# Usage: count_mon_min_data_avg(fd, 2010, TEMPER)
# Return: [12.2, 13.2, ....] the max data avg 12 months in one year
def count_mon_min_data_avg(fd, year, cat_flag):
        count = 0
        flag = 0
        avg_data = []
        year_data = []
        for line in fd.readlines():
                a = re.split(',|\n| ', line)
                # Notice the None value
                if ((int)(a[YEAR]) == year):
                        if (flag == 0):
                                temp = (int)(a[MON])
                                flag = 1
                        if (len(a[cat_flag]) != 0):
                                year_data.append((float)(a[cat_flag]))
                                count = count + 1
                        if(temp != (int)(a[MON])):
				length = (int)(count * RATE)
	                        value = heapq.nsmallest(length, year_data)
        	                avg = mean(value)
                	        avg_data.append(avg)
                        	year_data = []
                       	 	count = 0
                        temp = (int)(a[MON])
	length = (int)(count * RATE)
        value = heapq.nsmallest(length, year_data)
        avg = mean(value)
        avg_data.append(avg)
        year_data = []
        count = 0

	return avg_data

# Objective: Show the number of missing data yearly
# Count miss data each year
# Usage: count_year_missdata(fd, YEAR, TEMPER)
# Return [0, 2, 5,.....] the number of missing data every year
def count_year_missdata(fd, year_flag, mis_flag):
        count = 0
        flag = 0
        miss_count = 0
        missdata = []
        for line in fd.readlines():
                a = re.split(',|\n| ', line)
                if (flag == 0):
                        temp = (int)(a[year_flag])
                        flag = 1
                if (len(a[mis_flag]) == 0):
                        miss_count = miss_count + 1
                if(temp != (int)(a[year_flag])):
                        count = count + 1
                        missdata.append(miss_count)
                        miss_count = 0
                temp = (int)(a[year_flag])
        missdata.append(miss_count)
        return missdata

# Objective: Show the number of data monthly in one year
# count the number of each month in one year
# Usage: count_year_mon_missdata(fd, 2010, TEMTER)
# Return [0, 3, 4, 5, ...] the missing data 12 months in one year
def count_year_mon_missdata(fd, year, mis_flag):
        temp = 0
        miss_count = 0
        flag = 0
        count = 0
        missdata = []
        for line in fd.readlines():
                a = re.split(',|\n| ', line)
                if (flag == 0 and (int)(a[YEAR]) == year):
                        temp = (int)(a[MON])
                        flag = 1
                if (len(a[mis_flag]) == 0 and (int)(a[YEAR]) == year):
                        miss_count = miss_count + 1
                if(temp != (int)(a[MON]) and (int)(a[YEAR]) == year):
                        count = count + 1
                        missdata.append(miss_count)
                        miss_count = 0
                temp = (int)(a[MON])
        missdata.append(miss_count)
        return missdata
