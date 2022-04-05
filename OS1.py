
#内存空闲区域，key值为内存区域编号，value的列表分别为分区长度、起始地址
memory={}
keymem=[1]

#进程表，value值为进程长度，进程起始地址
process={}
keyprocess=[]

def meau():
    print("*"*25+"动态分区管理"+"*"*25)
    print("1、内存分配")
    print("2、内存回收")
    print("0、退出")

def showmemory():
    for each in keymem:
        print("内存区号:"+str(each)+"\t"+"分区长度:"+str(memory[each][0])+"\t"+"起始地址:"+str(memory[each][1])+"\t")

def showprocess():
    for each in keyprocess:
        print("进程号:"+str(each)+"\t"+"进程长度:"+str(process[each][0])+"\t"+"起始地址:"+str(process[each][1])+"\t")


def distribution():
    while True:
        print("请选择分配算法:")
        print("1、最先适应法")
        print("2、最佳适应法")
        print("3、最坏适应法")
        print("0、返回上一界面")

        choose=input()
        if choose=='0':
            break
        elif choose=='1':
            distri(1)
        elif choose=='2':
            distri(2)
        elif choose=='3':
            distri(3)
        else:
            print("输入错误请重新输入！")

def distri(type):
    global memory,keymem,process,keyprocess

    print("当前空闲区状况为:")
    showmemory()

    print("请输入待分配进程大小：")
    size=input()
    size=int(size)

    if type==1:
        memory = {k: v for k, v in sorted(memory.items(), key=lambda item: item[1][1])}
        keymem = list(memory.keys())
    elif type==2:
        memory = {k: v for k, v in sorted(memory.items(), key=lambda item: item[1][0])}
        keymem = list(memory.keys())
    else:
        memory = {k: v for k, v in sorted(memory.items(), key=lambda item: item[1][0],reverse=True)}
        keymem = list(memory.keys())

    for each in keymem:
        if memory[each][0] >size:

            newkey = keyprocess[-1] + 1
            keyprocess.append(newkey)
            process[newkey] = [size, memory[each][1]]

            newlength=memory[each][0]-size
            newaddress=memory[each][1]+size
            memory[each]=[newlength,newaddress]


            print("分配完成！当前空闲区状况为:")
            showmemory()

            print("当前进程状况为:")
            showprocess()
            print("\n")

            return
        elif memory[each][0] ==size:
            memory.pop(each)
            keymem.remove(each)

            if process[1][0]==0:
                process[1]=[size,memory[each][1]]
            else:
                newkey=keyprocess[-1]+1
                keyprocess.append(newkey)
                process[newkey]=[size,memory[each][1]]

            newlength=memory[each][0]-size
            newaddress=memory[each][1]+size
            memory[each]=[newlength,newaddress]

            print("分配完成！当前空闲区状况为:")
            showmemory()

            print("当前进程状况为:")
            showprocess()
            print("\n")

            return


    print("没有足够的内存空间进行分配！")


def recycling():
    global memory, keymem, process, keyprocess

    print("当前空闲区状况为:")
    showmemory()

    print("当前进程状况为:")
    showprocess()

    print("请选择要回收的进程号：")
    keypro=input()
    keypro=int(keypro)

    if keypro not in keyprocess:
        print("输入的进程号不存在！")
        return

    flag=0

    for each in keymem:
        #上临空闲区
        if memory[each][1]+memory[each][0]== process[keypro][1]:
            newlength=memory[each][0]+process[keypro][0]
            newaddress=memory[each][1]
            memory[each]=[newlength,newaddress]
            flag=1
            break
            #下临空闲区
        elif process[keypro][1]+process[keypro][0]==memory[each][1]:
            newlength = memory[each][0] + process[keypro][0]
            newaddress =process[keypro][1]
            memory[each] = [newlength, newaddress]
            flag=1
            break
        else:
            pass

    memory = {k: v for k, v in sorted(memory.items(), key=lambda x: x[0])}
    # memory=sorted(memory.keys())
    keymem = list(memory.keys())

    if flag==0:
        newlength = process[keypro][0]
        newaddress = process[keypro][1]
        newkeymem = keymem[-1] + 1
        keymem.append(newkeymem)
        memory[newkeymem] = [newlength, newaddress]

    process.pop(keypro)
    keyprocess.remove(keypro)

    memory = {k: v for k, v in sorted(memory.items(), key=lambda item: item[1][1])}
    keymem = list(memory.keys())

    if len(keymem)>1:
        for i in range(len(keymem) - 1):
            if memory[keymem[i]][0]+memory[keymem[i]][1] == memory[keymem[i+1]][1]:
                newlength = memory[keymem[i]][0]+memory[keymem[i+1]][0]
                newaddress = memory[keymem[i]][1]
                memory[keymem[i]]=[newlength,newaddress]

                memory.pop(keymem[i + 1])
                keymem.remove(keymem[i+1])
                break

    print("回收完成！当前空闲区状况为:")
    showmemory()

    print("当前进程状况为:")
    showprocess()
    print("\n")




if __name__=='__main__':
   print('请输入内存大小：')
   a=int(input())
   memory[1]=[a,0]

   print('请输入当前进程个数：')
   num=input()
   for each in range(int(num)):
       print('当前进程号为：'+str(each+1))
       print('请输入当前进程大小：')
       size=input()
       keyprocess.append(each+1)
       process[each+1]=[int(size),memory[1][1]]
       msize=memory[1][0]-int(size)
       if msize<0:
           print('空间不足，分配失败！')
           break
       madd=memory[1][1]+int(size)
       memory[1]=[msize,madd]

   print("分配完成！当前空闲区状况为:")
   showmemory()

   print("当前进程状况为:")
   showprocess()
   print("\n")


   while True:
       meau()
       choose=input()
       if choose == '0':
           break
       elif choose== '1':
           distribution()
       elif choose=='2':
           recycling()
       else:
           print("输入错误，请重新输入")
