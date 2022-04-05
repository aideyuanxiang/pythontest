from audioop import error

import pandas as pd

Operation = ['*', '-', '/', '=', '>', '<', '>=', '==', '<=', '%', '+', '+=', '-=', '*=', '/=']  # 词法分析器中分别运算符
Delimiter = ['(', ')', ',', ';', '.', '{', '}', '<', '>', '"']  # 词法分析器中分别界符
KeyWord = ['bool', 'char', 'class', 'double', 'false', 'float', 'getchar', 'include', 'int', 'long', 'main',
           'null', 'open', 'printf','private', 'public', 'put', 'read', 'return', 'short', 'scanf', 'signed', 'static',
           'stdio', 'string','struct', 'true','unsigned', 'void','while','and']

vt = ['while','(',')','{','}','and','i','>','=','+','d',';','#']
vn = ['S','A','B','E','F','H','G']
productions=['S\'->S','S->whileAB','A->(E)','B->{F}','E->EandE','E->i>d','F->i=G;','G->G+d','G->d']

fuhao=[]
fuhaoL=[]

actionData = [['' for i in range(len(vt))] for j in range(23)]
Action = pd.DataFrame(data = actionData,index=range(23),columns=vt)
gotoData = [[-1 for i in range(len(vn))] for j in range(23)]
Goto = pd.DataFrame(data = gotoData,index=range(23),columns=vn)

Action.loc[0]['while']='s2'
Action.loc[1]['#']='acc'
Action.loc[2]['(']='s4'
Action.loc[3]['{']='s13'
Action.loc[4]['i']='s9'
Action.loc[5][')']='s6'
Action.loc[5]['and']='s7'
Action.loc[6]['{']='r2'
Action.loc[7]['i']='s9'
Action.loc[8][')']='r4'
Action.loc[8]['and']='s7'
Action.loc[9]['>']='s10'
Action.loc[10]['d']='s11'
Action.loc[11][')']='r5'
Action.loc[11]['and']='r5'
Action.loc[12]['#']='r1'
Action.loc[13]['i']='s16'
Action.loc[14]['}']='s15'
Action.loc[15]['#']='r3'
Action.loc[16]['=']='s17'
Action.loc[17]['d']='s19'
Action.loc[18][';']='s20'
Action.loc[18]['+']='s21'
Action.loc[19]['+']='r8'
Action.loc[20]['}']='r6'
Action.loc[21]['d']='s22'
Action.loc[22][';']='r7'


Goto.loc[0]['S']=1
Goto.loc[2]['A']=3
Goto.loc[3]['B']=12
Goto.loc[4]['E']=5
Goto.loc[7]['E']=8
Goto.loc[13]['F']=14
Goto.loc[17]['G']=18

class Complier():  # 封装成编译器
    def IsLetter(self, Char):
        if ((Char >= 'a' and Char <= 'z') or (Char >= 'A' and Char <= 'Z')):
            return True
        else:
            return False

    def IsDigit(self, Char):
        if (Char <= '9' and Char >= '0'):
            return True
        else:
            return False

    def IsSpace(self, Char):
        if (Char == ' '):
            return True
        else:
            return False

    def RemoveSpace(self, List):  # 清除字符串中前后的空格
        indexInList = 0
        for String in List:
            List[indexInList] = String.strip()
            indexInList += 1
        return List


    def Reader(self, List):
        ResultList = []
        # f = open('D:\\编译原理\\test\\result.txt', 'w')
        count=0
        for String in List:
            count=count+1
            Letter = ''
            Digit = ''
            letter = ''
            index = 0
            for Char in String:
                if (index < len(String) - 1):
                    index += 1
                if (self.IsLetter(Char)):
                    if (self.IsLetter(String[index]) or self.IsDigit(String[index])):
                        Letter += Char
                    elif (self.IsSpace(String[index]) or (String[index] in Delimiter) or (
                            String[index] in Operation) or (String[index:index + 2] in Operation)):
                        Letter += Char
                        if Letter in KeyWord:
                            ResultList.append(Letter)
                            # f.write('<' + Letter + ',关键字>'+'\n')
                            print('<' + Letter + ',关键字>' + '\n')
                        else:
                            ResultList.append('i')
                            fuhaoL.append(Letter)
                            # f.write('<' + Letter + ',标识符>'+'\n')
                            print('<' + Letter + ',标识符>' + '\n')
                        Letter = ''
                else:
                    if (self.IsDigit(Char)):
                        if (self.IsLetter(String[index]) or self.IsDigit(String[index])):
                            Digit += Char
                        elif (self.IsSpace(String[index]) or (String[index] in Delimiter) or (
                                String[index] in Operation) or (String[index:index + 2] in Operation)):
                            Digit += Char
                            ResultList.append('d')
                            fuhao.append(Digit)
                            # f.write('<' + Digit + ',常数>'+'\n')
                            print('<' + Digit + ',常数>' + '\n')
                            Digit = ''
                    else:
                        if (Char == '#'):
                            ResultList.append('#')
                            # f.write('<#,宏定义符号>'+'\n')
                            print('<#,宏定义符号>' + '\n')
                        else:
                            if (Char in Delimiter):
                                ResultList.append(Char)
                                # f.write('<' + Char + ',界符>'+'\n')
                                print('<' + Char + ',界符>' + '\n')
                            else:
                                if (Char in Operation):
                                    letter += Char
                                    if (String[index] in Operation):
                                        letter += String[index]
                                        ResultList.append(letter)
                                        # f.write('<' + letter + ',运算符>'+'\n')
                                        print('<' + letter + ',运算符>' + '\n')
                                        letter = ''
                                    else:
                                        ResultList.append(letter)
                                        # f.write('<' + letter + ',运算符>'+'\n')
                                        print('<' + letter + ',运算符>' + '\n')
                                        letter = ''
                                else:
                                    if (self.IsSpace(Char)):
                                        pass



        return ResultList

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


def getRes(lang):
    # f = open('D:\\编译原理\\test\\result2.txt', 'w')
    lang.append('#')
    V=lang
    t=0
    # f.write('V is '+V+'\n')
    # print('V is ' + V + '\n')
    status=Stack()
    symbol = Stack()
    temps=Stack()
    status.push('0')
    middle=[]
    index=0
    indexl=0
    i = 0
    a = V[0]
    while True:
        s = int(status.top())
        curAct = Action[a][s]
        if curAct==''or curAct==-1:
            print('此处源程序语法有误！')
            print('符号栈中为' + symbol.show())
            print('输入为 ' + ' '.join(V[i:]))
            t=1
            break
        if curAct[0] == 's':
            symbol.push(a)
            status.push(str(curAct[1:]))
            i = i + 1
            a = V[i]
            # f.write('移进\n')
            print('移进\n')
        elif curAct[0] == 'r':
            go=productions[int(curAct[1])].split('->')[0]
            curProd = productions[int(curAct[1])].split('->')[-1]
            sy=[]
            if curProd[:5]=='while':
                for j in range(3):
                    status.pop()
                    sy.append(symbol.pop())
            elif curProd[1:4]=='and':
                for j in range(3):
                    status.pop()
                    sy.append(symbol.pop())
            else:
                for j in range(len(curProd)):
                    status.pop()
                    sy.append(symbol.pop())

            # tempmiddle=[]
            # flag=0



            if len(sy)!=1 and sy[1]=='>':
                if sy[0]=='d' and sy[2]!='i':
                    middle.append('(j>,' + sy[2] + ',' + fuhao[index] + ',' + '10' + str(len(middle) + 3) + ')')
                    middle.append('(j,_,_')
                    index=index+1
                elif sy[0]!='d' and sy[2]=='i':
                    middle.append('(j>,' + fuhaoL[indexl] + ',' + sy[0] + ',' + '10' + str(len(middle) + 3) + ')')
                    middle.append('(j,_,_')
                    indexl = indexl + 1
                elif sy[0]=='d' and sy[2]=='i':
                    middle.append('(j>,' + fuhaoL[indexl] + ',' + fuhao[index] + ',' + '10' + str(len(middle) + 3) + ')')
                    middle.append('(j,_,_')
                    index=index+1
                    indexl = indexl + 1
                else:
                    middle.append('(j>,'+sy[2]+','+sy[0]+','+'10'+str(len(middle)+3)+')')
                    middle.append('(j,_,_')
            elif len(sy)!=1 and sy[2]=='=':
                if sy[1]=='d'and sy[3]!='i':
                    middle.append('(' + sy[2] + ',' + fuhao[index] + ',' + '_' + ',' + sy[3] + ')')
                    index=index+1
                elif sy[1]!='d'and sy[3]=='i':
                    if sy[1] in vn:
                        sy[1]=temps.pop()
                    middle.append('(' + sy[2] + ',' + sy[1] + ',' + '_' + ',' + fuhaoL[indexl] + ')')
                    indexl = indexl + 1
                elif sy[1]=='d'and sy[3]=='i':
                    middle.append('(' + sy[2] + ',' +fuhao[index] + ',' + '_' + ',' + fuhaoL[indexl] + ')')
                    index = index + 1
                    indexl = indexl + 1
                else:
                    middle.append('('+sy[2]+','+sy[1]+','+'_'+','+sy[3]+')')

            elif  len(sy)!=1 and sy[1]=='+':
                middle.append('(' + sy[1] + ',' + fuhao[index] + ',' + fuhao[index+1] + ',' + newtemp() + ')')
                temps.push(temp[-1])
                index = index + 2

            t = status.top()
            A = go
            symbol.push(A)
            status.push(str(Goto[A][int(t)]))
            # f.write('输出 '+' '.join(productions[int(curAct[1])])+ ' 规约'+'\n')
            print('输出 ' + ' '.join(productions[int(curAct[1])]) + ' 规约')
        elif curAct[0:3] == 'acc':
            # f.write('分析完成'+'\n')
            print('分析完成' + '\n')
            break
        else:
            raise error()
        # f.write('状态栈中为 '+status.show()+'\n')
        # f.write('符号栈中为'+symbol.show()+'\n')
        # f.write('输入为 '+ ' '.join(V[i:])+'\n')
        # f.write('\n')
        print('状态栈中为 ' + status.show())
        print('符号栈中为' + symbol.show())
        print('输入为 ' + ' '.join(V[i:]))
        print('\n')

    if t=='0':
        middle.append('(j,_,_' + '101' + ')')
        count = 0
        for each in middle:
            if each[1] == 'j' and each[2] != '>' and count!=len(middle)-1:
                middle[count] = '(j,_,_' + '10' + str(len(middle) + 1) + ')'
            count = count + 1

        count = 1
        for each in middle:
            print('10' + str(count) + ':' + each)
            count = count + 1

    # print(middle)

def main():
    ComPlier = Complier()
    SourceProgram = []
    Filepath = 'D:\\编译原理\\test\\testke.txt'
    for line in open(Filepath, 'r', encoding='UTF-8-sig'):
        line = line.replace('\n', '')
        SourceProgram.append(line)
    SourceProgram = ComPlier.RemoveSpace(SourceProgram)
    sentence=ComPlier.Reader(SourceProgram)
    getRes(sentence)


if __name__ == "__main__":
    print(Action)
    print(Goto)
    main()
