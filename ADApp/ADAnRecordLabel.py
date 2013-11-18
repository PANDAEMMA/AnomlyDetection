#!/usr/bin/python

#-----------------------------------------------
# ADAnRecordLabel.py
# The analysis results showing in each Record cells
# Data: 1. Miss data count. 2. Max data avg. 3. Residual
# Plot: 1. x-axis ratio of each item in one month
#
#------------------------------------------------

# Objective: Be one of label in each cell, show the max data avg of each year
# Calculate 1% maximum data average
# Usage: count_year_max_data_avg(fd, TEMPER)
# Return : [94.97, 95.64, 95.23, ...]
def count_year_max_data_avg(fd, cat_flag):
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
                        length = (int)(count * 0.01)
                        b_sum = 0
                        for i in range(length):
                                b = max(year_data)
                                b_sum = b_sum + (float)(b)
                                year_data.remove(b)
                        avg = b_sum/length
                        avg_data.append(avg)
                        year_data = []
                        count = 0
                temp = (int)(a[YEAR])
        return avg_data

# Objective: Be one of label in each cell, show the min data avg of each year
# Calculate 1% minimum data
# Usage: count_year_mix_data_avg(fd, TEMPER)
# Return: [13.3, 12.2, .....]
def count_year_mix_data_avg(fd, cat_flag):
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
                        length = (int)(count * 0.01)
                        b_sum = 0
                        for i in range(length):
                                b = min(year_data)
                                b_sum = b_sum + (float)(b)
                                year_data.remove(b)
                        avg = b_sum/length
                        avg_data.append(avg)
                        year_data = []
                        count = 0
                temp = (int)(a[YEAR])
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
                                length = (int)(count * 0.01)
                                b_sum = 0
                                for i in range(length):
                                        b = max(year_data)
                                        b_sum = b_sum + (float)(b)
                                        year_data.remove(b)
                                avg = b_sum/length
                                avg_data.append(avg)
                                year_data = []
                                count = 0
                        temp = (int)(a[MON])
        length = (int)(count * 0.01)
        b_sum = 0
        for i in range(length):
                b = max(year_data)
                b_sum = b_sum + (float)(b)
                year_data.remove(b)
        avg = b_sum/length
        avg_data.append(avg)
        year_data = []
        count = 0
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
                                length = (int)(count * 0.01)
                                b_sum = 0
                                for i in range(length):
                                        b = min(year_data)
                                        b_sum = b_sum + (float)(b)
                                        year_data.remove(b)
                                avg = b_sum/length
                                avg_data.append(avg)
                                year_data = []
                                count = 0
                        temp = (int)(a[MON])
        length = (int)(count * 0.01)
        b_sum = 0
        for i in range(length):
                b = min(year_data)
                b_sum = b_sum + (float)(b)
                year_data.remove(b)
        avg = b_sum/length
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
