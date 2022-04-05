import math

visit=[]
sit=0


def mean():
    print('*'*25+'磁盘调度'+'*'*25)
    print('1、先来先服务算法')
    print('2、最短寻道优先算法')
    print('3、电梯算法')
    print('0、退出')

def FCFS():
    print('访问顺序为：')
    print(str(sit)+'  ',end='')
    for each in visit:
        print(str(each)+'  ',end='')

    print('\n',end='')
    sum=0
    t=sit
    for each in visit:
        sum=sum+math.fabs(each-t)
        t=each
    print('移动的总磁道数为：'+str(sum))

def SSTF():
    print('访问顺序为：')
    print(str(sit) + '  ', end='')
    t=sit
    visitnew=visit.copy()
    sum=0
    for i in range(len(visit)):
        pop = 0
        min = 10000
        for each in visitnew:
            if math.fabs(each-t)<min:
                min=math.fabs(each-t)
                pop=each

        t=pop
        sum=sum+min
        visitnew.remove(pop)
        print(str(pop) + '  ', end='')
    print('\n', end='')
    print('移动的总磁道数为：' + str(sum))

def SCAN():
    print('请输入当前移动方向（左：left，右：right）：')
    direction = input()
    if direction == 'left':
        pass
    elif direction == 'right':
        pass
    else:
        print('输入错误！请重新输入！')
        return
    print('访问顺序为：')
    print(str(sit) + '  ', end='')
    t = sit
    min=0
    max=0
    if direction == 'left':
        visitnew = sorted(visit, reverse=True)
        min=visitnew[-1]
        for each in visitnew:
            if each > t:
                continue
            print(str(each) + '  ', end='')
        visitnew=sorted(visit)
        max=visitnew[-1]
        for each in visitnew:
            if each < t:
                continue
            print(str(each) + '  ', end='')

        print('\n', end='')
        print('移动的总磁道数为：' + str(t+max - 2*min))
    else:
        visitnew = sorted(visit)
        max = visitnew[-1]
        for each in visitnew:
            if each < t:
                continue
            print(str(each) + '  ', end='')
        visitnew = sorted(visit, reverse=True)
        min = visitnew[-1]
        for each in visitnew:
            if each > t:
                continue
            print(str(each) + '  ', end='')
        print('\n', end='')
        print('移动的总磁道数为：' + str(2*max - min-t))






if __name__=='__main__':
    flag=0
    print('请输入当前磁头位置：')
    sit=int(input())
    print('请输入当前访问序列个数：')
    num=input()
    for i in range(int(num)):
        print('请输入第'+str(i+1)+'个访问位置')
        visit.append(int(input()))


    while True:
        mean()
        choose=input()
        if choose=='0':
            break
        elif choose=='1':
            FCFS()
        elif choose=='2':
            SSTF()
        elif choose=='3':
            SCAN()
        else:
            print('输入错误请重新输入！')
