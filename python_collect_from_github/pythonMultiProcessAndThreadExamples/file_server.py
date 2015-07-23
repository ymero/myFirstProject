#!/usr/bin/env python
# -*- coding: utf-8 -*-


import socket
import os
import time


def saveFile(s, a):
    print 'Accept new connection from %s:%s to receive file ...' % addr
    s.sendall('getfilename')
    filename = s.recv(1024)
    if '/' in filename:
        dir = os.path.dirname(filename)
        try:
            os.stat(dir)
        except:
            print('Directory does not exist. Creating directory.')
            os.mkdir(dir)
    f = open(filename, 'wb')
    print('Filename: ' + filename)

    while True:
        s.sendall('getfile')
        size = int(s.recv(16))
        print('Total size: ' + str(size))
        recvd = ''
        while size > len(recvd):
            data = s.recv(1024)
            if not data: 
                break
            recvd += data
            f.write(data)
            #print(len(recvd))
        break
    
    print('假装文件很大, 保存时间很长 (暂停10秒钟) ...' )
    time.sleep(10)
    

    s.sendall('end')
    print('File %s received. 保存成功' % filename)

    s.close()
    f.close()


#main function
print('Waiting for client to connect...')
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.bind(('', 1234))
mySocket.listen(5)

while True:
     sock, addr = mySocket.accept()
     saveFile(sock, addr)

mySocket.close(); #不会执行到这里
