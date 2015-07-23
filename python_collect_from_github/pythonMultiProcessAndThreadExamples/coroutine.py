#Source: http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/0013868328689835ecd883d910145dfa8227b539725e5ed000
#Source: Python yield 使用浅析 http://www.ibm.com/developerworks/cn/opensource/os-cn-python-yield/

import time
from inspect import isgeneratorfunction 

def consumer():
    r = ''
    while True:
        n = yield r
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        time.sleep(1)
        r = '200 OK'

def produce(c):
    #print ('type c.next() %s ' % type( c.next() ) )
    c.next()
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)
        print('[PRODUCER] Consumer return: %s' % r)
    c.close()

if __name__=='__main__':
    c = consumer()
    print ("is consumer() a generatorfunction %s" % isgeneratorfunction(consumer) )  
    produce(c)