#!/usr/bin/python3
import sys
import datetime
import re

def getlines(filename):
    f = open(filename)
    lines = f.readlines()
    f.close()
    return lines

def stamp_stripper(unstripped_stamp):
    res = re.search(r'(?<=reading at ).*', unstripped_stamp)
    return res.group(0)

if len(sys.argv) < 2:
    print("usage: analysis.py <datafile>")
    sys.exit(0)

datafile = sys.argv[1]
lines = getlines(datafile)

# Get total reading duration
start_datetime_str, end_datetime_str = stamp_stripper(lines[0]), stamp_stripper(lines[-1])
start_datetime = datetime.datetime.strptime(start_datetime_str, "%Y-%m-%d %H:%M:%S.%f")
end_datetime = datetime.datetime.strptime(end_datetime_str, "%Y-%m-%d %H:%M:%S.%f")
duration = end_datetime - start_datetime


# Turn temperature readings into differences of type float
data_list = [ nums[1] - nums[0] for nums in [list(map(float, s[0:-1].split(' '))) for s in lines[1:-1]]]

print(data_list)
print(duration)
