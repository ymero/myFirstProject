#!/bin/bash

source /online/.bash_profile

echo "###################### �����������ؼ����̼�� ##########################"

# 5,15,25,35,45,55 * * * * /online/shell/monitor.sh >> /online/shell/monitor.log

echo "������ڣ�`date`"
echo "���������`ifconfig bond0|grep "inet\>"|sed 's/^[ ]*//g'|awk '{print $2}'|sed 's/addr://g'`"

tom=`ps -ef|grep -v tail|grep -v vi|grep -v grep|grep tomcat|wc -l`

ng=`ps -ef|grep -v tail|grep -v vi|grep -v grep|grep nginx|wc -l`

rs=`ps -ef|grep -v tail|grep -v vi|grep -v grep|grep rsync|wc -l`


if [ $tom = "0" ];
then
    echo "���棡tomcat���̲����ڣ�"
    while :;
    do
        echo "��������tomcat..."
        sh /online/tomcat/bin/startup.sh
        tom=`ps -ef|grep -v tail|grep -v vi|grep -v grep|grep tomcat|wc -l`
        if [ $tom = "0" ];
        then
            echo "����ʧ�ܣ�5����ٴγ�������tomcat..."
            sleep 5
            continue
        else
            echo "tomcat�����ɹ���"
            break
        fi
    done
else
    echo "tomcat��������"
fi


if [ $ng = "0" ];
then
    echo "���棡nginx���̲����ڣ�"
    while :;
    do
        echo "��������nginx..."
        /online/nginx/sbin/nginx
        ng=`ps -ef|grep -v tail|grep -v vi|grep -v grep|grep nginx|wc -l`
        if [ $ng = "0" ];
        then
            echo "����ʧ�ܣ�5����ٴγ�������nginx..."
            sleep 5
            continue
        else
            echo "nginx�����ɹ���"
            break
        fi
    done
else
    echo "nginx��������"
fi

if [ $rs = "0" ];
then
    echo "���棡rsync���̲����ڣ�"
    while :;
    do
        echo "��������rsync..."
        rm -f /online/rsync_server/rsyncd.pid
        /bin/bash /online/rsync_server/start_rsync.sh &
        sleep 1

        rs=`ps -ef|grep -v tail|grep -v vi|grep -v grep|grep rs|wc -l`
        if [ $rs = "0" ];
        then
            echo "����ʧ�ܣ�5����ٴγ�������rsync..."
            sleep 5
            continue
        else
            echo "rsync�����ɹ���"
            break
        fi
    done
else
    echo "rsync��������"
fi
echo "###################### �����������ؼ����̼�� ##########################"

