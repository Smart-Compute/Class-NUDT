class MyComputer(object):
    def __init__(self):
        print("init CPU")
        # 程序计数器，假设指令的地址101开始
        self.pc = 101
        # 指令寄存器
        self.ir = []
        # 32位寄存器
        self.regs = [bytearray(4)]*32

        # 初始化内存，暂时用list模拟
        print('init memory')
        self.mem = bytearray(2**32)
        self.mem[3] = 1
        self.mem[7] = 1

        print('init IO')
        # 将汇编指令从code.txt读入input
        self.input = []

    # 写内存
    def setMemData(self, addr, data):
        self.mem[addr] = data

    # 读内存
    def getMemData(self, addr):
        return self.mem[addr: addr+4]

    # 0. 准备阶段
    def read2Mem(self, filename):
        self.input = [s.rstrip('\n') for s in open(filename, 'r').readlines()]
        print(self.input)
        # write the code from file to memory
        for i in range(self.pc, self.pc + len(self.input)):
            code = self.input[i-self.pc]
            # 1 1 0
            if code == 'Load r1, #0':
                self.setMemData(i*4, 1)
                self.setMemData(i*4+1, 1)
                self.setMemData(i*4+2, 0)
                self.setMemData(i*4+3, 0)
            # 1 2 1
            elif code == 'Load r2, #1':
                self.setMemData(i*4, 1)
                self.setMemData(i*4+1, 2)
                self.setMemData(i*4+2, 1)
                self.setMemData(i*4+3, 0)
            # 2 3 1 2
            elif code == 'Add r3, r1, r2':
                self.setMemData(i*4, 2)
                self.setMemData(i*4+1, 3)
                self.setMemData(i*4+2, 1)
                self.setMemData(i*4+3, 2)
            # 3 3 3
            elif code == 'Store r3, #3':
                self.setMemData(i*4, 3)
                self.setMemData(i*4+1, 3)
                self.setMemData(i*4+2, 3)
                self.setMemData(i*4+3, 0)

    # 1. 取指阶段
    def fetch(self):
        self.ir = self.getMemData(self.pc*4)
        self.pc += 1

    # 2. 执行阶段
    def process(self):
        # 根据ir执行不同的操作
        # print("process")
        self.fetch()
        # Load r2, #1 [1,2,1,0]
        if self.ir[0] == 1:
            self.regs[self.ir[1]] = self.getMemData(self.ir[2]*4)
            print("Load #", self.ir[2], "to r", self.ir[1])
            print("The regster is", self.regs[self.ir[1]])
        # Add r3, r1, r2 [2,3,1,2]
        elif self.ir[0] == 2:
            # 将四个字节转成10进制，相加
            self.regs[self.ir[1]] = int.from_bytes(self.regs[self.ir[2]], 'big') + \
                int.from_bytes(self.regs[self.ir[3]], 'big')
            print("Add r", self.ir[2], "and r", self.ir[3], ". The result is", self.regs[self.ir[1]])
            # 将十进制转换成十六进制
            self.regs[self.ir[1]] = bytearray.fromhex(str(hex(self.regs[self.ir[1]])).replace('0x','').zfill(8))
            print("The regster is", self.regs[self.ir[1]])
        # Store r3, #3 [3,3,3,0]
        elif self.ir[0] == 3:
            # self.mem[self.ir[2]*4+3] = self.regs[self.ir[1]]
            # print(self.mem[self.ir[2]*4+3])
            self.setMemData(self.ir[2]*4, self.regs[self.ir[1]][0])
            self.setMemData(self.ir[2]*4+1, self.regs[self.ir[1]][1])
            self.setMemData(self.ir[2]*4+2, self.regs[self.ir[1]][2])
            self.setMemData(self.ir[2]*4+3, self.regs[self.ir[1]][3])
            print("Store to #", self.ir[2], "and the result is ...")
            print("Memory status is", self.mem[0:16])

    def run(self):
        while True:
            self.process()
            # print(self.ir)
            if self.ir[0] > 3 or self.ir[0] == 0:
                break



if __name__ == "__main__":
    computer = MyComputer()
    # computer.read2Mem('高体/homework/code.txt')
    computer.read2Mem('code.txt')
    computer.run()


'''
The print result:
init CPU
init memory
init IO
['Load r1, #0', 'Load r2, #1', 'Add r3, r1, r2', 'Store r3, #3']
Load # 0 to r 1
The regster is bytearray(b'\x00\x00\x00\x01')
Load # 1 to r 2
The regster is bytearray(b'\x00\x00\x00\x01')
Add r 1 and r 2 . The result is 2
The regster is bytearray(b'\x00\x00\x00\x02')
Store to # 3 and the result is ...
Memory status is bytearray(b'\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x02')
'''
