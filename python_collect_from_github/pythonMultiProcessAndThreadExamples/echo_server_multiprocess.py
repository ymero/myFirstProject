#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Source: https://gist.github.com/micktwomey/606178

'a server example which send hello to client.'

import multiprocessing
import time, socket, os

def tcplink(sock, addr):
    print 'Run task %s (%s)...' % (name, os.getpid())
    print 'Accept new connection from %s:%s...' % addr
    sock.send('Welcome!')
    while True:
        data = sock.recv(1024)
        print ("debug:  %s recv data %s" % (addr, data) )
        time.sleep(2)
        if data == 'exit' or not data:
            break
        sock.send('Hello, %s!' % data)
    sock.close()
    print 'Connection from %s:%s closed.' % addr

if __name__=='__main__':

    print 'Parent process %s.' % os.getpid()
    #p = Pool()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 监听端口:
    s.bind(('127.0.0.1', 9999))
    s.listen(5)
    print 'Waiting for connection...'

       
    #workers = [ multiprocessing.Process(target=tcplink, args=(sock, addr))  for i in range(5) ]

    # for p in workers:
    #     p.daemon = True
    #     p.start()
    

    while True:
        # 接受一个新连接:
        sock, addr = s.accept()
        # 创建新线程来处理TCP连接:
        #t = threading.Thread(target=tcplink, args=(sock, addr))
        #t.start()
        process = multiprocessing.Process(target=tcplink, args=(sock, addr))

        process.daemon = True
        process.start()
        time.sleep(10)

    #for process in multiprocessing.active_children():
       #logging.info("Shutting down process %r", process)
    #    process.terminate()
    #    process.join()

    print 'subprocesses %s done.' % os.getpid()