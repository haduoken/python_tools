#!/usr/bin/python3
import time

t = (2020, 4, 17, 17, 3, 38, 1, 48, 0)

# t = time.gmtime(0)
# t.tm_year, t.tm_mon, t.tm_mday = int(year), int(month), int(day)

secs = time.mktime(t)
print("time.mktime(t) : %f" % secs)
print("asctime(localtime(secs)): %s" % time.asctime(time.localtime(secs)))
