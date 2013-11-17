#!/usr/bin/python

#---------------------------------------
# ADAnList.py
# The information showing in record list window for data clean
# 1. Miss data, 2. Extreme data, 3. Delete function
#
#---------------------------------------

# List down all the miss data
# return miss data with (ID, YEAR, MON, DAY, HOUR, MIN)
# Usage: get_all_missdata_list(fd, TEMPER)
def got_all_missdata_list(fd, mis_flag):
        id_count = 0
        missdata = []
        for line in fd.readlines():
                a = re.split(',|\n| ', line)
                if (len(a[mis_flag]) == 0):
                        zipped = zip([id_count], [a[YEAR]], [a[MON]], [a[DAY]], [a[HOUR]], [a[MIN]])
                        missdata.append(zipped)
                        id_count = id_count + 1
        return missdata

