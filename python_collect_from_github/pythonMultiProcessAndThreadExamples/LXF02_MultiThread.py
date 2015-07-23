#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time, threading
import os

# 新线程执行的代码:
def loop():
    print '[pid:%d] thread %s is running...' % (os.getpid(), threading.current_thread().name)
    n = 0
    while n < 5:
        n = n + 1
        print '[pid:%d] thread %s >>> %s' % (os.getpid(),threading.current_thread().name, n)
        time.sleep(1)
    print '[pid:%d] thread %s ended.' % (os.getpid(), threading.current_thread().name)

print '[pid:%d] thread %s is running...' % (os.getpid(), threading.current_thread().name)
t = threading.Thread(target=loop, name='LoopThread')
t.start()
t.join()
print '[pid:%d] thread %s ended.' % (os.getpid(), threading.current_thread().name) 