
# -*- coding: utf-8 -*-
# 多进程扫描网段
import multiprocessing
import subprocess
from netaddr import IPNetwork
# ping 网段ip


def ping_host(activeq, notactiveq, ipaddr):
    # ping -c1 -w1 中-c1是指ping的次数，-w是指执行的最后期限，也就是执行的时间，单位为秒
    # if subprocess.call('ping -c1 -W 1 %s > /dev/null' % ipaddr, shell=True)
    # != 0:
    if subprocess.call('ping -n 1 -w 1 %s >NUL' % ipaddr, shell=True) != 0:
        activeq.put(ipaddr)
    else:
        notactiveq.put(ipaddr)

# 读取队列数据


def read(q, f):
    # if q:
    #     for i in q:
    #         print(q.get(True))
    # else:
    #     print("queue empty")

    while True:
        if not q.empty():
            value = q.get(True)
            print(value)
            f.write(str(value) + "\n")
        else:
            print("Queue end:" + str(q))
            f.write("Queue end\n")
            # f.flush()
            break


# 扫描ip主函数
if __name__ == '__main__':
    # 创建进程间通信队列
    manager = multiprocessing.Manager()
    activeq = manager.Queue()
    notactiveq = manager.Queue()
    process_number = 4
    host_list = IPNetwork('10.16.2.0/24')
    # 创建进程池
    pool = multiprocessing.Pool(processes=process_number)
    for ipaddr in host_list:
        pool.apply_async(ping_host, args=[activeq, notactiveq, ipaddr])
    pool.close()
    pool.join()
    with open("ips.txt", "w") as f:
        # 输出正在使用ip
        read(activeq, f)
        # 输出未被使用ip
        read(notactiveq, f)
