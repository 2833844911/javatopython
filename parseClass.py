

class constantPoolParse:
    def __init__(self, start, fileb, num):
        self.constantpooltable = {}
        # 开始位置
        self.start = start
        # 文件
        self.fileb = fileb
        # constantPool数量
        self.num = num

        self.end = None
        self.off = 0
        self.index = 0

    def CONSTANT_Utf8_info(self):
        self.index += 1
        data = {}
        data["length"] = int(self.fileb[self.start+1: self.start+3].hex(), base=16)
        data['data'] = self.fileb[self.start+3: self.start+3+data["length"]]
        data['type'] = 1
        self.start = self.start+3+data["length"]
        self.constantpooltable[self.index] = data

    def CONSTANT_Integer_info(self):
        self.index += 1
        data = {}
        data['data'] = self.fileb[self.start+1: self.start+5]
        data['type'] = 3
        self.start = self.start+5
        self.constantpooltable[self.index] = data

    def CONSTANT_Float_info(self):
        self.index += 1
        data = {}
        data['data'] = self.fileb[self.start+1: self.start+5]
        data['type'] = 4
        self.start = self.start+5
        self.constantpooltable[self.index] = data

    def CONSTANT_Long_info(self):
        self.index += 1
        data = {}
        data['data'] = self.fileb[self.start+1: self.start+9]
        data['type'] = 5
        self.start = self.start+9
        self.constantpooltable[self.index] = data

    def CONSTANT_Double_info(self):
        self.index += 1
        data = {}
        data['data'] = self.fileb[self.start+1: self.start+9]
        data['type'] = 6
        self.start = self.start+9
        self.constantpooltable[self.index] = data

    def CONSTANT_Class_info(self):
        self.index += 1
        data = {}
        data['data'] = self.fileb[self.start+1: self.start+3]
        data['type'] = 7
        self.start = self.start+3
        self.constantpooltable[self.index] = data
    def CONSTANT_String_info(self):
        self.index += 1
        data = {}
        data['data'] = self.fileb[self.start+1: self.start+3]
        data['type'] = 8
        self.start = self.start+3
        self.constantpooltable[self.index] = data

    def CONSTANT_Fieidref_info(self):
        self.index += 1
        data = {}
        data['classInfo'] = self.fileb[self.start + 1: self.start + 3]
        data['NameAndTypeInfo'] = self.fileb[self.start + 3: self.start + 5]
        data['type'] = 9
        self.start = self.start+5
        self.constantpooltable[self.index] = data

    def CONSTANT_Methodref_info(self):
        self.index += 1
        data = {}
        data['classInfo'] = self.fileb[self.start + 1: self.start + 3]
        data['NameAndTypeInfo'] = self.fileb[self.start + 3: self.start + 5]
        data['type'] = 10
        self.start = self.start+5
        self.constantpooltable[self.index] = data

    def CONSTANT_InterfaceMethodref_info(self):
        self.index += 1
        data = {}
        data['classInfo'] = self.fileb[self.start+1: self.start+3]
        data['nameAndTypeInfo'] = self.fileb[self.start + 3: self.start + 5]
        data['type'] = 11
        self.start = self.start+5
        self.constantpooltable[self.index] = data

    def CONSTANT_NameAndType_info(self):
        self.index += 1
        data = {}
        data['nameInfo'] = self.fileb[self.start+1: self.start+3]
        data['nameType'] = self.fileb[self.start + 3: self.start + 5]
        data['type'] = 12
        self.start = self.start+5
        self.constantpooltable[self.index] = data

    def CONSTANT_InvokeDynamic_info(self):
        self.index += 1
        data = {}
        data['bootstrapMethodAttrIndex'] = self.fileb[self.start + 1: self.start + 3]
        data['nameAndTypeIndex'] = self.fileb[self.start + 3: self.start + 5]
        data['type'] = 18
        self.start = self.start + 5
        self.constantpooltable[self.index] = data

    def CONSTANT_MethodHandle_info(self):
        self.index += 1
        data = {}
        data['referenceKind'] = self.fileb[self.start + 1: self.start + 2]
        data['referenceIndex'] = self.fileb[self.start + 2: self.start + 4]
        data['type'] = 15
        self.start = self.start + 4
        self.constantpooltable[self.index] = data

    def getIndex(self, index):
        data = self.constantpooltable[index].copy()
        if data['type'] == 7 or data['type'] == 8:
            data['data'] = self.constantpooltable[int(data['data'].hex(), base=16)].copy()
        elif data['type'] == 9:
            data['classInfo'] = self.constantpooltable[int(data['classInfo'].hex(), base=16)].copy()
            data['classInfo']['data'] = self.constantpooltable[int(data['classInfo']['data'].hex(), base=16)].copy()
            data['NameAndTypeInfo'] = self.constantpooltable[int(data['NameAndTypeInfo'].hex(), base=16)].copy()
            data['NameAndTypeInfo']['nameInfo'] = self.constantpooltable[
                int(data['NameAndTypeInfo']['nameInfo'].hex(), base=16)].copy()
            data['NameAndTypeInfo']['nameType'] = self.constantpooltable[
                int(data['NameAndTypeInfo']['nameType'].hex(), base=16)].copy()
        elif data['type'] == 10:
            data['classInfo'] = self.constantpooltable[int(data['classInfo'].hex(), base=16)].copy()
            data['classInfo']['data'] = self.constantpooltable[int(data['classInfo']['data'].hex(), base=16)].copy()
            data['NameAndTypeInfo'] = self.constantpooltable[int(data['NameAndTypeInfo'].hex(), base=16)].copy()
            data['NameAndTypeInfo']['nameInfo'] = self.constantpooltable[
                int(data['NameAndTypeInfo']['nameInfo'].hex(), base=16)].copy()
            data['NameAndTypeInfo']['nameType'] = self.constantpooltable[
                int(data['NameAndTypeInfo']['nameType'].hex(), base=16)].copy()
        elif data['type'] == 11:
            data['classInfo'] = self.constantpooltable[int(data['classInfo'].hex(), base=16)].copy()
            data['classInfo']['data'] = self.constantpooltable[int(data['classInfo']['data'].hex(), base=16)].copy()
            data['NameAndTypeInfo'] = self.constantpooltable[int(data['NameAndTypeInfo'].hex(), base=16)].copy()
            data['NameAndTypeInfo']['nameInfo'] = self.constantpooltable[int(data['NameAndTypeInfo']['nameInfo'].hex(), base=16)].copy()
            data['NameAndTypeInfo']['nameType'] = self.constantpooltable[int(data['NameAndTypeInfo']['nameType'].hex(), base=16)].copy()
        elif data['type'] == 12:
            data['nameInfo'] = self.constantpooltable[int(data['nameInfo'].hex(), base=16)].copy()
            data['nameType'] = self.constantpooltable[int(data['nameType'].hex(), base=16)].copy()
        elif data['type'] == 15:
            data['referenceIndex'] = self.getIndex(int(data['referenceIndex'].hex(), base=16)).copy()

        elif data['type'] == 18:
            data['bootstrapMethodAttrIndex'] = "暂时没有解析"
            data['nameAndTypeIndex'] = self.constantpooltable[int(data['nameAndTypeIndex'].hex(), base=16)].copy()
            data['nameAndTypeIndex']['nameInfo'] = self.constantpooltable[
                int(data['nameAndTypeIndex']['nameInfo'].hex(), base=16)].copy()
            data['nameAndTypeIndex']['nameType'] = self.constantpooltable[
                int(data['nameAndTypeIndex']['nameType'].hex(), base=16)].copy()
        return data




    def parseFun(self):
        for _ in range(self.num - 1):
            type = int(self.fileb[self.start])
            if type == 1:
                self.CONSTANT_Utf8_info()
            elif type == 3:
                self.CONSTANT_Integer_info()
            elif type == 4:
                self.CONSTANT_Float_info()
            elif type == 5:
                self.CONSTANT_Long_info()
            elif type == 6:
                self.CONSTANT_Double_info()
            elif type == 7:
                self.CONSTANT_Class_info()
            elif type == 8:
                self.CONSTANT_String_info()
            elif type == 9:
                self.CONSTANT_Fieidref_info()
            elif type == 10:
                self.CONSTANT_Methodref_info()
            elif type == 11:
                self.CONSTANT_InterfaceMethodref_info()
            elif type == 12:
                self.CONSTANT_NameAndType_info()
            elif type == 15:
                self.CONSTANT_MethodHandle_info()
            elif type == 18:
                self.CONSTANT_InvokeDynamic_info()
            else:
                print("常量池解析错误", type)
        self.end = self.start
        self.off = 1

class methodsInfoParse:
    def __init__(self, start, fileb, num, constantpool):
        self.methodInfotable = []
        # 开始位置
        self.start = start
        # 文件
        self.fileb = fileb
        # constantPool数量
        self.num = num
        # 常量池
        self.constantpool = constantpool

        self.end = None
        self.off = 0
        self.index = 0

    def exceptionTable(self):
        data = {}
        data['startPc'] = self.fileb[self.start:self.start+2]
        data['endPc'] = self.fileb[self.start+2:self.start+4]
        data['handlerPc'] = self.fileb[self.start + 4:self.start + 6]
        data['catchType'] = self.fileb[self.start + 6:self.start + 8]
        self.start = self.start + 8
        return data

    def lineNumberTable(self):
        data = {}
        data['startPc'] = self.fileb[self.start:self.start+2]
        data['lineNumber'] = self.fileb[self.start+2:self.start+4]
        self.start = self.start+4
        return data

    def lineNumberTableAttribute(self):
        data = {}
        data['attributeNameIndex'] ={"cbbSour": self.fileb[self.start:self.start+2], "yhhData":self.constantpool.getIndex(int( self.fileb[self.start:self.start+2].hex(), base=16))}
        data["attributeLength"] = self.fileb[self.start+2:self.start+6]
        data['lineNumberTableLength'] = self.fileb[self.start+6: self.start+8]
        self.start = self.start+8
        data["attributeList"] = []
        for _ in range(int(data['lineNumberTableLength'].hex(), base=16)):
            lineNumber = self.lineNumberTable()
            data["attributeList"].append(lineNumber)
        return data

    def localVariableTable(self):
        data = {}
        data['startPc'] = self.fileb[self.start:self.start + 2]
        data['length'] = self.fileb[self.start+2:self.start + 4]
        data['nameIndex'] = {"cbbSour":self.fileb[self.start + 4:self.start + 6], "yhhData":self.constantpool.getIndex(int(self.fileb[self.start + 4:self.start + 6].hex(), base=16))}
        data['descriptorIndex'] = {"cbbSour":self.fileb[self.start + 6:self.start +8 ], "yhhData":self.constantpool.getIndex(int(self.fileb[self.start + 6:self.start +8 ].hex(), base=16))}
        data['index'] = self.fileb[self.start +8: self.start +10]
        self.start = self.start +10
        return data



    def localVariableTableAttribute(self):
        data = {}
        data['attributeNameIndex'] = {"cbbSour":self.fileb[self.start:self.start + 2], "yhhData":self.constantpool.getIndex(int(self.fileb[self.start:self.start + 2].hex(), base=16))}
        data["attributeLength"] = self.fileb[self.start + 2:self.start + 6]
        data['localVariableTableLength'] = self.fileb[self.start + 6: self.start + 8]
        self.start = self.start + 8
        data["attributeList"] = []
        for _ in range(int(data['localVariableTableLength'].hex(), base=16)):
            localVariable = self.localVariableTable()
            data["attributeList"].append(localVariable)
        return data

    def StackMapTable(self):
        data = {}
        data['attributeNameIndex'] = {"cbbSour": self.fileb[self.start:self.start + 2],
                                      "yhhData": self.constantpool.getIndex(
                                          int(self.fileb[self.start:self.start + 2].hex(), base=16))}
        data["attributeLength"] = self.fileb[self.start + 2:self.start + 6]
        data['localVariableTableLength'] = self.fileb[self.start + 6: self.start + 8]
        self.start = self.start + 6
        # 先不解析
        data["attributeList"] = [{"data": self.fileb[self.start: self.start+ int(data["attributeLength"].hex(), base=16)]}]
        self.start = self.start+ int(data["attributeLength"].hex(), base=16)
        return data

    def attributeInfo(self):
        data = {}
        data['attributeNameIndex'] = {"cbbSour":self.fileb[self.start:self.start+2], "yhhData":self.constantpool.getIndex(int(self.fileb[self.start:self.start+2].hex(), base=16))}
        data['attributeLength'] = self.fileb[self.start+2:self.start+6]
        code = data['attributeNameIndex']['yhhData']
        if code['data'] == b'Code':
            data['maxStack'] = self.fileb[self.start+6:self.start+8]
            data['maxLocals'] = self.fileb[self.start + 8:self.start + 10]
            data['codeLength'] = self.fileb[self.start + 10:self.start + 14]
            codelength = int(data['codeLength'].hex(), base=16)
            data['code'] = self.fileb[self.start + 14: self.start + 14 + codelength]
            data['exceptionTableLength'] = self.fileb[self.start + 14 + codelength: self.start + 16 + codelength]
            self.start = self.start + 16 + codelength
            data['exceptionTableList'] = []
            for _ in range(int(data['exceptionTableLength'].hex(), base=16)):
                exception = self.exceptionTable()
                data['exceptionTableList'].append(exception)

            data['attributesCount'] = self.fileb[self.start:self.start+2]
            data['attributeList'] = []
            self.start = self.start+2
            for _ in range(int(data['attributesCount'].hex(), base=16)):
                name = self.constantpool.getIndex(int(self.fileb[self.start:self.start+2].hex(), base=16))['data']
                if name == b'LineNumberTable':
                    lineNumber = self.lineNumberTableAttribute()
                    data['attributeList'].append(lineNumber)
                elif name == b'LocalVariableTable':
                    localVariable = self.localVariableTableAttribute()
                    data['attributeList'].append(localVariable)
                elif name == b'StackMapTable':
                    stackmaptable = self.StackMapTable()
                    data['attributeList'].append(stackmaptable)
                else:
                    print("attributes 解析失败")
        elif code['data'] == b'Exceptions':
            print("attributeInfo Exceptions 解析情况没有考虑")

        else:
            data['info'] = self.fileb[self.start+6]
            self.start = self.start+7
            print("attributeInfo 解析情况没有考虑")
        return data

    def methodInfo(self):
        data = {}
        data['accessFlags'] = self.fileb[self.start:self.start+2]
        data['nameIndex'] = {"cbbSour":self.fileb[self.start+2:self.start+4],"yhhData":self.constantpool.getIndex(int(self.fileb[self.start+2:self.start+4].hex(),base=16))}
        data['descriptorIndex'] = {"cbbSour":self.fileb[self.start + 4:self.start + 6],"yhhData":self.constantpool.getIndex(int(self.fileb[self.start + 4:self.start + 6].hex(),base=16))}
        data['attributesCount'] = self.fileb[self.start + 6:self.start + 8]
        data['attributeList'] = []
        self.start += 8
        for _ in range(int(data['attributesCount'].hex(), base=16)):
            att = self.attributeInfo()
            data['attributeList'].append(att)
        return data


    def parseFun(self):
        for _ in range(self.num):
            method = self.methodInfo()
            self.methodInfotable.append(method)
        self.end = self.start
        self.off = 1


class fieldInfoPrase:
    def __init__(self, start, fileb, num, constantpool):
        self.fieldInfoPrase = []
        # 开始位置
        self.start = start
        # 文件
        self.fileb = fileb
        # constantPool数量
        self.num = num
        # 常量池
        self.constantpool = constantpool

        self.end = None
        self.off = 0
        self.index = 0

    def exceptionTable(self):
        data = {}
        data['startPc'] = self.fileb[self.start:self.start+2]
        data['endPc'] = self.fileb[self.start+2:self.start+4]
        data['handlerPc'] = self.fileb[self.start + 4:self.start + 6]
        data['catchType'] = self.fileb[self.start + 6:self.start + 8]
        self.start = self.start + 8
        return data

    def lineNumberTable(self):
        data = {}
        data['startPc'] = self.fileb[self.start:self.start+2]
        data['lineNumber'] = self.fileb[self.start+2:self.start+4]
        self.start = self.start+4
        return data

    def lineNumberTableAttribute(self):
        data = {}
        data['attributeNameIndex'] ={"cbbSour": self.fileb[self.start:self.start+2], "yhhData":self.constantpool.getIndex(int( self.fileb[self.start:self.start+2].hex(), base=16))}
        data["attributeLength"] = self.fileb[self.start+2:self.start+6]
        data['lineNumberTableLength'] = self.fileb[self.start+6: self.start+8]
        self.start = self.start+8
        data["attributeList"] = []
        for _ in range(int(data['lineNumberTableLength'].hex(), base=16)):
            lineNumber = self.lineNumberTable()
            data["attributeList"].append(lineNumber)
        return data

    def localVariableTable(self):
        data = {}
        data['startPc'] = self.fileb[self.start:self.start + 2]
        data['length'] = self.fileb[self.start+2:self.start + 4]
        data['nameIndex'] = {"cbbSour":self.fileb[self.start + 4:self.start + 6], "yhhData":self.constantpool.getIndex(int(self.fileb[self.start + 4:self.start + 6].hex(), base=16))}
        data['descriptorIndex'] = {"cbbSour":self.fileb[self.start + 6:self.start +8 ], "yhhData":self.constantpool.getIndex(int(self.fileb[self.start + 6:self.start +8 ].hex(), base=16))}
        data['index'] = self.fileb[self.start +8: self.start +10]
        self.start = self.start +10
        return data



    def localVariableTableAttribute(self):
        data = {}
        data['attributeNameIndex'] = {"cbbSour":self.fileb[self.start:self.start + 2], "yhhData":self.constantpool.getIndex(int(self.fileb[self.start:self.start + 2].hex(), base=16))}
        data["attributeLength"] = self.fileb[self.start + 2:self.start + 6]
        data['localVariableTableLength'] = self.fileb[self.start + 6: self.start + 8]
        self.start = self.start + 8
        data["attributeList"] = []
        for _ in range(int(data['localVariableTableLength'].hex(), base=16)):
            localVariable = self.localVariableTable()
            data["attributeList"].append(localVariable)
        return data

    def StackMapTable(self):
        data = {}
        data['attributeNameIndex'] = {"cbbSour": self.fileb[self.start:self.start + 2],
                                      "yhhData": self.constantpool.getIndex(
                                          int(self.fileb[self.start:self.start + 2].hex(), base=16))}
        data["attributeLength"] = self.fileb[self.start + 2:self.start + 6]
        data['localVariableTableLength'] = self.fileb[self.start + 6: self.start + 8]
        self.start = self.start + 6
        # 先不解析
        data["attributeList"] = [{"data": self.fileb[self.start: self.start+ int(data["attributeLength"].hex(), base=16)]}]
        self.start = self.start+ int(data["attributeLength"].hex(), base=16)
        return data

    def attributeInfo(self):
        data = {}
        data['attributeNameIndex'] = {"cbbSour":self.fileb[self.start:self.start+2], "yhhData":self.constantpool.getIndex(int(self.fileb[self.start:self.start+2].hex(), base=16))}
        data['attributeLength'] = self.fileb[self.start+2:self.start+6]
        code = data['attributeNameIndex']['yhhData']
        if code['data'] == b'Code':
            data['maxStack'] = self.fileb[self.start+6:self.start+8]
            data['maxLocals'] = self.fileb[self.start + 8:self.start + 10]
            data['codeLength'] = self.fileb[self.start + 10:self.start + 14]
            codelength = int(data['codeLength'].hex(), base=16)
            data['code'] = self.fileb[self.start + 14: self.start + 14 + codelength]
            data['exceptionTableLength'] = self.fileb[self.start + 14 + codelength: self.start + 16 + codelength]
            self.start = self.start + 16 + codelength
            data['exceptionTableList'] = []
            for _ in range(int(data['exceptionTableLength'].hex(), base=16)):
                exception = self.exceptionTable()
                data['exceptionTableList'].append(exception)

            data['attributesCount'] = self.fileb[self.start:self.start+2]
            data['attributeList'] = []
            self.start = self.start+2
            for _ in range(int(data['attributesCount'].hex(), base=16)):
                name = self.constantpool.getIndex(int(self.fileb[self.start:self.start+2].hex(), base=16))['data']
                if name == b'LineNumberTable':
                    lineNumber = self.lineNumberTableAttribute()
                    data['attributeList'].append(lineNumber)
                elif name == b'LocalVariableTable':
                    localVariable = self.localVariableTableAttribute()
                    data['attributeList'].append(localVariable)
                elif name == b'StackMapTable':
                    stackmaptable = self.StackMapTable()
                    data['attributeList'].append(stackmaptable)
                else:
                    print("attributes 解析失败")
        elif code['data'] == b'Exceptions':
            print("attributeInfo Exceptions 解析情况没有考虑")

        else:
            data['info'] = self.fileb[self.start+6]
            self.start = self.start+7
            print("attributeInfo 解析情况没有考虑")
        return data

    def methodInfo(self):
        data = {}
        data['accessFlags'] = self.fileb[self.start:self.start+2]
        data['nameIndex'] = {"cbbSour":self.fileb[self.start+2:self.start+4],"yhhData":self.constantpool.getIndex(int(self.fileb[self.start+2:self.start+4].hex(),base=16))}
        data['descriptorIndex'] = {"cbbSour":self.fileb[self.start + 4:self.start + 6],"yhhData":self.constantpool.getIndex(int(self.fileb[self.start + 4:self.start + 6].hex(),base=16))}
        data['attributesCount'] = self.fileb[self.start + 6:self.start + 8]
        data['attributeList'] = []
        self.start += 8
        for _ in range(int(data['attributesCount'].hex(), base=16)):
            att = self.attributeInfo()
            data['attributeList'].append(att)
        return data


    def parseFun(self):
        for _ in range(self.num):
            method = self.methodInfo()
            self.fieldInfoPrase.append(method)
        self.end = self.start
        self.off = 1

class jvmParse:
    def __init__(self, filePath):
        with open(filePath, 'rb') as f:
            self.fileb = f.read()

        self.start = 0

        # 魔数
        self.magic = None
        # 次版本号
        self.minorversion = None
        # 主版本号
        self.majorversion = None
        # 常量池数量
        self.constantpoolcount = None
        # 常量池
        self.constantpool = None
        # 类的权限
        self.accessflags = None
        # 类名
        self.thisclass = None
        # 父类名
        self.supperclass = None
        # 实现的接口数量
        self.interfacescount = None
        # field数量
        self.fieldscount = None
        # field
        self.fieldInfo = None
        # 方法数量
        self.methodscount = None
        # 方法
        self.methodsinfo = None
        # 类属性数量
        self.attributescount = None
        # 类属性
        self.attributeList = None


    def getMagic(self):
        self.magic = self.fileb[:4]

    def minorVersion(self):
        self.minorversion = int(self.fileb[4:6].hex(), base=16)

    def majorVersion(self):
        self.majorversion = int(self.fileb[6:8].hex(), base=16)

    def constantPoolCount(self):
        self.constantpoolcount = int(self.fileb[8:10].hex(), base=16)

    def constantPool(self):
        self.constantpool = constantPoolParse(10, self.fileb, self.constantpoolcount)
        self.constantpool.parseFun()
        self.start = self.constantpool.end

    def accessFlags(self):
        self.accessflags = int(self.fileb[self.start:self.start+2].hex(), base=16)
        self.start = self.start+2

    def thisClass(self):

        self.thisclass = {"cbbSour": self.fileb[self.start:self.start+2],"yhhData":int(self.fileb[self.start:self.start+2].hex(), base=16)}
        self.start = self.start+2

    def supperClass(self):
        self.supperclass = {"cbbSour": self.fileb[self.start:self.start+2],"yhhData":int(self.fileb[self.start:self.start+2].hex(), base=16)}
        self.start = self.start+2

    def interfacesCount(self):
        self.interfacescount = int(self.fileb[self.start:self.start+2].hex(), base=16)
        self.start = self.start+2

    def interfaces(self):
        pass

    def fieldsCount(self):
        self.fieldscount = int(self.fileb[self.start:self.start+2].hex(), base=16)
        self.start = self.start + 2

    def fieldsInfo(self):
        self.fieldInfo = fieldInfoPrase(self.start, self.fileb, self.fieldscount, self.constantpool)
        self.fieldInfo.parseFun()
        self.start = self.fieldInfo.end

    def methodsCount(self):
        self.methodscount = int(self.fileb[self.start:self.start + 2].hex(), base=16)
        self.start = self.start + 2

    def methodsInfo(self):
        self.methodsinfo = methodsInfoParse(self.start, self.fileb, self.methodscount, self.constantpool)
        self.methodsinfo.parseFun()
        self.start = self.methodsinfo.end

    def attributesCount(self):
        self.attributescount = self.fileb[self.start:self.start+2]
        self.start = self.start+2

    def innerClassInfo(self):
        data = {}
        data['innerClassInfoIndex'] = self.constantpool.getIndex(int(self.fileb[self.start: self.start+2].hex(), base=16))
        data['outerClassInfoIndex'] = self.constantpool.getIndex(int(self.fileb[self.start+2: self.start+4].hex(), base=16))
        data['innerNameIndex'] = self.constantpool.getIndex(
            int(self.fileb[self.start + 4: self.start + 6].hex(), base=16))
        data['innerClassAccessFlags'] = self.fileb[self.start + 6: self.start + 8]
        self.start += 8
        return data

    def bootstrapMethod(self):
        data = {}
        data['bootstrapMethodRef'] = self.constantpool.getIndex(int(self.fileb[self.start:self.start+2].hex(), base=16))
        data['numBootStrapArguments'] = int(self.fileb[self.start+2:self.start + 4].hex(), base=16)
        data['bootStrapArguments'] = []
        self.start = self.start + 4
        for _ in range(data['numBootStrapArguments']):
            s = self.constantpool.getIndex(int(self.fileb[self.start:self.start + 2].hex(), base=16))
            data['bootStrapArguments'].append(s)
            self.start = self.start + 2
        return data

    def attributes(self):
        self.attributeList = []
        for _ in range(int(self.attributescount.hex(), base=16)):
            d = self.constantpool.getIndex(int(self.fileb[self.start:self.start+2].hex(), base=16))
            if d['data'] == b'SourceFile':
                data = {}
                data['attributeNameIndex'] = {"cbbSour":self.fileb[self.start:self.start+2], "yhhData":self.constantpool.getIndex(int(self.fileb[self.start:self.start+2].hex(), base=16))}
                data['attributeLength'] = self.fileb[self.start+2:self.start + 6]
                data['sourcefileIndex'] = {"cbbSour":self.fileb[self.start  + 6:self.start + 8], "yhhData":self.constantpool.getIndex(int(self.fileb[self.start + 6:self.start + 8].hex(), base=16))}
                self.start = self.start + 8
                self.attributeList.append(data)
            elif d['data'] == b'BootstrapMethods':
                data = {}
                data['attributeNameIndex'] = {"cbbSour": self.fileb[self.start:self.start + 2],
                                              "yhhData": self.constantpool.getIndex(
                                                  int(self.fileb[self.start:self.start + 2].hex(), base=16))}
                data['attributeLength'] = self.fileb[self.start + 2:self.start + 6]
                data['numBootstrapMethods'] = int(self.fileb[self.start + 6: self.start + 8].hex(), base=16)
                self.start += 8
                data['bootstrapMethod'] = []
                for _ in range(data['numBootstrapMethods']):
                    data['bootstrapMethod'].append(self.bootstrapMethod())
                self.attributeList.append(data)
            elif d['data'] == b'InnerClasses':
                data = {}
                data['attributeNameIndex'] = {"cbbSour": self.fileb[self.start:self.start + 2],
                                              "yhhData": self.constantpool.getIndex(
                                                  int(self.fileb[self.start:self.start + 2].hex(), base=16))}
                data['attributeLength'] = self.fileb[self.start + 2:self.start + 6]
                data['numberOfClasses'] = int(self.fileb[self.start + 6: self.start + 8].hex(), base=16)
                self.start += 8
                data['innerClassInfo'] = []
                for _ in range(data['numberOfClasses']):
                    data['innerClassInfo'].append(self.innerClassInfo())
                self.attributeList.append(data)


    def startFun(self):
        self.getMagic()
        self.minorVersion()
        self.majorVersion()
        self.constantPoolCount()
        self.constantPool()
        self.accessFlags()
        self.thisClass()
        self.supperClass()
        self.interfacesCount()
        self.interfaces()
        self.fieldsCount()
        self.fieldsInfo()
        self.methodsCount()
        self.methodsInfo()
        self.attributesCount()
        self.attributes()


if __name__ == '__main__':
    s = jvmParse("./test/uiop.class")
    s.startFun()
    print()