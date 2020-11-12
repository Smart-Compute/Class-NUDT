# load R1 100

from ISA import *

def load_direct(code_split):
    r = int(code_split[1][1])
    v = int(code_split[2])
    b = [0x00, r, v>>8, v&0xFF]
    return b

# load R1 R2
def load_reg(code_split):
    r1 = int(code_split[1][1])
    r2 = int(code_split[2][1])
    # v = int(code_split[2])
    b = [0x01, r1, 0, r2]
    return b

# load R1 $100
def load_mem(code_split):
    r = int(code_split[1][1])
    v = int(code_split[2][1:])
    b = [0x02, r, v>>8, v&0xFF]
    return b
# Halt
def halt(code_split):
    b = [0xFE, 0xFF, 0xFE, 0xFF]
    return b

#Store R1 $0
def store(code_split):
    r = int(code_split[1][1])
    v = int(code_split[2][1:])
    b = [0x10, r, v>>8, v&0xFF]
    return b

# Add R1 50
def add_val(code_split):
    r = int(code_split[1][1])
    v = int(code_split[2])
    b = [0x40, r, v>>8, v&0xFF]
    return b

# Add R1 R2
def add_reg(code_split):
    r1 = int(code_split[1][1])
    r2 = int(code_split[2][1])
    b = [0x42, r1, 0, r2]
    return b

# Sub R1 50
def sub_val(code_split):
    r = int(code_split[1][1])
    v = int(code_split[2])
    b = [0x41, r, v>>8, v&0xFF]
    return b

# Sub R1 R2
def sub_reg(code_split):
    r1 = int(code_split[1][1])
    r2 = int(code_split[2][1])
    b = [0x43, r1, 0, r2]
    return b

# Cmp R1 100
def cmp_val(code_split):
    r = int(code_split[1][1])
    v = int(code_split[2])
    b = [0x20, r, v>>8, v&0xFF]
    return b

# Sub R1 R2
def cmp_reg(code_split):
    r1 = int(code_split[1][1])
    r2 = int(code_split[2][1])
    b = [0x21, r1, 0, r2]
    return b

# .label 1
def label(code_split):
    pass

# BEQ loop
def beq(code_split, addr):
    b = [0x30, 0x00, addr>>8, addr&0xFF]
    return b

# BNE loop
def bne(code_split, addr):
    b = [0x31, 0x00, addr>>8, addr&0xFF]
    return b
