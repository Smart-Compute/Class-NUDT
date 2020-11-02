from assember import *
from decoder import *
class MyComputer(object):
    def __init__(self):
        # 程序计数器，假设指令的地址101开始
        self.pc = 101
        # 指令寄存器
        self.ir = []
        # 32位寄存器
        # self.regs = [bytearray(4)]*8
        self.regs = [bytearray(4) for i in range(8)]
        self.flag = 0
        # store the addr of label
        self.label = {}

        self.mem = bytearray(2**16)
        self.mem[3] = 1
        self.mem[7] = 1
        self.mem[400] = 0xFF
        self.mem[401] = 0xFF
        self.mem[200] = 0xFF
        self.mem[201] = 0xFF

        # 将汇编指令从code.txt读入input
        self.input = []

    # 写内存
    def setMemData(self, addr, data):
        self.mem[addr] = data

    # write 4 byte to mem
    def write2mem(self, i, result_list):
        self.mem[i*4]=result_list[0]
        self.mem[i*4+1]=result_list[1]
        self.mem[i*4+2]=result_list[2]
        self.mem[i*4+3]=result_list[3]

    # 读内存
    def getMemData(self, addr):
        return self.mem[addr: addr+4]

    # 0. 准备阶段
    def read2Mem(self, filename):
        self.input = [s.rstrip('\n') for s in open(filename, 'r').readlines()]
        print(self.input)
        # Assember
        j = self.pc
        for i in range(self.pc, self.pc + len(self.input)):
            code = self.input[i-self.pc]
            code_split = code.split()
            print(code_split)
            if code_split[0]=="Load":
                if code_split[2][0] == '$':
                    result_list = load_mem(code_split)
                elif code_split[2][0] == 'R':
                    result_list = load_reg(code_split)
                else:
                    result_list = load_direct(code_split)

            elif code_split[0] == "Halt":
                result_list = halt(code_split)

            elif code_split[0] == "Store":
                result_list = store(code_split)
            elif code_split[0] == "Add":
                if code_split[2][0] == 'R':
                    result_list = add_reg(code_split)
                else:
                    result_list = add_val(code_split)

            elif code_split[0] == "Sub":
                if code_split[2][0] == 'R':
                    result_list = sub_reg(code_split)
                else:
                    result_list = sub_val(code_split)

            # https://blog.csdn.net/zhouqt/article/details/78172332
            elif code_split[0] == "Cmp":
                if code_split[2][0] == 'R':
                    result_list = cmp_reg(code_split)
                else:
                    result_list = cmp_val(code_split)
            elif code_split[0][0] == ".":
                self.label[code_split[0][1:]] = j
                print(self.label)
                j = j - 1
                continue

            elif code_split[0] == "BEQ":
                addr = self.label[code_split[1]]
                result_list = beq(code_split, addr)

            elif code_split[0] == "BNE":
                addr = self.label[code_split[1]]
                result_list = bne(code_split, addr)

            print(result_list)
            j = j + 1
            self.write2mem(j, result_list)

        # check memory
        # print(self.mem[self.pc*4 : self.pc*4+50])

    # 1. 取指阶段
    def fetch(self):
        self.ir = self.getMemData(self.pc*4)
        self.pc += 1

    # 2. 执行阶段
    def process(self):
        print("process")
        dic = {0x00:do_load_direct, 0x01:do_load_reg, 0x02:do_load_mem, 0xFE:do_halt, 0x10:do_store, 0x20:do_cmp_val, 0x21:do_cmp_reg, 0x30:do_beq, 0x31:do_bne, 0x40:do_add_val, 0x42:do_add_reg, 0x41:do_sub_val, 0x43:do_sub_reg}
        while True:
            self.fetch()
            num = self.ir[0]
            print("***************************")
            print("ir is:", end='')
            for i in range(4):
                print(hex(self.ir[i]), end=' ')
            if num == 0xFE:
                dic[num]()
                break

            self.flag, self.pc = dic[num](self.ir, self.mem, self.regs, self.flag, self.pc)
            # print("flag", self.flag)
            print(self.pc)
            # print(self.regs[1], self.regs[2])

if __name__ == "__main__":
    computer = MyComputer()
    # computer.read2Mem('高体/homework/2.ISA/code.txt')
    computer.read2Mem('code.txt')
    computer.process()
