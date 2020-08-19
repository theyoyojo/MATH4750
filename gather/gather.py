#!/usr/bin/python3
# Based on code from https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/software

import glob
import time
import datetime
import sys
import signal

BASE_DIR = '/sys/bus/w1/devices/'
SENSOR_DIRS = glob.glob(BASE_DIR + '28*')
NUM_SRCS = len(SENSOR_DIRS)
DATA_SRCS = [SENSOR_DIRS[i] + '/w1_slave' for i in range(NUM_SRCS)]

# Print the date on recipt of SIGINT
def print_date_on_sigint(sig, frame):
    print("End sensor reading at {}".format(str(datetime.datetime.now())))
    sys.exit(0)

# Get the pure, raw, uncensored sensor data
def read_temp_raw(index):
    srcfile = open(DATA_SRCS[i], 'r')
    lines = srcfile.readlines()
    srcfile.close()
    return lines
    
# Extract the actual temperature value from the raw data 
def read_temp(index):
    lines = read_temp_raw(index)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = format(float(temp_string) / 1000.0, '.2f')
        return temp_c


# Register the signal handler and read on loop until forcibly stopped
signal.signal(signal.SIGINT, print_date_on_sigint)
print("Begin sensor reading at {}".format(str(datetime.datetime.now())))
while True:
    for i in range(NUM_SRCS):
        print(read_temp(i),end=' ' if i < NUM_SRCS - 1 else '\n')
    time.sleep(1)
