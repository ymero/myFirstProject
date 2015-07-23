#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time, os
import threading, multiprocessing

def loop():
    x = 0
    while True:
        x = x ^ 1

print "I will always running to burning your CPU, kill me with pid: ", os.getpid()
for i in range(multiprocessing.cpu_count()):
    t = threading.Thread(target=loop)
    t.start()