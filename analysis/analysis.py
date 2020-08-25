#!/usr/bin/python3
import sys
import datetime
import re
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy

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

# paramaters: t(ime), I(nitial), C(ooling coefficient), O(ffset)
def exponential_decay(t, I, C, O):
    return I * numpy.exp(-C * t) + O

# If we don't have datafile, we can't do anything
if len(sys.argv) < 2:
    print("usage: analysis.py <datafile>")
    sys.exit(0)


# Get the raw data from the datafile
datafile = sys.argv[1]
lines = getlines(datafile)

# Calculate the duration of the sensor reading
duration = calculate_duration(stamp_stripper(lines[0]), stamp_stripper(lines[-1]))

# Turn temperature readings into differences of type float
y_data = [nums[1] - nums[0] for nums in [list(map(numpy.float64, s[0:-1].split(' '))) for s in lines[1:-1]]]

# Calculate the time interval by dividing the total duration by the number of data points
x_range = len(y_data)
x_units = (duration / x_range).total_seconds()
x_data = numpy.array([numpy.float64(i * x_units) for i in range(x_range)])

# Perform non-linear least squares curve fitting using the scipy library
popt, pcov = curve_fit(exponential_decay, x_data, y_data)

# Plot the raw data in blue dashed lines
plt.plot(x_data, y_data, 'b--', label='data')

# Plot the curve we fitted to the data
plt.plot(x_data, exponential_decay(x_data, *popt), 'r-',
        label='fit:I=%.3E, C=%.3E, O=%.3E' % tuple(popt))

plt.xlabel('Time (units = seconds, interval = %.3f)')
plt.ylabel('Temperature (units = degrees celcius)')
plt.legend()

# The result :)
plt.show()
