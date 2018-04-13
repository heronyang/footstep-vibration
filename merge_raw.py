#!/usr/bin/env python3
import sys
DIR = sys.argv[1]

s = ""
i = 0

while True:

    filename = "data-" = i
    if not os.path.exists(filename):
        print("End, %d is done" % i)
        break
    f = open(filename)
    s += f.read()
    f.close()
    i += 1

f = open(filename, "w")
f.write(s)
f.close()
