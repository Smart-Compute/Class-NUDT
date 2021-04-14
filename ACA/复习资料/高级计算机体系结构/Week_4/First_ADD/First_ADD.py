import sys
import ctypes

'''
这段小程序，是我写的第一段.py，值得纪念一下，说几句
越智能，越难控制
你会发现，你的恐惧几乎完全来源于你对事物信息的不完全了解
当我连一个变量需要占多大内存空间都不知道时，我感觉好像完全不对了

我的难点有两个：
1.没上过科大计算机的课，对题目的理解有疑虑。
    只有几个词，没有题干，让人感觉不太适应，是太开放了，还是。。。不怕甲方要求多，就怕甲方不知道要啥
    我当作是开放来做吧。我的理解是：
        用python模拟内存和寄存器（模型），以及load store add这些指令，
        之后做主函数，把那段加法操作的程序实现。
        注意：8-bit-cell  32bit-Add 会有大端小端的问题  Add会有S和U的区别  还会有地址越界的问题

2.我没用过python，我要找到和题目较为相近的数据类型，表达要模拟的内存和寄存器
    2.1. 我用bytearray模拟字节编址的Mem，用了list表征Reg，为了安全，list里的元素，用前用后，都用Modi_32u“洗洗手”
    2.2. 我把有无符号，做成了“设置”，而不是两种指令
    2.3. 大端小端的做了两个最“底层”的函数Set_MemVal，Get_MemVal实现
    2.4. 用了ctypes，把一直当作U存储的数据，根据不同U/S设置，完成显示前转换
    
有一些感触：
    虽然缩进这些比较严格，但是，总让人感觉python好松散啊，太随意，特别是全局变量相关以及变量类型随意变化，让我接受不了。
    python给出的迭代器、列表表达式这些，就是在说，你要把代码行数减低，让一行尽可能多的逻辑复杂。
    但我却认为应该尽可能的把每行做简单点，把行数做大。
    这种区别很像RISC和CISC
    一个变量所占用的空间，由python自动去维护，你能用的数据是无限长的（受限于内存）。人确实太懒了。
    
    S.F. 2019/10/13
'''


# 这个函数是为了校验整型数，让他不超过 32bit
# 没办法，python对数据类型内存的管理实在太智能，让我有点点没有安全感，这个&操作可认为是把32以上的高位清空，那就不会超过32bit了
def Modi_32u(Num_in):
    return Num_in & 0xFFFF_FFFF


# 这个函数测试下全局变量怎么使用
def Test_Global():
    global RegNum, MemSize
    return print(RegNum, MemSize)


# 这个函数，用来对某个内存单元按照不同的大端小端模式，设置数据，当然还要检查是否发生地址越界
def Set_MemVal(AddMem, Val):
    # 我吃不准，python传入参数是否会脏，所以还是用设置个局部变量
    l_Val = Modi_32u(Val)
    l_AddMem = Modi_32u(AddMem)

    global BigLitSet, MemArr, MemSize

    if l_AddMem > (MemSize - 4):
        print('发生了访问越界')
        sys.exit()

    if BigLitSet == 'B':
        MemArr[l_AddMem + 0] = (l_Val & 0xFF00_0000) >> 24
        MemArr[l_AddMem + 1] = (l_Val & 0x00FF_0000) >> 16
        MemArr[l_AddMem + 2] = (l_Val & 0x0000_FF00) >> 8
        MemArr[l_AddMem + 3] = (l_Val & 0x0000_00FF) >> 0
    elif BigLitSet == 'L':
        MemArr[l_AddMem + 3] = (l_Val & 0xFF00_0000) >> 24
        MemArr[l_AddMem + 2] = (l_Val & 0x00FF_0000) >> 16
        MemArr[l_AddMem + 1] = (l_Val & 0x0000_FF00) >> 8
        MemArr[l_AddMem + 0] = (l_Val & 0x0000_00FF) >> 0
    else:
        print('发生了没有设置正确大小端的错误')
        sys.exit()
    return


# 这个函数，用来按照不同的大端小端模式读取某个内存单元数据，读取数据，当然还要检查是否发生地址越界
def Get_MemVal(AddMem):
    # 我吃不准，python传入参数是否会脏，所以还是用设置个局部变量
    l_AddMem = Modi_32u(AddMem)
    l_Val = 0x0000_0000

    global BigLitSet, MemArr, MemSize

    if l_AddMem > (MemSize - 4):
        print('发生了访问越界')
        sys.exit()
    if BigLitSet == 'B':
        l_Val |= MemArr[l_AddMem + 0] << 24
        l_Val |= MemArr[l_AddMem + 1] << 16
        l_Val |= MemArr[l_AddMem + 2] << 8
        l_Val |= MemArr[l_AddMem + 3] << 0
    elif BigLitSet == 'L':
        l_Val |= MemArr[l_AddMem + 3] << 24
        l_Val |= MemArr[l_AddMem + 2] << 16
        l_Val |= MemArr[l_AddMem + 1] << 8
        l_Val |= MemArr[l_AddMem + 0] << 0
    else:
        print('发生了没有设置正确大小端的错误')
        sys.exit()
    return l_Val


def Load(RegN, AddMem):
    # 我吃不准，python传入参数是否会脏，所以还是用设置个局部变量
    l_RegN = Modi_32u(RegN)
    l_AddMem = Modi_32u(AddMem)
    global BigLitSet, MemArr, MemSize, RegNum, RegList
    if 0 <= l_RegN <= RegNum:
        RegList[l_RegN] = Get_MemVal(l_AddMem)
    else:
        print('寄存器地址越界')
    return


def Store(RegN, AddMem):
    # 我吃不准，python传入参数是否会脏，所以还是用设置个局部变量
    l_RegN = Modi_32u(RegN)
    l_AddMem = Modi_32u(AddMem)
    global BigLitSet, MemArr, MemSize, RegNum, RegList
    if 0 <= l_RegN <= RegNum:
        Set_MemVal(l_AddMem, RegList[l_RegN])
    else:
        print('寄存器地址越界')
    return


def Add(Reg_D, Reg_SA, Reg_SB):
    global RegNum, RegList, SignFlag
    if 0 <= Reg_D <= RegNum and 0 <= Reg_SA <= RegNum and 0 <= Reg_SB <= RegNum:
        if SignFlag == 'U':
            RegList[Reg_D] = Modi_32u(RegList[Reg_SA] + RegList[Reg_SB])
        elif SignFlag == 'S':
            RegList[Reg_D] = Modi_32u(ctypes.c_long(RegList[Reg_SA]).value
                                      + ctypes.c_long(RegList[Reg_SB]).value)
    else:
        print('寄存器地址越界')
    return


'''从这里开始进入主程序'''

# 开始，模拟并测试内存

MemSize = input('\n告诉我模拟多大尺寸的内存(KByte):')
# 校验输入是否有误
if MemSize == '':
    print('不输入就按回车，逗我的吗?')
    sys.exit()
if not MemSize.lstrip('-').isdigit():
    print('不能敲字母!敲数！')
    sys.exit()
MemSize = int(MemSize)
if MemSize <= 0:
    print('别逗我，不能小于1也不能是负的!')
    sys.exit()
elif MemSize > 10:
    print('亲，别太大，演示演示就是了!')
    sys.exit()

# 这种，一个变量名，一会是字符串，一会是整形的事情还是挺吓人的。
# KB->B，MemSize还有个功能，之后，用作内存访问边界检查
MemSize *= 1024
# 我挑了好久，才发现有bytearray这种数据类型，比较好操作，又是8bit字节的，就他吧。
MemArr = bytearray(MemSize)
print(MemArr)
print('上面打印的就是内存的内容')
print('用字节串数组bytearray去模拟Memory，为了响应题目8bit-Cell字节编址')

# 刚学python，为了试下循环，我做个内存测试小程序段，就当玩了,但是好像这种for不被python推荐
print('开始内存有效性测试!')
Flag_Test = False  # 出错标志变量
for i in range(0, MemSize):
    MemArr[i] = 0x00
    if MemArr[i] != 0x00:
        Flag_Test = True
        break
    MemArr[i] = 0xFF
    if MemArr[i] != 0xFF:
        Flag_Test = True
        break
if Flag_Test:
    print('hh,模拟的内存也会有坏的，你说咋办吧!')
    sys.exit()
print('通过内存测试！模拟%dByte的内存' % MemSize)
# 结束内存初始化，模拟、测试内存，MemArr[],MemSize待用


# 开始模拟寄存器Reg
RegNum = input('\n告诉我模拟多少个32bit的Reg(只接受4-128个,还要是2^n,不要乱写,谢谢):')
if RegNum == '':
    print('不输入就按回车,逗我的吗?')
    sys.exit()
if not RegNum.lstrip('-').isdigit():
    print('不能敲字母!敲数!')
    sys.exit()
RegNum = int(RegNum)  # 好惊险的操作啊，😨，人类是越来越懒了，都敢这么干了
if RegNum < 4 or RegNum > 128:
    print('亲,要么设置大了，要么设置小了.')
    sys.exit()
if not (RegNum in (2 ** x for x in range(2, 8))):  # 试一下测试功能，好像有点意思。这里面还有个短语，嘻嘻
    print('不是2^n,你懂的.')
    sys.exit()

# 我用什么模拟寄存器呢？list吧。因为，这个可能是python最重要的数据类型了吧。
RegList = []
for i in range(RegNum):
    RegList.append(0xFFFF_FFFF)  # 这种生成list估计效率是最低的？

RegList = [0xFFFF_FFFF for i in range(RegNum)]  # 这种用列表表达式的，貌似效率高？？

print('寄存器位宽:%d' % (sys.getsizeof(RegList[1])))
print('寄存器个数:%d' % (len(RegList)))
# 这里就不自检了
# 结束寄存器Reg初始化

# 设置大小端模式，这里既然已经，模拟了8bitcell的内存，那么就肯定有大小端模式的事情，所以，这里需要考虑设置
while True:
    BigLitSet = input('\n请输入大小端模式,B/L:')
    if (BigLitSet == 'B' or BigLitSet == 'b' or
            BigLitSet == 'L' or BigLitSet == 'l' or
            BigLitSet == ''):
        break
    else:
        print('输入有误，B/L或直接回车(L),不区分大小写')
if BigLitSet == '':  # 默认是小端
    BigLitSet = 'L'
BigLitSet = BigLitSet.upper()  # 都改成大写

# 设置有符号，还是无符号，其实我应该做两个指令，但是，题目没说，我就在这里，把有无符号，作为一个参数输入
while True:
    SignFlag = input('\n请输入ADD指令模拟有无符号,S/U:')
    if (SignFlag == 'S' or SignFlag == 's' or
            SignFlag == 'U' or SignFlag == 'u' or
            SignFlag == ''):
        break
    else:
        print('输入有误，S/U或直接回车(S),不区分大小写')
if SignFlag == '':  # 默认是小端
    SignFlag = 'S'
SignFlag = SignFlag.upper()  # 都改成大写

# 设置内存初值
while True:
    TempData = input('\n设置#0中数据:')
    if TempData.lstrip('-').isdigit():
        TempData = int(TempData)
        Set_MemVal(0 << 2, TempData)
        break
    else:
        print('输入有误,请输入数字')

while True:
    TempData = input('\n设置#1中数据:')
    if TempData.lstrip('-').isdigit():
        TempData = int(TempData)
        Set_MemVal(1 << 2, TempData)
        break
    else:
        print('输入有误,请输入数字')

# 好的，同志们这里开始模拟作业那几条语句

print('\n')
input('所有按任意键可以开始:')
print('Load r1,#0   把第一只大象搬进来')
Load(1, 0 << 2)
print('Load r2,#1   把第二只大象搬进来')
Load(2, 1 << 2)
print('Add r3,r1,r2 两只大象生了只小象放r3')
Add(3, 1, 2)
print('Store r3,#3  把小象送出去')
Store(3, 3 << 2)
print('看看小象长什么样：')
if SignFlag == 'U':
    print(ctypes.c_ulong(Get_MemVal(3 << 2)).value)
else:
    print(ctypes.c_long(Get_MemVal(3 << 2)).value)

'''

'''
