#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time, threading
import os

import time, threading

# 假定这是你的银行存款:
balance = 0
lock_for_balance = threading.Lock()

def change_it(n):
    # 先存后取，结果应该为0:
    global balance
    balance = balance + n
    balance = balance - n

def run_thread(n):
    for i in range(100000):
        lock_for_balance.acquire()
        try:
            # 放心地改吧:
            change_it(n)
        finally:
            # 改完了一定要释放锁:
            lock_for_balance.release()

t1 = threading.Thread(target=run_thread, args=(5,))
t2 = threading.Thread(target=run_thread, args=(8,))
t1.start()
t2.start()
t1.join()
t2.join()


if balance == 0:
	print "Congratulations! balance = %d, the Lock is working" %  balance 
else:
	print "Bang! balance = %d, fix me to let balance = 0 " %  balance 