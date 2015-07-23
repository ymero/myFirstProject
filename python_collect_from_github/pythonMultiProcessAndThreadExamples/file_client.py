#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sys

if len(sys.argv) <= 1 :
	print "Usage: ", sys.argv[0], "<file_your_wanna_sent>"
else:
    print('Trying to connect...')
    s = socket.socket()
    s.connect(('127.0.0.1', 1234))

    print('Connected. Wating for command.')
    while True:
        cmd = s.recv(32)

        if cmd == 'getfilename':
            print('"getfilename" command received.')
            s.sendall(sys.argv[1])

        if cmd == 'getfile':
            print('"getfile" command received. Going to send file.')
            with open(sys.argv[1], 'rb') as f:
                data = f.read()
            s.sendall('%16d' % len(data))
            s.sendall(data)
            print('File transmission done.')

        if cmd == 'end':
            print('"end" command received. Teminate.')
            break