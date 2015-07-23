//���ڲ�¡��������URLȥ���е�Ӧ��  
  
//���ⱳ��  
/** 
�������������(��������)ȥ����һ����ҳ,����Ϣ����(��������)�ĵ�һ��. 
���Ѿ�����������������һ����ҳ,������������ҳ��URL,�����㻹��һ����Ҫ���ص���ҳ��URL, 
������������,�����ЩURL�Ѿ������ع���,��Ͳ���Ҫ�ٴ�������,����������ٵ�ʶ�� 
����ЩURL�ϵ��ǻ�û�����ص�,������һ�������,���ǲ��ܳ���1%��. 
**/   
  
//������URL��ʼ����Ϊ20���� �������������ģ�����ݣ����Խ��������������Ӧ����  
//����URL����Ϊ186083��  
//��ʹ�ñ�׼C�������б���  
//����hash�������¼ ���µ����  
//ԭ���������ʾ  
  
#include <string>  
#include <iostream>  
#include <assert.h>  
#include <fstream>  
#include <time.h>  
using  namespace std;  
  
  
#define FUNC_NUM 8  
#define BIT_MAX 3999949 //����һ��������why?  
const int  HASH_SIZE = BIT_MAX / 8  + 1;  
  
char    hash[HASH_SIZE];  
int     strInt[FUNC_NUM];  
  
//���±�<<[1-8]>>���ֵ����ַ���ɢ�к���������������ʹ���ˣ���ɢ�к���  
  
//<<1>>  
unsigned int RSHash(const std::string& str)  
{  
   unsigned int b    = 378551;  
   unsigned int a    = 63689;  
   unsigned int hash = 0;  
  
   for(std::size_t i = 0; i < str.length(); i++)  
   {  
      hash = hash * a + str[i];  
      a    = a * b;  
   }  
  
   return hash;  
}  
  
//<<2>>  
unsigned int JSHash(const std::string& str)  
{  
   unsigned int hash = 1315423911;  
  
   for(std::size_t i = 0; i < str.length(); i++)  
   {  
      hash ^= ((hash << 5) + str[i] + (hash >> 2));  
   }  
  
   return hash;  
}  
  
//<<3>>  
unsigned int PJWHash(const std::string& str)  
{  
   unsigned int BitsInUnsignedInt = (unsigned int)(sizeof(unsigned int) * 8);  
   unsigned int ThreeQuarters     = (unsigned int)((BitsInUnsignedInt  * 3) / 4);  
   unsigned int OneEighth         = (unsigned int)(BitsInUnsignedInt / 8);  
   unsigned int HighBits          = (unsigned int)(0xFFFFFFFF) << (BitsInUnsignedInt - OneEighth);  
   unsigned int hash              = 0;  
   unsigned int test              = 0;  
  
   for(std::size_t i = 0; i < str.length(); i++)  
   {  
      hash = (hash << OneEighth) + str[i];  
  
      if((test = hash & HighBits)  != 0)  
      {  
         hash = (( hash ^ (test >> ThreeQuarters)) & (~HighBits));  
      }  
   }  
  
   return hash;  
}  
  
//<<4>>  
unsigned int APHash(const std::string& str)  
{  
   unsigned int hash = 0xAAAAAAAA;  
  
   for(std::size_t i = 0; i < str.length(); i++)  
   {  
      hash ^= ((i & 1) == 0) ? (  (hash <<  7) ^ str[i] * (hash >> 3)) :  
                               (~((hash << 11) + (str[i] ^ (hash >> 5))));  
   }  
  
   return hash;  
}  
  
//<<5>>  
unsigned int BKDRHash(const std::string& str)  
{  
   unsigned int seed = 131; // 31 131 1313 13131 131313 etc..  
   unsigned int hash = 0;  
  
   for(std::size_t i = 0; i < str.length(); i++)  
   {  
      hash = (hash * seed) + str[i];  
   }  
  
   return hash;  
}  
  
//<<6>>  
unsigned int SDBMHash(const std::string& str)  
{  
   unsigned int hash = 0;  
  
   for(std::size_t i = 0; i < str.length(); i++)  
   {  
      hash = str[i] + (hash << 6) + (hash << 16) - hash;  
   }  
  
   return hash;  
}  
  
//<<7>>  
unsigned int FNVHash(const std::string& str)  
{  
   const unsigned int fnv_prime = 0x811C9DC5;  
   unsigned int hash = 0;  
   for(std::size_t i = 0; i < str.length(); i++)  
   {  
      hash *= fnv_prime;  
      hash ^= str[i];  
   }  
  
   return hash;  
}  
  
//<<8>>  
 unsigned int Hflp(string str){  
        unsigned int len = str.length();  
        unsigned int sum = 0;  
        for(std::size_t i=0;i<len;i++){  
               sum ^= str[i] << (8*(i%4));  
        }  
         return sum & 0x7FFFFFFF;  
 }  
  
//����hash�������¼ http://jinyun2012.blog.sohu.com  
  
  
//��һ�������urlɢ�г�һ������  
void getIntSet(string url , int * set)  
{  
        set[0] = RSHash(url)   % BIT_MAX;  
        set[1] = JSHash(url)   % BIT_MAX;  
        set[2] = PJWHash(url)  % BIT_MAX;  
        set[3] = APHash(url)   % BIT_MAX;  
        set[4] = BKDRHash(url) % BIT_MAX;  
        set[5] = SDBMHash(url) % BIT_MAX;  
        set[6] = FNVHash(url)  % BIT_MAX;  
        set[7] = Hflp(url)     % BIT_MAX;  
}  
  
//��ÿ��urlӳ�䵽hash������  
void shadeHash(string url){  
        getIntSet(url , strInt);  
        for(int i=0;i<FUNC_NUM;i++){  
                int pos = (strInt[i] >> 3);  
                int mod = strInt[i] & 7;  
                int val = 1 << (7 - mod);  
                hash[pos] |= val;  
        }  
}  
  
//����url�Ƿ������url.dat�ļ���  
bool find(string url)  
{  
        getIntSet(url , strInt);  
        bool res = true;  
        for(int i=0;i<FUNC_NUM && res == true; i++){  
                int pos = (strInt[i] >> 3);  
                int mod = strInt[i] & 7;  
                int val = 1 << (7 - mod);  
                res &= (bool)(hash[pos] & val);  
        }  
        return res;  
}  
  
int main(int argc, char* argv[])  
{  
        ifstream url_in("url.dat");  
        assert(url_in != NULL);  
        string url;  
        int len(0);  
        time_t con_start = time(NULL);  
        while(getline(url_in , url)){  
                len += url.length();  
                shadeHash(url);  
        }  
        time_t con_end = time(NULL);  
        url_in.close();  
  
        //��ȡ�ļ��в�������  
        ifstream test_in("test_url.dat");  
        assert(test_in);  
        int count(0) , size(0);  
        time_t test_start = time(NULL);  
        while(getline(test_in , url)){  
                size++;  
                if(find(url))count++;  
        }  
        time_t test_end = time(NULL);  
  
        cout<<"����URL������"<<size<<endl;  
        cout<<"����URL������"<<count<<endl;  
        cout<<"�������   : "<<count * 1.0 / size<<endl << endl;  
  
        cout<<"��������--->"<<endl;  
        cout<<"ԭURL��ռ�洢�ռ�:        "<<len <<" byte"<<endl;  
        cout<<"������Ҫ�洢�ռ� :         "<< HASH_SIZE<<" byte"<<endl;  
        cout<<"�ռ��Լ       ��       "<< 1.0 - HASH_SIZE * 1.0 / len <<endl;  
        cout<<"����hash������ʱ��        "<<(con_end - con_start)<<"s"<<endl;  
        cout<<"��������ʱ��                 "<<(test_end - test_start)<<"s"<<endl;  
            return 0;  
}  
