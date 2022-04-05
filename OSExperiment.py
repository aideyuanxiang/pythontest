import time
import threading
from threading import Semaphore

Wmutex = Semaphore(1)
Rmutex = Semaphore(1)
Rcount = 0

#读者线程
def reader(i,sleept,start,start_sleep):
    #每个进程开始时间不一样，对应相应的到达时间就要睡眠相应的时间
    time.sleep(start_sleep)
    print('时间点  '+str((int(time.strftime('%S'))-start+60)%60)+'  读者  '+str(i)+'  等待读\n', end='')
    #Rmutex p操作
    Rmutex.acquire()
    global Rcount
    if Rcount == 0:
        # Wmutex p操作
        Wmutex.acquire()
    Rcount += 1
    # Rmutex v操作
    Rmutex.release()
    print('时间点  '+str((int(time.strftime('%S'))-start+60)%60)+'  读者  '+str(i)+'  正在读\n', end='')
    time.sleep(sleept)
    print('时间点  '+str((int(time.strftime('%S'))-start+60)%60)+'  读者  '+str(i)+'  读完\n', end='')
    # Rmutex p操作
    Rmutex.acquire()
    Rcount -= 1
    if Rcount == 0:
        # Wmutex v操作
        Wmutex.release()

    # Rmutex v操作
    Rmutex.release()

#写者线程
def writer(i,sleept,start,start_sleep):
    # 每个进程开始时间不一样，对应相应的到达时间就要睡眠相应的时间
    time.sleep(start_sleep)
    print('时间点  '+str((int(time.strftime('%S'))-start+60)%60)+'  写者  '+str(i)+'  等待写\n', end='')
    # Wmutex p操作
    Wmutex.acquire()
    print('时间点  '+str((int(time.strftime('%S'))-start+60)%60)+'  写者  '+str(i)+'  正在写\n', end='')
    time.sleep(sleept)
    print('时间点  '+str((int(time.strftime('%S'))-start+60)%60)+'  写者  '+str(i)+'  写完\n', end='')
    # Wmutex v操作
    Wmutex.release()


if __name__ == '__main__':
    idx = []
    rwlist = []
    start_time = []
    continue_time = []
    #打开相应输入文件
    with open('D:\\操作系统\\test\\input.txt','r') as f:
        data = f.readlines()
        #逐行读入并以空格为分格符
        for x in data:
            x = x.split()
            idx.append(int(x[0]))
            rwlist.append(x[1])
            start_time.append(int(x[2]))
            continue_time.append(int(x[3]))
    start = int(time.strftime('%S'))
    print('时间点  '+str(start-start)+'  所有线程开始启动\n', end='')
    for i in range(len(rwlist)):
        #输出相应进程启动
        print('时间点  '+str((int(time.strftime('%S'))-start+60)%60)+'  线程  '+str(idx[i])+'  启动\n', end='')
        if rwlist[i] == 'R':
            #创建读者线程
            t = threading.Thread(target=reader, args=(idx[i],continue_time[i],start,start_time[i]))
            t.start()
        else:
            #创建写者线程
            t = threading.Thread(target=writer, args=(idx[i],continue_time[i],start,start_time[i]))
            t.start()

