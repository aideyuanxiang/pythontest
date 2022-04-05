Operation = ['*', '-', '/', '=', '>', '<', '>=', '==', '<=', '%', '+', '+=', '-=', '*=', '/=']  # 词法分析器中分别运算符
Delimiter = ['(', ')', ',', ';', '.', '{', '}', '<', '>', '"']  # 词法分析器中分别界符
KeyWord = ['bool', 'char', 'class', 'double', 'false', 'float', 'getchar', 'include', 'int', 'long', 'main',
           'null', 'open', 'printf','private', 'public', 'put', 'read', 'return', 'short', 'scanf', 'signed', 'static',
           'stdio', 'string','struct', 'true','unsigned', 'void']


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
        valueList=[]
        f = open('D:\\编译原理\\test\\result.txt', 'w')
        for String in List:
            Letter = ''
            Digit = ''
            letter = ''
            index = 0
            for Char in String:

                if Char=='i':
                    valueList.append('i')

                if (index < len(String) - 1):
                    index += 1
                if (self.IsLetter(Char)):
                    if (self.IsLetter(String[index]) or self.IsDigit(String[index])):
                        Letter += Char
                    elif (self.IsSpace(String[index]) or (String[index] in Delimiter) or (
                            String[index] in Operation) or (String[index:index + 2] in Operation)):
                        Letter += Char
                        ResultList.append(Letter)
                        if Letter in KeyWord:
                            f.write('<' + Letter + ',关键字>'+'\n')
                        else:
                            f.write('<' + Letter + ',标识符>'+'\n')
                        Letter = ''
                else:
                    if (self.IsDigit(Char)):
                        if (self.IsLetter(String[index]) or self.IsDigit(String[index])):
                            Digit += Char
                        elif (self.IsSpace(String[index]) or (String[index] in Delimiter) or (
                                String[index] in Operation) or (String[index:index + 2] in Operation)):
                            Digit += Char
                            ResultList.append(Digit)
                            f.write('<' + Digit + ',常数>'+'\n')
                            Digit = ''
                    else:
                        if (Char == '#'):
                            ResultList.append('#')
                            f.write('<#,宏定义符号>'+'\n')
                        else:
                            if (Char in Delimiter):
                                ResultList.append(Char)
                                f.write('<' + Char + ',界符>'+'\n')
                            else:
                                if (Char in Operation):
                                    letter += Char
                                    if (String[index] in Operation):
                                        letter += String[index]
                                        ResultList.append(letter)
                                        f.write('<' + letter + ',运算符>'+'\n')
                                        letter = ''
                                    else:
                                        ResultList.append(letter)
                                        f.write('<' + letter + ',运算符>'+'\n')
                                        letter = ''
                                else:
                                    if (self.IsSpace(Char)):
                                        pass
        return ResultList,valueList

def main():
    ComPlier = Complier()
    SourceProgram = []
    Filepath = 'D:\\编译原理\\test\\test.txt'
    for line in open(Filepath, 'r', encoding='UTF-8-sig'):
        line = line.replace('\n', '')
        SourceProgram.append(line)
    SourceProgram = ComPlier.RemoveSpace(SourceProgram)
    ComPlier.Reader(SourceProgram)


if __name__ == "__main__":
    main()