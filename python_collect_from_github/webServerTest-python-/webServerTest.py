# -*- coding: utf-8 -*-
import httplib
import datetime
import threading
from time import ctime
import pdb
import sys
reload(sys)
sys.setdefaultencoding('utf8')
#测试时开启的线程数
threadNum = 100
#测试时请求服务器的总次数
requestNum = 100000

#全局变量，记录当前请求的次数和成功的请求次数
sumRequest = 0
successRequest = 0

#全局变量，记录历史最大、最小、平均请求时间，单位为毫秒
maxTime =0
averageTime=0
minTime=100000000


#锁变量，由于要对两个全局变量进行多线程访问，因此要加锁，这里式互斥锁
sumMutex = threading.Lock()             #总访问次数锁
successMutex = threading.Lock()         #总成功次数锁
maxTimeMutex = threading.Lock()         #最大访问时间锁
averageTimeMutex = threading.Lock()     #平均访问时间锁
minTimeMutex = threading.Lock()         #最小访问时间锁


class serverCheck(threading.Thread):
    def __init__(self,index,maxNums):
        threading.Thread.__init__(self)
        self.index = index
        self.maxNums = maxNums
        self.thread_stop = False

    #线程启动函数
    def run(self):
        #print "线程",self.index,"启动"
        loopFlag=1
        while loopFlag:
            global sumRequest
            sumMutex.acquire()              #获得总访问次数锁，查看是否访问次数已经足够
            if sumRequest<self.maxNums:     #若访问次数不够，则继续访问
                sumRequest = sumRequest+1
                currentSumRequest = sumRequest
                sumMutex.release()          #解锁
                startRequestTime = datetime.datetime.now()
                
                try:
                    conn = httplib.HTTPConnection("113.107.235.117",80) #开始请求http服务器
                    conn.request("GET",'/')
                    response = conn.getresponse()
                except BaseException:               #若出现请求异常，则输出异常信息，关闭连接，进行下一次请求
                    print self.index,"线程请求异常"
                    conn.close()
                    continue
                
                endRequestTime = datetime.datetime.now()
                if response.status == 200:  #查看回复状态码，若成功则记录
                    global successRequest
                    successMutex.acquire()
                    successRequest = successRequest+1
                    successMutex.release()

                    #计算本次访问话费的毫秒数
                    thisRequestMillisecondTime= (endRequestTime-startRequestTime).seconds*1000+((endRequestTime-startRequestTime).microseconds/1000)

                    #更新最大访问时间    
                    global maxTime
                    maxTimeMutex.acquire()
                    maxTime = max(thisRequestMillisecondTime,maxTime)
                    maxTimeMutex.release()
                    #更新最小访问时间
                    global minTime
                    minTimeMutex.acquire()
                    #print "this:",thisRequestMillisecondTime
                    #print "min:",minTime
                    minTime = min(thisRequestMillisecondTime,minTime)
                    #print "nowmin:",minTime
                    minTimeMutex.release()
                    #更新平均访问时间
                    global averageTime
                    averageTimeMutex.acquire()
                    averageTime = averageTime+(thisRequestMillisecondTime-averageTime)/currentSumRequest
                    averageTimeMutex.release();

                conn.close()
            else:                   #若已经达到总访问次数，则解锁并将循环标志置0
                sumMutex.release()      
                loopFlag=0
                
        #print "线程",self.index,"结束";

    def stop(self):
       self.thread_stop = True;

if __name__ == "__main__":
    
    print u"×××××开始测试!×××××" 
    print u"测试线程数：",threadNum
    print u"测试总请求数:",requestNum
    
    threads=[]
    startTime = datetime.datetime.now()
    for i in range(threadNum):
        threads.append(serverCheck(i,requestNum))

    for i in range(len(threads)):
        threads[i].start()
    
    for i in range(len(threads)):          #主线程等待其他线程完成请求
        threads[i].join()
    
    endTime = datetime.datetime.now()    
    print u"×××××测试结束!×××××"
    print u"总次数:",sumRequest
    print u"成功次数：",successRequest
    print u"测试时长：",(endTime-startTime).seconds,"秒"
    print u"最大请求时间:",maxTime,"毫秒"
    print u"最小请求时间:",minTime,"毫秒"
    print u"平均请求时间:",averageTime,"毫秒"

