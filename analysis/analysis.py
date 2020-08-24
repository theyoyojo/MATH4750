#!/usr/bin/python3
import sys



if len(sys.argv) < 2:
    print("usage: analysis.py <datafile>")
    sys.exit(0)

datafile = sys.argv[1]
print("file", datafile)
