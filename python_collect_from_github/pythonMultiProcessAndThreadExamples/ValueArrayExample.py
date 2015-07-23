#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Source: http://www.bkjia.com/Pythonjc/915477.html
from multiprocessing import Pool
from multiprocessing import Process, Value, Array
import os, time, random

def f(n, a, sleep_second):
    print 'Run task %s (pid:%s)...' % ("f():", os.getpid())
    n.value = n.value + 1
    for i in range(len(a)):
        a[i] = a[i] * 10
        time.sleep(sleep_second)
        print 'a[%d] * 10 = %d  \t(pid:%s)...' % (i, a[i], os.getpid())
    print(n.value)
    print(a[:])

if __name__ == '__main__':
    num = Value('i', 1)
    arr = Array('i', range(6))


    print "pool started"

    p = Process(target=f, args=(num, arr, 0.5))
    p.start()
    p.join()


    p2 = Process(target=f, args=(num, arr, 1))
    p2.start()
    p2.join()

