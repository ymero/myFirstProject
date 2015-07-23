# -*- encoding:utf-8 -*-

'''
The MIT License (MIT)

Copyright (c) 2014 mr.github

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

'''
    date:   2014-02-27 11:48:04
    desc:   �ٶ�/�е�����ӿ�ʹ��
    urls:   ['http://developer.baidu.com/wiki/index.php?title=�����ĵ���ҳ/�ٶȷ���/����API',
             'http://fanyi.youdao.com/openapi']
    email:  withfaker@gmail.com
    update: 2014-02-27 17:11:43
            �����ȶ�,�ٶȷ�����е������Ĳ�ֻ��һ���...
'''

from urllib import quote, urlopen
import json
import sys

def translate_baidu(word):
    url = "http://openapi.baidu.com/public/2.0/bmt/translate?client_id=8e2hZ4pSYWXavUQ73R013ka4&q=%s&from=en&to=zh" % quote(word)
    s = urlopen(url).read()

    try:
        obj = json.loads(s)
    except ValueError, e:
        print "internal error: [%s]." %e.message
        sys.exit(-3)

    if obj.has_key("error_code"):
        print "internal error:[%s]" % obj["error_msg"]
        sys.exit(-2)
    
    for i in range(len(obj["trans_result"])):
        print obj["trans_result"][i][u"dst"]


def translate_youdao(word):
    url = "http://fanyi.youdao.com/openapi.do?keyfrom=mktime&key=1072012949&type=data&doctype=json&version=1.1&q=%s" % quote(word)
    s = urlopen(url).read()
    
    try:
        obj = json.loads(s)
    except ValueError, e:
        print "internal error: [%s]." %e.message
        sys.exit(-3)

    errCode = obj[u'errorCode']
    if errCode != 0:
        print "error. code:[%d]" % errCode
        sys.exit(-2)

    if obj.has_key(u'translation'):
        print '���룺', obj[u'translation'][0]

    if obj.has_key(u'basic'):
        print '���ͣ�', obj[u'basic'][u'explains'][0]
    print ''

    if obj.has_key(u'web'):
        webs = obj[u'web']
        for i in range(len(webs)):
            w = webs[i]
            #print w
            print '�ؼ��ʣ�', w[u'key']
            values = w[u'value']
            for v in values:
                print "  %s" % v

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "usage: python mydict.py word"
        sys.exit(-1)
    word = sys.argv[1]
    #print "�ٶȷ���"
    #translate_baidu(word)
    print "\n�е�����"
    translate_youdao(word)
