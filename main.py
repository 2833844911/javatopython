
from parseClass import jvmParse


# 解析签名
class parseArgsF:
    def __init__(self, data):
        self.sig = data
        # 参数个数
        self.argsNumber = 0
        # 参数
        self.argsList = []
        # 返回值
        self.returnT = None

    def parseFun(self):
        off = 0
        isre = 0
        da = ''
        for i in list(self.sig):
            if i == '(':
                continue
            elif i == 'B' or i == "C" or i == "S" or i == "I" or i == "F" or i == "J" or i == "D" or i == "V":
                da += i

                if isre == 0 and off == 0:
                    self.argsNumber += 1
                    self.argsList.append(da)
                    da = ''
                elif isre == 1 and off == 0:
                    self.returnT = da
                    return
            elif i == 'L':
                off = 1
                da += i
            elif i == '[':
                da += i
            elif i == ';':
                off = 0
                if isre == 0 and off == 0:
                    self.argsNumber += 1
                    self.argsList.append(da)
                    da = ''
                elif isre == 1 and off == 0:
                    self.returnT = da
                    return
            elif i == ')':
                isre = 1
                off = 0
                continue
            else:
                da += i


# 解析code
class parseClass:
    def __init__(self, code):
        self.code = code
        self.dataall = {}

    def parseFun(self):
        bh = 0
        data = []
        start = 0
        maxLength = len(self.code)
        while 1:
            if maxLength <= start:
                break

            if self.code[start] in [0, 87, 50, 190, 90,1,2,3,4,5,6,7,8,26,27,28,29, 75,76,77,78,42,43,44,45,59,60,61,62, 172, 87, 177, 96, 89, 176, 100, 104, 108]:
                data.append(self.code[start])
                self.dataall[start] = data.copy()
                start += 1
                bh += 1

                data = []
            elif self.code[start] in [180, 181, 182,187, 183, 184, 178, 166, 165, 159, 160, 161, 162, 163, 164, 17, 167, 132, 153, 154, 155,156, 157, 158]:

                data.append(self.code[start])
                data.append(self.code[start+1: start+3])
                self.dataall[start] = data.copy()
                data = []
                start = start+3

                bh += 1
            elif self.code[start] in [18, 58, 25, 16, 54, 21]:

                data.append(self.code[start])
                data.append(self.code[start+1])
                self.dataall[start] = data.copy()

                data = []
                start = start+2
                bh += 1
            elif self.code[start] in [186]:

                data.append(self.code[start])
                data.append(self.code[start+1: start+3])
                data.append(self.code[start + 3: start + 5])
                self.dataall[start] = data.copy()

                data = []
                start = start+5
                bh += 1
            else:
                #print("指令未解析", self.code[start])
                break


class myFunCall:
    def __init__(self, name, data, supperstack, types, args):
        self.off = 0
        self.Code = None
        self.argsre = None
        self.argsre = data
        self.supperstack = supperstack
        self.types = types

        self.args = []
        self.retu = None
        self.retu = None
        self.bootargs = args
        self.funCall()
        self.funList(name)


    def funList(self,data):
        if data == "java/lang/Object-<init>.()V":
            self.retu = None
        elif data == 'java/lang/String-replace.(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;':
            self.args = self.args[::-1]
            self.retu = self.args[0].replace(self.args[1], self.args[2])
            self.supperstack.append(self.retu)
        elif data == "java/lang/StringBuilder-append.(Ljava/lang/String;)Ljava/lang/StringBuilder;":
            # #print(self.args)
            self.retu = self.args[0]
            self.supperstack.append(self.retu)
        elif data == "java/lang/StringBuilder-toString.()Ljava/lang/String;":
            # #print("is to STring")
            # #print(self.argsre)
            # #print(self.supperstack)
            s = self.supperstack.pop()
            self.supperstack.append(s)
        elif data == 'cbbtopython-print.(I)V' or data == 'cbbtopython-print.(Ljava/lang/String;)V':
            print("#print",self.args[0])
        elif data == 'java/lang/String-split.(Ljava/lang/String;)[Ljava/lang/String;':
            p = self.supperstack.pop()
            #print("dada",self.args,p )

            self.retu = p.split(self.args[0])
            self.supperstack.append(self.retu)
        elif data == 'java/lang/invoke/StringConcatFactory-makeConcatWithConstants.(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;' or data == 'java/lang/invoke/StringConcatFactory-makeConcatWithConstants.(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;':
            index = 0
            d = self.bootargs['bootStrapArguments'][0]['data']['data'].split(b'\x01')
            da = b''
            if len(self.args) == 3:
                self.args.append(self.args.pop(0))
            for i in d:
                da += i
                if index >= len(self.args):
                    continue
                da += self.args[index].encode()
                index += 1

            self.retu = da.decode()
            self.supperstack.append(self.retu)
        elif data == 'java/lang/String-valueOf.(I)Ljava/lang/String;':
            self.retu = str(self.args[0])
            self.supperstack.append(self.retu)
        else:
            print("找不到方法", data)

    def funCall(self):
        # #print(self.supperstack, self.argsre.argsNumber)
        if self.argsre.argsNumber == 0:
            return
        for i in range(self.argsre.argsNumber):
            self.args.append(self.supperstack.pop())
        # if self.types == "invokespecial" or self.types == "invokevirtual":
        #     # 传入this
        #     ags = self.supperstack.pop()
        #     self.args.append(ags)




class runSme:
    def __init__(self, data, clstack, LocalVariableTable, createfunstack, constantpool, supperstack, bootstrapMethod,globalThis,init=0):
        self.off = 0
        self.Code = None
        self.argsre = None
        self.globalThis = globalThis
        self.clstack = clstack
        self.createfunstack = createfunstack
        self.LocalVariableTable = LocalVariableTable
        self.argsre = data['argsre']
        self.constantpool = constantpool
        self.supperstack = supperstack
        self.bootstrapMethod = bootstrapMethod

        self.argsme = []
        for i in range(self.argsre.argsNumber):
            ags = self.clstack.pop()
            self.argsme.append(ags)

        for index, info in enumerate(self.argsme):
            self.LocalVariableTable[index+init]['data'] = info

        for i in data['attributeList']:
            if i['attributeNameIndex']['yhhData']['data'] == b'Code':
                self.off = 1
                self.Code = i['codeList'].dataall


    def findModth(self, needFindFun, type=None , args=None):
        argsre = parseArgsF(needFindFun.split('.')[1])
        argsre.parseFun()
        # #print(argsre.argsNumber,needFindFun.split('.')[1])
        if needFindFun in self.createfunstack:
            value = self.createfunstack[needFindFun]
            LocalVariableTable = value['LocalVariableTable'].copy()
            clstack = value['clstack'].copy()

            u = []
            for i in range(argsre.argsNumber):
                ags = self.clstack.pop()
                u.append(ags)
            clstack+=u[::]
            s = runSme(value, clstack, LocalVariableTable, self.createfunstack, self.constantpool,self.clstack, self.bootstrapMethod, self.globalThis)
            s.run()

        else:
            da = self.myfun(needFindFun, argsre, type, args)
            if da == False:
                pass


    def myfun(self, data, argsre, type, args):

        myFunCall(data, argsre, self.clstack, type, args)


    def pop(self):
        self.clstack.pop()

    def aload_0(self):
        self.clstack.append(self.LocalVariableTable[0]['data'])
    def aload_1(self):
        self.clstack.append(self.LocalVariableTable[1]['data'])
    def aload_2(self):
        self.clstack.append(self.LocalVariableTable[2]['data'])
    def aload_3(self):
        self.clstack.append(self.LocalVariableTable[3]['data'])
    def iload_3(self):
        self.clstack.append(self.LocalVariableTable[3]['data'])
    def iload_2(self):
        self.clstack.append(self.LocalVariableTable[2]['data'])
    def iload_1(self):
        self.clstack.append(self.LocalVariableTable[1]['data'])
    def iload_0(self):
        self.clstack.append(self.LocalVariableTable[0]['data'])

    def iadd(self):
        a = self.clstack.pop()
        b = self.clstack.pop()
        s = a + b
        self.clstack.append(s)

    def isub(self):
        a = self.clstack.pop()
        b = self.clstack.pop()
        s = b - a
        self.clstack.append(s)

    def imul(self):
        a = self.clstack.pop()
        b = self.clstack.pop()
        s = int(a * b)
        self.clstack.append(s)

    def idiv(self):
        a = self.clstack.pop()
        b = self.clstack.pop()
        s = int(b / a)
        self.clstack.append(s)

    def dup(self):
        # #print("dup :")
        # #print(self.clstack)
        a = self.clstack.pop()
        self.clstack.append(a)
        self.clstack.append(a)

    def invokespecial(self, data):
        funInfo = self.constantpool.getIndex(int(data[1].hex(), base=16))
        needFindFun = funInfo['classInfo']['data']['data'].decode() +'-'+funInfo['NameAndTypeInfo']['nameInfo']['data'].decode()+'.'+funInfo['NameAndTypeInfo']['nameType']['data'].decode()
        #print("invokespecial",needFindFun)
        argsre = parseArgsF(needFindFun.split('.')[1])
        argsre.parseFun()
        args = []
        for i in range(argsre.argsNumber):
            _ = self.clstack.pop()
            # #print(_)
            args.append(_)
        this = self.clstack.pop()
        if needFindFun == 'java/lang/Object-<init>.()V':
            self.findModth(needFindFun, 'invokespecial')
        elif type(this) == type({}) and "cbbINfo" in this:
            # #print(this)
            args = [this] + args
            this[needFindFun](*args)
        else:
            this.callFun(needFindFun, self.clstack, args)


    def new(self, data):

        funInfo = self.constantpool.getIndex(int(data[1].hex(), base=16))
        needFindClass = funInfo['data']['data'].decode()
        # #print("needFindClass", needFindClass)
        # #print(self.clstack)

        if needFindClass == "cbbtopython$arrayt":
            self.clstack.append(
                {"data": [], "cbbINfo": 1,
                 "cbbtopython$arrayt-<init>.()V": self.java_lang_StringBuilder_init,
                 "cbbtopython$arrayt-put.(Ljava/lang/String;)V": self.cbbtopython_arrayt_put,
                 "cbbtopython$arrayt-put.(I)V": self.cbbtopython_arrayt_put,
                 "cbbtopython$arrayt-sget.(I)Ljava/lang/String;": self.cbbtopython_arrayt_get,
                 "cbbtopython$arrayt-iget.(I)I": self.cbbtopython_arrayt_get,
                 "cbbtopython$arrayt-ipop.(I)I": self.cbbtopython_arrayt_pop,
                 "cbbtopython$arrayt-spop.(I)Ljava/lang/String;": self.cbbtopython_arrayt_pop,
                 })
        elif needFindClass == 'java/lang/StringBuilder':
            self.clstack.append({"data":"", "cbbINfo": 1, "java/lang/StringBuilder-<init>.()V": self.java_lang_StringBuilder_init,"java/lang/StringBuilder-append.(Ljava/lang/String;)Ljava/lang/StringBuilder;": self.java_lang_StringBuilder_append,
                                 "java/lang/StringBuilder-toString.()Ljava/lang/String;":self.java_lang_StringBuilder_toString
                                 })
        else:
            # #print("is open:", needFindClass)
            s = JVM("./test/"+ needFindClass+".class", 1)
            s.start(needFindClass)
            self.clstack.append(s)


    def invokevirtual(self, data):
        funInfo = self.constantpool.getIndex(int(data[1].hex(), base=16))
        needFindFun = funInfo['classInfo']['data']['data'].decode() + '-' + funInfo['NameAndTypeInfo']['nameInfo'][
            'data'].decode() + '.' + funInfo['NameAndTypeInfo']['nameType']['data'].decode()
        argsre = parseArgsF(needFindFun.split('.')[1])
        argsre.parseFun()
        # #print("length:", argsre.argsNumber)
        # #print(self.clstack)
        args = []

        if needFindFun == 'java/lang/Object-<init>.()V' or needFindFun == 'java/lang/String-split.(Ljava/lang/String;)[Ljava/lang/String;':
            self.findModth(needFindFun, 'invokevirtual')
            return

        for i in range(argsre.argsNumber):
            _ = self.clstack.pop()
            # #print(_)
            args.append(_)
        this = self.clstack.pop()
        #print("this", this)
        #print("args", args)
        if type(this) == type({}) and "cbbINfo" in this:
            # #print("iscome", self.clstack, args)
            args = [this]+args
            this[needFindFun](*args)
        else:
            this.callFun(needFindFun, self.clstack, args)

    def putfield(self, data):
        fieldInfo = self.constantpool.getIndex(int(data[1].hex(), base=16))
        d = self.clstack.pop()
        name = fieldInfo['NameAndTypeInfo']['nameInfo']['data'].decode()
        fyy = self.clstack.pop()
        # #print("putfield", d)
        # #print(self.clstack)
        self.globalThis[name] = d
        # #print(fieldInfo)
        # #print(self.globalThis)

    def getfield(self, data):
        # #print("isco")
        # #print(self.globalThis)
        fieldInfo = self.constantpool.getIndex(int(data[1].hex(), base=16))
        name = fieldInfo['NameAndTypeInfo']['nameInfo']['data'].decode()
        fyy = self.clstack.pop()

        d = self.globalThis[name]
        # #print("getfield", d)
        self.clstack.append(d)
        # #print(fieldInfo)
        # #print(self.globalThis)
        # #print(self.clstack)

    def dup_x1(self):
        # #print("dup_x1")
        # #print(self.clstack)
        s = self.clstack.pop()
        # #print([s])
        self.clstack.append(s)
        self.clstack.append(s)
        self.clstack.append(s)

    def invokestatic(self, data):
        # #print(self.clstack)
        funInfo = self.constantpool.getIndex(int(data[1].hex(), base=16))

        needFindFun = funInfo['classInfo']['data']['data'].decode() + '-' + funInfo['NameAndTypeInfo']['nameInfo'][
            'data'].decode() + '.' + funInfo['NameAndTypeInfo']['nameType']['data'].decode()
        self.findModth(needFindFun, 'invokestatic')
    def invokedynamic(self, data):
        funInfo = self.constantpool.getIndex(int(data[1].hex(), base=16))
        args = self.bootstrapMethod[int(data[2].hex(), base=16)]
        needFindFun = args['bootstrapMethodRef']['referenceIndex']['classInfo']['data']["data"].decode()+'-'+args['bootstrapMethodRef']['referenceIndex']['NameAndTypeInfo']['nameInfo']['data'].decode() + '.' + funInfo['nameAndTypeIndex']['nameType']['data'].decode()
        args = self.bootstrapMethod[int(data[2].hex(), base=16)]
        self.findModth(needFindFun, 'invokedynamic', args=args)

    def java_lang_StringBuilder_init(self, this):
        #print("use java_lang_StringBuilder_init")
        # #print(self.LocalVariableTable)
        pass

    def java_lang_StringBuilder_append(self, this, data):
        #print("java_lang_StringBuilder_append")
        #print(this)
        #print(data)
        this['data'] += data
        self.clstack.append(this)

    def java_lang_StringBuilder_toString(self,this):
        #print("java_lang_StringBuilder_toString",this)
        self.clstack.append(this['data'])

    def cbbtopython_arrayt_put(self, this, data):
        this['data'].append(data)

    def cbbtopython_arrayt_get(self, this, data):
        s = this['data'][data]
        self.clstack.append(s)

    def cbbtopython_arrayt_pop(self, this, data=None):
        s = this['data'].pop(data)
        self.clstack.append(s)



    def if_acmpne(self, data):
        s = self.clstack.pop()
        a = self.clstack.pop()

        if s != a:
            d = self.getint(int(data[1].hex(), base=16))
            return d
        return 3

    def ifeq(self, data):
        s = self.clstack.pop()
        if s == 0:
            return self.getint(int(data[1].hex(), base=16))
        return 3

    def ifne(self, data):
        s = self.clstack.pop()
        if s != 0:
            return self.getint(int(data[1].hex(), base=16))
        return 3

    def iflt(self, data):
        s = self.clstack.pop()
        if s < 0:
            return self.getint(int(data[1].hex(), base=16))
        return 3
    def ifle(self, data):
        s = self.clstack.pop()
        if s <= 0:
            return self.getint(int(data[1].hex(), base=16))
        return 3

    def ifgt(self, data):
        s = self.clstack.pop()
        if s > 0:
            return self.getint(int(data[1].hex(), base=16))
        return 3
    def ifge(self, data):
        s = self.clstack.pop()
        if s >= 0:
            return self.getint(int(data[1].hex(), base=16))
        return 3

    def if_acmpeq(self, data):
        s = self.clstack.pop()
        a = self.clstack.pop()
        if s == a:
            return self.getint(int(data[1].hex(), base=16))
        return 3

    def if_icmpeq(self, data):
        s = self.clstack.pop()
        a = self.clstack.pop()
        if s == a:
            return self.getint(int(data[1].hex(), base=16))
        return 3
    def if_icmpne(self, data):
        s = self.clstack.pop()
        a = self.clstack.pop()
        if s != a:
            d = self.getint(int(data[1].hex(), base=16))
            return d
        return 3

    def if_icmplt(self, data):
        s = self.clstack.pop()
        a = self.clstack.pop()
        if s < a:
            return self.getint(int(data[1].hex(), base=16))
        return 3

    def if_icmpge(self, data):
        s = self.clstack.pop()
        a = self.clstack.pop()
        # #print(s,a)
        if s <= a:
            d = self.getint(int(data[1].hex(), base=16))
            # #print("come", d)
            return d
        return 3

    def if_icmpgt(self, data):
        s = self.clstack.pop()
        a = self.clstack.pop()
        if s > a:
            return self.getint(int(data[1].hex(), base=16))
        return 3

    def if_icmple(self, data):
        s = self.clstack.pop()
        a = self.clstack.pop()
        if s >= a:
            return self.getint(int(data[1].hex(), base=16))
        return 3

    def getint(self, data):
        if data < 0x8000:
            return data
        else:
            return data - 0x10000

    def getint1(self, data):
        if data < 128:
            return data
        else:
            return data - 256

    def Jreturn(self):
        pass

    def areturn(self):
        a = self.clstack.pop()
        self.supperstack.append(a)

    def ireturn(self):
        a = self.clstack.pop()
        self.supperstack.append(a)

    def ldc(self, data):
        stringInfo = self.constantpool.getIndex(int(data[1]))['data']['data'].decode()
        self.clstack.append(stringInfo)

    def astore_1(self):
        s = self.clstack.pop()
        self.LocalVariableTable[1]['data'] = s

    def astore_0(self):
        s = self.clstack.pop()
        self.LocalVariableTable[0]['data'] = s

    def astore_2(self):
        s = self.clstack.pop()
        self.LocalVariableTable[2]['data'] = s

    def astore_3(self):
        s = self.clstack.pop()
        self.LocalVariableTable[3]['data'] = s

    def bipush(self, data):
        s = int(data[1])
        self.clstack.append(s)

    def sipush(self, data):
        s = int(data[1].hex(), base=16)
        self.clstack.append(s)

    def istore_3(self):
        s = self.clstack.pop()
        self.LocalVariableTable[3]['data'] = s
    def istore_2(self):
        s = self.clstack.pop()
        self.LocalVariableTable[2]['data'] = s
    def istore_1(self):
        s = self.clstack.pop()
        self.LocalVariableTable[1]['data'] = s
    def istore_0(self):
        s = self.clstack.pop()
        self.LocalVariableTable[0]['data'] = s
    def istore(self, data):
        s = self.clstack.pop()
        self.LocalVariableTable[int(data[1])]['data'] = s

    def astore(self, data):
        s = self.clstack.pop()
        self.LocalVariableTable[int(data[1])]['data'] = s
    def iload(self, data):
        s = self.LocalVariableTable[int(data[1])]['data']
        self.clstack.append(s)
    def iconst_m1(self):
        self.clstack.append(-1)
    def iconst_0(self):
        self.clstack.append(0)
    def iconst_1(self):
        self.clstack.append(1)

    def aload(self,data):
        s = self.LocalVariableTable[int(data[1])]['data']
        self.clstack.append(s)


    def iconst_2(self):
        self.clstack.append(2)

    def iconst_3(self):
        self.clstack.append(3)
    def iconst_4(self):
        self.clstack.append(4)

    def iconst_5(self):
        self.clstack.append(5)

    def arraylength(self):
        d = self.clstack.pop()
        # #print("array",d)
        s = len(d)
        self.clstack.append(s)

    def aaload(self):
        d = self.clstack.pop()
        d2 = self.clstack.pop()
        s = d2[d]
        self.clstack.append(s)

    def iinc(self, data):
        s = self.getint1(int(data[1][1]))
        self.LocalVariableTable[int(data[1][0])]['data'] += s

    def goto(self, data):
        s = self.getint(int(data[1].hex(), base=16))
        return s

    def run(self):
        if self.off == 0:
            return
        start = 0
        while 1:
            #print("指令：", start, self.Code[start])
            if self.Code[start][0] == 2:
                self.iconst_m1()
                start += 1
            elif self.Code[start][0] == 3:
                self.iconst_0()
                start += 1
            elif self.Code[start][0] == 4:
                self.iconst_1()
                start += 1
            elif self.Code[start][0] == 5:
                self.iconst_2()
                start += 1
            elif self.Code[start][0] == 6:
                self.iconst_3()
                start += 1
            elif self.Code[start][0] == 7:
                self.iconst_4()
                start += 1
            elif self.Code[start][0] == 8:
                self.iconst_5()
                start += 1
            elif self.Code[start][0] == 17:
                self.sipush(self.Code[start])
                start += 3
            elif self.Code[start][0] == 29:
                self.iload_3()
                start += 1
            elif self.Code[start][0] == 28:
                self.iload_2()
                start += 1
            elif self.Code[start][0] == 27:
                self.iload_1()
                start += 1
            elif self.Code[start][0] == 25:
                self.aload(self.Code[start])
                start += 2
            elif self.Code[start][0] == 26:
                self.iload_0()
                start += 1
            elif self.Code[start][0] == 42:
                self.aload_0()
                start += 1
            elif self.Code[start][0] == 43:
                self.aload_1()
                start += 1
            elif self.Code[start][0] == 44:
                self.aload_2()
                start += 1
            elif self.Code[start][0] == 45:
                self.aload_3()
                start += 1
            elif self.Code[start][0] == 87:
                self.pop()
                start += 1
            elif self.Code[start][0] == 89:
                self.dup()
                start += 1
            elif self.Code[start][0] == 90:
                self.dup_x1()
                start += 1
            elif self.Code[start][0] == 132:
                self.iinc(self.Code[start])
                start += 3
            elif self.Code[start][0] == 180:
                self.getfield(self.Code[start])
                start += 3
            elif self.Code[start][0] == 181:
                self.putfield(self.Code[start])
                start += 3
            elif self.Code[start][0] == 182:
                self.invokevirtual(self.Code[start])
                start += 3
            elif self.Code[start][0] == 183:
                self.invokespecial(self.Code[start])
                start += 3
            elif self.Code[start][0] == 184:
                self.invokestatic(self.Code[start])
                start += 3
            elif self.Code[start][0] == 186:
                self.invokedynamic(self.Code[start])
                start += 5
            elif self.Code[start][0] == 187:
                self.new(self.Code[start])
                start += 3
            elif self.Code[start][0] == 190:
                self.arraylength()
                start += 1
            elif self.Code[start][0] == 176:
                self.areturn()
                start += 1
                break
            elif self.Code[start][0] == 177:
                self.Jreturn()
                start += 1
                break
            elif self.Code[start][0] == 172:
                self.ireturn()
                start += 1
                break
            elif self.Code[start][0] == 167:
                goto_number = self.goto(self.Code[start])
                start += goto_number
            elif self.Code[start][0] == 166:
                if_acmpne_number = self.if_acmpne(self.Code[start])
                start += if_acmpne_number
            elif self.Code[start][0] == 165:
                if_acmpeq_number = self.if_acmpeq(self.Code[start])
                start += if_acmpeq_number
            elif self.Code[start][0] == 153:
                ifeq_number = self.ifeq(self.Code[start])
                start += ifeq_number
            elif self.Code[start][0] == 154:
                ifne_number = self.ifne(self.Code[start])
                start += ifne_number
            elif self.Code[start][0] == 155:
                iflt_number = self.iflt(self.Code[start])
                start += iflt_number
            elif self.Code[start][0] == 156:
                ifge_number = self.ifge(self.Code[start])
                start += ifge_number
            elif self.Code[start][0] == 157:
                ifgt_number = self.ifgt(self.Code[start])
                start += ifgt_number
            elif self.Code[start][0] == 158:
                ifle_number = self.ifle(self.Code[start])
                start += ifle_number
            elif self.Code[start][0] == 159:
                if_icmpeq_number = self.if_icmpeq(self.Code[start])
                start += if_icmpeq_number
            elif self.Code[start][0] == 160:
                if_icmpne_number = self.if_icmpne(self.Code[start])
                start += if_icmpne_number
            elif self.Code[start][0] == 161:
                if_icmplt_number = self.if_icmplt(self.Code[start])
                start += if_icmplt_number
            elif self.Code[start][0] == 162:
                if_icmpge_number = self.if_icmpge(self.Code[start])
                start += if_icmpge_number
            elif self.Code[start][0] == 163:
                if_icmpgt_number = self.if_icmpgt(self.Code[start])
                start += if_icmpgt_number
            elif self.Code[start][0] == 164:
                if_icmple_number = self.if_icmple(self.Code[start])
                start += if_icmple_number
            elif self.Code[start][0] == 18:
                self.ldc(self.Code[start])
                start += 2
            elif self.Code[start][0] == 78:
                self.astore_3()
                start += 1
            elif self.Code[start][0] == 76:
                self.astore_1()
                start += 1
            elif self.Code[start][0] == 75:
                self.astore_0()
                start += 1
            elif self.Code[start][0] == 77:
                self.astore_2()
                start += 1
            elif self.Code[start][0] == 16:
                self.bipush(self.Code[start])
                start += 2
            elif self.Code[start][0] == 59:
                self.istore_0()
                start += 1
            elif self.Code[start][0] == 60:
                self.istore_1()
                start += 1
            elif self.Code[start][0] == 61:
                self.istore_2()
                start += 1
            elif self.Code[start][0] == 62:
                self.istore_3()
                start += 1
            elif self.Code[start][0] == 50:
                self.aaload()
                start += 1
            elif self.Code[start][0] == 54:
                self.istore(self.Code[start])
                start += 2
            elif self.Code[start][0] == 58:
                self.astore(self.Code[start])
                start += 2
            elif self.Code[start][0] == 21:
                self.iload(self.Code[start])
                start += 2
            elif self.Code[start][0] == 96:
                self.iadd()
                start += 1
            elif self.Code[start][0] == 100:
                self.isub()
                start += 1
            elif self.Code[start][0] == 104:
                self.imul()
                start += 1
            elif self.Code[start][0] == 108:
                self.idiv()
                start += 1
            else:
                #print("指令没有执行", start,self.Code)
                break





class JVM:
    def __init__(self, filePath, st=0):
        self.jvmparse = jvmParse(filePath)
        self.jvmparse.startFun()
        self.st = st
        self.fileName = None

        # 全局
        self.globalThis = {}
        for _ in self.jvmparse.fieldInfo.fieldInfoPrase:
            key = _['nameIndex']['yhhData']['data'].decode()
            # #print(key)
            self.globalThis[key] = None

        # 方法栈
        self.createfunstack = {}


    def firstCall(self):
        d = []
        for _ in self.jvmparse.attributeList:
            if _['attributeNameIndex']['yhhData']['data'] == b'BootstrapMethods':
                d = _['bootstrapMethod']

        for key, value in self.createfunstack.items():
            if key.split('.')[0] == self.fileName+"-<init>":
                clstack = value['clstack'].copy()
                LocalVariableTable = value['LocalVariableTable'].copy()
                LocalVariableTable[0]['data'] = value
                s = runSme(value,clstack, LocalVariableTable,self.createfunstack,self.jvmparse.constantpool,[],d, self.globalThis)
                s.run()
        for key, value in self.createfunstack.items():
            if key.split('.')[0] == self.fileName+"-main":
                clstack = value['clstack'].copy()
                LocalVariableTable = value['LocalVariableTable'].copy()
                clstack.append("cbb")
                s = runSme(value,clstack, LocalVariableTable, self.createfunstack, self.jvmparse.constantpool,[], d, self.globalThis)
                s.run()

    def callFun(self, funName, supperstack, data):
        d = []
        for _ in self.jvmparse.attributeList:
            if _['attributeNameIndex']['yhhData']['data'] == b'BootstrapMethods':
                d = _['bootstrapMethod']
        # #print(self.createfunstack)

        for key, value in self.createfunstack.items():
            if key == funName:
                # #print("key", key)
                clstack = value['clstack'].copy()

                # #print("is come",key)
                LocalVariableTable = value['LocalVariableTable'].copy()
                LocalVariableTable[0]['data'] = value
                clstack += data
                # for index, i in enumerate(data):
                #     LocalVariableTable[index+1]['data'] = i
                # #print("clsk", clstack)
                s = runSme(value,clstack, LocalVariableTable, self.createfunstack, self.jvmparse.constantpool,supperstack, d, self.globalThis, 1)
                s.run()
                return
        #print("没有找到函数：", funName)

    def callFunstat(self, funName, supperstack, data):
        d = []
        for _ in self.jvmparse.attributeList:
            if _['attributeNameIndex']['yhhData']['data'] == b'BootstrapMethods':
                d = _['bootstrapMethod']
        # #print(self.createfunstack)

        for key, value in self.createfunstack.items():
            if key == funName:
                # #print("key", key)
                clstack = value['clstack'].copy()
                if key.split('.')[0] == self.fileName + "-<init>":
                    # #print("is come",key)
                    LocalVariableTable = value['LocalVariableTable'].copy()
                    LocalVariableTable[0]['data'] = value
                else:
                    LocalVariableTable = value['LocalVariableTable'].copy()
                clstack += data
                s = runSme(value,clstack, LocalVariableTable, self.createfunstack, self.jvmparse.constantpool,supperstack, d,self.globalThis)
                s.run()
                return
        #print("没有找到函数：", funName)

    def createFunStack(self):
        for i in self.jvmparse.methodsinfo.methodInfotable:
            # #print("ca", i)
            # 解析参数
            argsre = parseArgsF(i['descriptorIndex']['yhhData']['data'].decode())
            argsre.parseFun()
            i["clstack"] = []
            i['LocalVariableTable'] = {}
            # 解析CODE
            for i2 in i['attributeList']:
                if i2['attributeNameIndex']['yhhData']['data'] == b"Code":
                    i2['codeList'] = self.parseCode(i2)
                    for i3 in i2['attributeList']:
                        if i3['attributeNameIndex']['yhhData']['data'] == b'LocalVariableTable':

                            for index ,i4 in enumerate(i3['attributeList']):
                                i['LocalVariableTable'][index] = {"name":i4['nameIndex']['yhhData']['data'].decode(), 'data':None}




            name = self.fileName+'-'+i['nameIndex']['yhhData']['data'].decode()+'.'+i['descriptorIndex']['yhhData']['data'].decode()
            i['argsre'] = argsre
            self.createfunstack[name] = i

    def getfileInfo(self):


        for i in self.jvmparse.attributeList:
            if i['attributeNameIndex']['yhhData']['data'] == b'SourceFile' and self.st == 0 or self.st == 2:
                self.fileName = i['sourcefileIndex']['yhhData']['data'].decode().split('.')[0]
                break
            elif i['attributeNameIndex']['yhhData']['data'] == b'InnerClasses' and self.st == 1:
                pass


    def parseCode(self,code):
        s = parseClass(code['code'])
        s.parseFun()
        return s

    def start(self, fileName=None):
        if fileName == None:
            self.getfileInfo()
        else:
            self.fileName = fileName
        self.createFunStack()
        if self.st == 0:
            self.firstCall()

if __name__ == '__main__':
    s = JVM("./test/main.class")
    s.start()
