#!/usr/bin/python3
import sys
import datetime
import re
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def getlines(filename):
    f = open(filename)
    lines = f.readlines()
    f.close()
    return lines

def stamp_stripper(unstripped_stamp):
    res = re.search(r'(?<=reading at ).*', unstripped_stamp)
    return res.group(0)

# Get total reading duration
def calculate_duration(start_datetime_str, end_datetime_str):
    start_datetime = datetime.datetime.strptime(start_datetime_str, "%Y-%m-%d %H:%M:%S.%f")
    end_datetime = datetime.datetime.strptime(end_datetime_str, "%Y-%m-%d %H:%M:%S.%f")
    return end_datetime - start_datetime

if len(sys.argv) < 2:
    print("usage: analysis.py <datafile>")
    sys.exit(0)


datafile = sys.argv[1]
lines = getlines(datafile)


duration = calculate_duration(stamp_stripper(lines[0]), stamp_stripper(lines[-1]))

# Turn temperature readings into differences of type float
y_data = [nums[1] - nums[0] for nums in [list(map(float, s[0:-1].split(' '))) for s in lines[1:-1]]]

# print(data_list)
# print(duration)

x_range = len(y_data)
x_units = (duration / x_range).total_seconds()
x_data = [i * x_units for i in range(x_range)]

print(x_range, x_units)
print(x_data)

plt.plot(x_data, y_data, 'g--', label='data')

plt.xlabel('Time (units = seconds, interval = {})'.format(x_units))
plt.ylabel('Temperature (units = degrees celcius)')

plt.show()
