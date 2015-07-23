#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Process, Queue
import os, time, random

# 写数据进程执行的代码:
def write(q):
    for value in ['A', 'B', 'C']*2:
        print 'writer[%s] Put %s to queue...' % (os.getpid(), value)
        q.put(value)
        #time.sleep(random.random())
        time.sleep(1)

# 读数据进程执行的代码:
def read(q):
    #while True:  
    for x in range(2): #修改为只读两次
        value = q.get(True)
        print '  reader[%s] Get %s from queue.' % (os.getpid(), value)
        time.sleep(1) 

if __name__=='__main__':
    # 父进程创建Queue，并传给各个子进程：
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    # 启动子进程pw，写入:
    pw.start()
    # 启动子进程pr，读取:
    pr.start()
    
    # 主进程等待pw结束后,再结束pr: join表示pw结束: 参 PyMOTW: http://pymotw.com/2/multiprocessing/basics.html
    #pw.join()
    # pr进程里是死循环，无法等待其结束，只能强行终止:
    #pr.terminate()


    #修改为 pr结束(只读了2个字符) , 干掉 pw, 没必要说那么多话唠(原本的计划是6个)
    # 主进程等待pw结束后,再结束pr: join表示pw结束: 参 PyMOTW: http://pymotw.com/2/multiprocessing/basics.html
    pr.join()
    # pr进程里是死循环，无法等待其结束，只能强行终止:
    pw.terminate()