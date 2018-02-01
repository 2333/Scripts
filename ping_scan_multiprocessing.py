# Ping一个IP的代码

import os


def ping1(ip):
    print("start to ping %s" % ip)

    file1 = open('D:\work\ip_dead.txt', 'a+')
    file2 = open('D:\work\ip_active.txt', 'a+')

    try:
        echo = os.system('ping -n 3 -w 1 %s' % ip)
    except Exception as e:
        print("ping {} error".format(ip))

    if echo:
        file1.write(str(ip)+'\n')
        print("%s dead" % ip)

    else:
        file2.write(str(ip)+'\n')
        print("%s alive" % ip)

    file1.close()
    file2.close()

# 多线程ping代码

import os
from multiprocessing.pool import ThreadPool
from multiprocessing import freeze_support       #在Windows环境最好导入
import ipaddress
THREAD_NUM = 20

def ping_scan(network):
    pool = ThreadPool(processes=THREAD_NUM)

    net = ipaddress.ip_network(network)

    ip_list = [ip for ip in net]
    for index in range(0, len(ip_list), THREAD_NUM):

        result_list = []     #每次循环清空
        for ip in ip_list[index:index+THREAD_NUM]:
            result_list.append(pool.apply_async(ping1, [ip]))   #将THREAD_NUM个句柄append进result_list
        for result in result_list:
            result.get(timeout=10)     #执行句柄，设置超时时间为10s


x = ping_scan('10.1.0.0/24')
