
#!/usr/local/bin/python2.7
#coding=gbk
'''
Created on 2012-11-7

@author: palydawn
'''
import cmath
from BitVector import BitVector

class BloomFilter(object):
    #֮ǰ��pythonд��һ���������棬����urlȥ���õľ��ǲ�¡�������������Ǹ�����c++д�ģ���windows����boost�����pythonģ��֮����python������ã������ô�python����дһ��������������linux��windows�¶����������ˣ������Ǵ��룺
    def __init__(self, error_rate, elementNum):
        #��������Ҫ��bit��
        self.bit_num = -1 * elementNum * cmath.log(error_rate) / (cmath.log(2.0) * cmath.log(2.0))
        
        #���ֽڶ���
        self.bit_num = self.align_4byte(self.bit_num.real)
        
        #�����ڴ�
        self.bit_array = BitVector(size=self.bit_num)
        
        #����hash��������
        self.hash_num = cmath.log(2) * self.bit_num / elementNum
        
        self.hash_num = self.hash_num.real
        
        #����ȡ��
        self.hash_num = int(self.hash_num) + 1
        
        #����hash��������
        self.hash_seeds = self.generate_hashseeds(self.hash_num)
        
    def insert_element(self, element):
        for seed in self.hash_seeds:
            hash_val = self.hash_element(element, seed)
            #ȡ����ֵ
            hash_val = abs(hash_val)
            #ȡģ����Խ��
            hash_val = hash_val % self.bit_num
            #������Ӧ�ı���λ
            self.bit_array[hash_val] = 1
    
    #���Ԫ���Ƿ���ڣ����ڷ���true�����򷵻�false 
    def is_element_exist(self, element):
        for seed in self.hash_seeds:
            hash_val = self.hash_element(element, seed)
            #ȡ����ֵ
            hash_val = abs(hash_val)
            #ȡģ����Խ��
            hash_val = hash_val % self.bit_num
            
            #�鿴ֵ
            if self.bit_array[hash_val] == 0:
                return False
        return True
        
    #�ڴ����    
    def align_4byte(self, bit_num):
        num = int(bit_num / 32)
        num = 32 * (num + 1)
        return num
    
    #����hash��������,hash_num������
    def generate_hashseeds(self, hash_num):
        count = 0
        #�����������ӵ���С��ֵ
        gap = 50
        #��ʼ��hash����Ϊ0
        hash_seeds = []
        for index in xrange(hash_num):
            hash_seeds.append(0)
        for index in xrange(10, 10000):
            max_num = int(cmath.sqrt(1.0 * index).real)
            flag = 1
            for num in xrange(2, max_num):
                if index % num == 0:
                    flag = 0
                    break
            
            if flag == 1:
                #��������hash���ӵĲ�ֵҪ�����
                if count > 0 and (index - hash_seeds[count - 1]) < gap:
                    continue
                hash_seeds[count] = index
                count = count + 1
            
            if count == hash_num:
                break
        return hash_seeds
    
    def hash_element(self, element, seed):
        hash_val = 1
        for ch in str(element):
            chval = ord(ch)
            hash_val = hash_val * seed + chval
        return hash_val
'''
#���Դ���
bf = BloomFilter(0.001, 1000000)
element = 'palydawn'
bf.insert_element(element)
print bf.is_element_exist('palydawn')'''

    ����ʹ����BitVector�⣬python����Ķ����Ʋ������������鷳������ͼ򵥶���
