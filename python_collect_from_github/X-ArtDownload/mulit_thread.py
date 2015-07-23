#!/usr/bin/env python
# coding:utf-8
# Author:ficapy
# Version:0.2
# Create On:2014-03-24

import re
import time
import StringIO
import gzip
import urllib2
import codecs
import threading
import Queue


f = codecs.open(r'art.txt', 'w', 'utf-8')
f.close()


def Gettitle(url):
    headers = {
        'Use-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.1.14) Gecko/20080404 (FoxPlus) Firefox/2.0.0.14'}
    req = urllib2.Request(url, headers=headers)
    page = urllib2.urlopen(req).read()
    #<img src="http://x-art.com/videos/pink_on_the_inside/thumb_2.jpg" alt="Pink on the Inside">
    title = re.findall(
        r'<img src="http://x-art.com/videos/.+.jpg" alt="(.+?)">',
        page)
    return title


def Getmagnet(single):
    assert isinstance(single, type(''))
    single = single.lower()
    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Use-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.1.14) Gecko/20080404 (FoxPlus) Firefox/2.0.0.14'}
    # 搜索页面
    searchlink = r'http://kickass.to/usearch/' + \
        urllib2.quote(single + ' ' + 'art')
    searchreq = urllib2.Request(searchlink, headers=headers)
    html_search = urllib2.urlopen(searchlink).read()
    html_search = gzip.GzipFile(
        fileobj=StringIO.StringIO(html_search),
        mode="r").read()
    if re.search(r'<span>  results .+ from \d+</span>', html_search):
        sourcelink = re.search(
            r'<a rel=".+" class=".+" href="(/.+?\.html)#comment">',
            html_search).group(1).decode('UTF-8')
    sourcelink = r'http://kickass.to' + sourcelink
    # 从资源页面提取magnet链接
    sourcereq = urllib2.Request(sourcelink, headers=headers)
    html = urllib2.urlopen(searchlink).read()
    html = gzip.GzipFile(fileobj=StringIO.StringIO(html), mode="r").read()
    if re.search(r'"(magnet.+?)" class', html):
        return re.search(r'"(magnet.+?)" class', html).group(1).decode('UTF-8')


def write(magnet_info):
    f = codecs.open(r'art.txt', 'a+', 'utf-8')
    f.write(magnet_info + u'\r\n')
    f.close()


class Fetch(threading.Thread):

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.setDaemon(True)
        self.start()

    def run(self):
        global count
        while True:
            title = self.queue.get()
            try:
                info = Getmagnet(title)
                if mutex.acquire(20):
                    count += 1
                    print count
                    write(info)
                    mutex.release()
            except Exception as ex:
                print ex
            self.queue.task_done()


def main():
    queue = Queue.Queue()
    start = time.time()
    title = Gettitle('http://x-art.com/videos/')
    for i in title:
        queue.put(i)
    for i in range(5):
        Fetch(queue)
    queue.join()
    cost = time.time() - start
    print unicode(r'总共获取{}个链接，成功下载{}个,耗时{}秒~~~'.format(len(title), count, cost), 'UTF-8')

if __name__ == '__main__':
    count = 0
    mutex = threading.Lock()
    main()
