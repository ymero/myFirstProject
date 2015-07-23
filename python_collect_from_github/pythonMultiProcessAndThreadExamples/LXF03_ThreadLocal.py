#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import time, os, random

# 创建全局ThreadLocal对象:
local_school = threading.local()

def process_student():
	time.sleep(random.random()) #小睡片刻, 避免打印到1行当中
	print 'Hello, %s @%s (in %s)' % (local_school.student, local_school.school, threading.current_thread().name)
   

def process_thread(name, school):
    # 绑定ThreadLocal的student:
    local_school.student = name
    local_school.school = school
    process_student()

t1 = threading.Thread(target= process_thread, args=('Alice', 'CUC'), name='Thread-A')
t2 = threading.Thread(target= process_thread, args=('Bob', 'BISU'), name='Thread-B')
t1.start()
t2.start()
t1.join()
t2.join()