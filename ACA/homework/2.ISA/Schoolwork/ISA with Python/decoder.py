def do_load_direct(ir, mem, regs, flag, pc):
    print("do_load_direct")
    regs[ir[1]][2] = ir[2]
    regs[ir[1]][3] = ir[3]
    print("regs_", ir[1], end=' ')
    for i in range(4):
        print(hex(regs[ir[1]][i]), end=' ')
    print()
    return flag, pc

def do_load_reg(ir, mem, regs, flag, pc):
    print("do_load_reg")
    for i in range(4):
        regs[ir[1]][i] = regs[ir[3]][i]
    # regs[ir[1]] = regs[ir[3]] # bug
    print("regs_", ir[1], end=' ')
    for i in range(4):
        print(hex(regs[ir[1]][i]), end=' ')
    print()
    return flag, pc

def do_load_mem(ir, mem, regs, flag, pc):
    print("do_load_mem")
    point = ir[2]<<8 | ir[3]
    print("mem start", point)
    regs[ir[1]][2:] = mem[point*2 : point*2+2]
    print("regs_", ir[1], end=' ')
    for i in range(4):
        print(hex(regs[ir[1]][i]), end=' ')
    print()
    return flag, pc

def do_halt():
    print("Halt")

def do_store(ir, mem, regs, flag, pc):
    print("do_store")
    point = ir[2]<<8 | ir[3]
    print("mem start", point)
    mem[point*2 : point*2+2] = regs[ir[1]][2:]
    print("mem", point*2, hex(mem[point*2]), hex(mem[point*2+1]))
    return flag, pc

def do_add_val(ir, mem, regs, flag, pc):
    print("do_add_val")
    val_reg = regs[ir[1]][2]<<8 | regs[ir[1]][3]
    val_ir = ir[2]<<8 | ir[3]
    val_res = val_reg + val_ir
    print(val_reg, "=", val_ir, "+", val_res)
    regs[ir[1]][2] = min(val_res>>8, 0xFF)
    regs[ir[1]][3] = val_res&0xFF
    print("regs_", ir[1], end=' ')
    for i in range(4):
        print(hex(regs[ir[1]][i]), end=' ')
    print()
    return flag, pc

def do_add_reg(ir, mem, regs, flag, pc):
    print("do_add_reg")
    val_reg1 = regs[ir[1]][2]<<8 | regs[ir[1]][3]
    val_reg2 = regs[ir[3]][2]<<8 | regs[ir[3]][3]
    val_res = val_reg1 + val_reg2
    print(val_reg1, "+", val_reg2, "=", val_res)
    regs[ir[1]][2] = min(val_res>>8, 0xFF)
    regs[ir[1]][3] = val_res&0xFF

    print("regs_", ir[1], end=' ')
    for i in range(4):
        print(hex(regs[ir[1]][i]), end=' ')
    print()

    return flag, pc


def do_sub_val(ir, mem, regs, flag, pc):
    print("do_sub_val")
    val_reg = regs[ir[1]][2]<<8 | regs[ir[1]][3]
    val_ir = ir[2]<<8 | ir[3]
    val_res = val_reg - val_ir
    print(val_reg, "-", val_ir, "=", val_res)
    regs[ir[1]][2] = min(val_res>>8, 0xFF)
    regs[ir[1]][3] = val_res&0xFF
    print("regs_", ir[1], end=' ')
    for i in range(4):
        print(hex(regs[ir[1]][i]), end=' ')
    print()
    return flag, pc

def do_sub_reg(ir, mem, regs, flag, pc):
    print("do_sub_reg")
    val_reg1 = regs[ir[1]][2]<<8 | regs[ir[1]][3]
    val_reg2 = regs[ir[3]][2]<<8 | regs[ir[3]][3]
    val_res = val_reg1 - val_reg2
    print(val_reg1, "-", val_reg2, "=", val_res)
    regs[ir[1]][2] = min(val_res>>8, 0xFF)
    regs[ir[1]][3] = val_res&0xFF
    print("regs_", ir[1], end=' ')
    for i in range(4):
        print(hex(regs[ir[1]][i]), end=' ')
    print()
    return flag, pc

def do_cmp_val(ir, mem, regs, flag, pc):
    print("do_cmp_val")
    val_reg = regs[ir[1]][2]<<8 | regs[ir[1]][3]
    val_ir = ir[2]<<8 | ir[3]
    if val_reg > val_ir:
        flag = 0
    elif val_reg == val_ir:
        flag = 1
    else:
        flag = 2
    print("flag", flag)
    return flag, pc

def do_cmp_reg(ir, mem, regs, flag, pc):
    print("do_cmp_reg")
    val_reg1 = regs[ir[1]][2]<<8 | regs[ir[1]][3]
    val_reg2 = regs[ir[3]][2]<<8 | regs[ir[3]][3]
    if val_reg1 > val_reg2:
        flag = 0
    elif val_reg1 == val_reg2:
        flag = 1
    else:
        flag = 2
    print("flag", flag)
    return flag, pc

def do_beq(ir, mem, regs, flag, pc):
    print("do_beq")
    if flag == 1:
        pc = ir[2]<<8 | ir[3]
        print("pc reload to", pc)
    return flag, pc

def do_bne(ir, mem, regs, flag, pc):
    print("do_bne")
    if flag != 1:
        pc = ir[2]<<8 | ir[3]
        print("ops, ***, pc reload to", pc)
    else:
        print("there are equal, skip the loop")
    return flag, pc
