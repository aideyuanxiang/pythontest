from audioop import error

import pandas as pd

from Compile1 import Complier

vt = ['=','+','-','*','(',')','i','#']
vn = ['S','E']
productions=['S\'->S','S->i=E','E->E+E','E->-E','E->E*E','E->(E)','E->i']

actionData = [['' for i in range(len(vt))] for j in range(15)]
Action = pd.DataFrame(data = actionData,index=range(15),columns=vt)
gotoData = [[-1 for i in range(len(vn))] for j in range(15)]
Goto = pd.DataFrame(data = gotoData,index=range(15),columns=vn)

Action.loc[0]['i']='s2'
Action.loc[1]['#']='acc'
Action.loc[2]['=']='s3'
Action.loc[3]['-']='s9'
Action.loc[3]['(']='s11'
Action.loc[3]['i']='s14'
Action.loc[4]['+']='s5'
Action.loc[4]['*']='s7'
Action.loc[4]['#']='r1'
Action.loc[5]['-']='s9'
Action.loc[5]['(']='s11'
Action.loc[5]['i']='s14'
Action.loc[6]['+']='s5'
Action.loc[6]['*']='s7'
Action.loc[6]['#']='r2'
Action.loc[6][')']='r2'
Action.loc[7]['-']='s9'
Action.loc[7]['(']='s11'
Action.loc[7]['i']='s14'
Action.loc[8]['+']='r4'
Action.loc[8]['*']='s7'
Action.loc[8][')']='r4'
Action.loc[8]['#']='r4'
Action.loc[9]['-']='s9'
Action.loc[9]['(']='s11'
Action.loc[9]['i']='s14'
Action.loc[10]['+']='r3'
Action.loc[10]['*']='r3'
Action.loc[10][')']='r3'
Action.loc[11]['-']='s9'
Action.loc[11]['(']='s11'
Action.loc[11]['i']='s14'
Action.loc[12]['+']='s5'
Action.loc[12]['*']='s7'
Action.loc[12][')']='s13'
Action.loc[13]['=']='r5'
Action.loc[13]['+']='r5'
Action.loc[13]['-']='r5'
Action.loc[13]['*']='r5'
Action.loc[13]['(']='r5'
Action.loc[13][')']='r5'
Action.loc[13]['i']='r5'
Action.loc[14]['#']='r6'
Action.loc[14]['=']='r6'
Action.loc[14]['+']='r6'
Action.loc[14]['-']='r6'
Action.loc[14]['*']='r6'
Action.loc[14]['(']='r6'
Action.loc[14][')']='r6'
Action.loc[14]['i']='r6'
Action.loc[14]['#']='r6'

Goto.loc[0]['S']=1
Goto.loc[3]['E']=4
Goto.loc[5]['E']=6
Goto.loc[7]['E']=8
Goto.loc[9]['E']=10
Goto.loc[11]['E']=12

temp=[]

def newtemp():
    global  temp
    if len(temp)==0:
        temp.append('t0')
    else:
        temp.append('t'+str(len(temp)))

    return temp[-1]

class Stack(object):
    def __init__(self):
        self.__list = []

    def push(self, item):
        self.__list.append(item)

    def pop(self):
        return self.__list.pop()

    def top(self):
        if self.__list:
            return self.__list[-1]
        return None

    def is_empty(self):
        return self.__list == []

    def size(self):
        return len(self.__list)

    def show(self):
        return ' '.join(self.__list)


def getRes(lang,value):
    f = open('D:\\编译原理\\test\\result2.txt', 'w')
    middle=[]
    V = lang+'#'
    f.write('V is '+V+'\n')
    status=Stack()
    symbol = Stack()
    temps=Stack()
    status.push('0')
    i = 0
    a = V[0]
    for each in value:
        temps.push(each)
    while True:
        s = int(status.top())
        curAct = Action[a][s]
        if curAct==''or curAct==-1:
            f.write('此处源程序语法有误！'+'\n')
            f.write('符号栈中为' + symbol.show()+'\n')
            f.write('输入为 ' + ' '.join(V[i:])+'\n')
            break
        if curAct[0] == 's':
            symbol.push(a)
            status.push(str(curAct[1:]))
            i = i + 1
            a = V[i]
            f.write('移进\n')
        elif curAct[0] == 'r':
            go=productions[int(curAct[1])].split('-')[0]
            curProd = productions[int(curAct[1])].split('>')[-1]
            sy=[]
            for j in range(len(curProd)):
                status.pop()
                sy.append(symbol.pop())

            tempmiddle=[]
            if len(sy)!=1:
                if sy[1]=='+':
                    middle.append('('+sy[1]+','+temps.pop()+','+temps.pop()+','+newtemp()+')')
                    temps.push(temp[-1])
                elif sy[1]=='*':
                    middle.append('(' + sy[1] + ',' + temps.pop() + ',' + temps.pop() + ',' + newtemp() + ')')
                    temps.push(temp[-1])
                elif sy[1]=='=':
                    middle.append('(' + sy[1] + ',' + temps.pop() + ',' + '_' + ',' + 'x' + ')')
                elif sy[1]=='-':
                    middle.append('(' + sy[1] + ',' + temps.pop() + ',' + '_' + ',' + newtemp() + ')')
                    temps.push(temp[-1])
            t = status.top()
            A = go
            symbol.push(A)
            status.push(str(Goto[A][int(t)]))
            f.write('输出 '+' '.join(productions[int(curAct[1])])+ ' 规约'+'\n')
        elif curAct[0:3] == 'acc':
            f.write('分析完成'+'\n')
            break
        else:
            raise error()
        f.write('状态栈中为 '+status.show()+'\n')
        f.write('符号栈中为'+symbol.show()+'\n')
        f.write('输入为 '+ ' '.join(V[i:])+'\n')
        f.write('\n')
    for each in middle:
        f.write(each+'\n')

#
# print(Action)
# print(Goto)

ComPlier = Complier()
SourceProgram = []
Filepath = 'D:\\编译原理\\test\\test2.txt'
for line in open(Filepath, 'r', encoding='UTF-8-sig'):
    line = line.replace('\n', '')
    SourceProgram.append(line)
SourceProgram = ComPlier.RemoveSpace(SourceProgram)
sentence,value=ComPlier.Reader(SourceProgram)
value=value[1:]
getRes(SourceProgram[0],value)