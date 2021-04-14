import copy

instructions = [
    ['LD', 'F6', '34', 'R2'],
    ['LD', 'F2', '45', 'R3'],
    ['MULTD', 'F0', 'F2', 'F4'],
    ['SUBD', 'F8', 'F6', 'F2'],
    ['DIVD', 'F10', 'F0', 'F6'],
    ['ADDD', 'F6', 'F8', 'F2'],
]

class Scoreboard:
    def __init__(self, instructions):
        n = len(instructions)
        self.instructions = instructions
        self.IStatus = {stage: [None] * n for stage in ['IS', 'RO', 'EC', 'WR']}
        # print("%s", "%d", self.IStatus)
        # exit()
        self.FUStatus = {name: {head: None for head in ['Busy', 'Op', 'Fi', 'Fj', 'Fk', 'Qj', 'Qk', 'Rj', 'Rk', 'Time', 'FullTime']} for name in ['Integer', 'Mult1', 'Mult2', 'Add', 'Divide']}
        for k, v in self.FUStatus.items():
            v['Busy'] = False
            if k == 'Integer':
                v['FullTime'] = 1
            elif k.startswith('Mult'):
                v['FullTime'] = 10
            elif k == 'Add':
                v['FullTime'] = 2
            elif k == 'Divide':
                v['FullTime'] = 40
        self.RRStatus = {reg: None for reg in ['F0', 'F2', 'F4', 'F6', 'F8', 'F10']}
        self.Register = {reg: 0 for reg in ['F0', 'F2', 'F4', 'F6', 'F8', 'F10']}
        self.Register['R2'] = 10
        self.Register['R3'] = 20
        self.pc = 0


    def step_issue(self, new_IStatus, new_FUStatus, new_RRStatus, cycle):
        if self.pc == len(instructions):
            return
        next_inst = self.instructions[self.pc]   #载入下一个指令
        Op, dest, s1, s2 = next_inst
        # check fu busy
        if Op == 'LD':
            if not self.FUStatus['Integer']['Busy']: FU = 'Integer'
            else: return
        elif Op == 'MULTD':
            if not self.FUStatus['Mult1']['Busy']: FU = 'Mult1'
            elif not self.FUStatus['Mult2']['Busy']: FU = 'Mult2'
            else: return
        elif Op == 'SUBD' or Op == 'ADDD':
            if not self.FUStatus['Add']['Busy']: FU = 'Add'
            else: return
        elif Op == 'DIVD':
            if not self.FUStatus['Divide']['Busy']: FU = 'Divide'
            else: return 
        # check waw
        for _, v in self.FUStatus.items():
            if dest == v['Fi']:
               return  #如果下一条指令对应的目的寄存器和当前输入的指令所对应的目的寄存器一致，那么需要防止WAW这种冒险，如果条件成立语句返回，不执行下面环节（“该指令被暂停”）
        next_inst.append(FU) #如果不存在WAW冒险则将FU加到next_inst数组后，表示该des寄存器所对应的结果状态为FU
        # IStatus
        new_IStatus['IS'][self.pc] = cycle #此时记录IS对应于self.pc的时刻
        # FUStatus
        new_FUStatus[FU]['Busy'] = True #那么此时更新指令集对应FU状态为“占用”
        new_FUStatus[FU]['Op'] = Op  #此时更新Op状态为当前进行的运算类型
        new_FUStatus[FU]['Fi'] = dest #将对应FU的目的寄存器更新
        new_FUStatus[FU]['Fj'] = s1 #将对应FU中的操作数1对应寄存器指定为s1
        new_FUStatus[FU]['Fk'] = s2  #将对应FU中的操作数2对应寄存器指定为s2
        new_FUStatus[FU]['Qj'] = self.RRStatus[s1] if s1 in self.RRStatus.keys() else None #检查是否正在进行的指令中，有无将本指令所需源寄存器作为目的寄存器的，有的话就将该s1对应的状态返给Qj（此时对应的就是RAW冒险的抑制），无的话就返回None给Qj，表示该操作数可以被读取。
        new_FUStatus[FU]['Qk'] = self.RRStatus[s2] if s2 in self.RRStatus.keys() else None
        new_FUStatus[FU]['Rj'] = self.RRStatus[s1] is None if s1 in self.RRStatus.keys() else True # 如果S1不在RR状态中，那么此时源寄存器就是yes状态，如果存在的话，将源寄存器状态赋值为“self.RRStatus[s1] is None”
        new_FUStatus[FU]['Rk'] = self.RRStatus[s2] is None if s2 in self.RRStatus.keys() else True
        # RRStatus
        new_RRStatus[dest] = FU  #此时将该指对应的目标寄存器的状态改为当前发射的FU
        # increase pc
        self.pc += 1  #程序计数+1



    def step_read_operands(self, new_IStatus, new_FUStatus, new_RRStatus, cycle):
        # for all insts blocked in issue
        for i, v in enumerate(self.IStatus['IS']): #遍历IStatus['IS']行的数据
            if v is None or self.IStatus['RO'][i] is not None:
                continue #如果IS状态都是None或者存在不为None的数据载入，那么不执行后续语句
            FU = self.instructions[i][4] #在发射阶段self.instruction后加了一项FU
            if self.FUStatus[FU]['Rj'] and self.FUStatus[FU]['Rk']: #如果 功能单元中对应的Rj和Rk的状态都为true，记录下此时的时钟数，并且更新接下来进入Exec阶段前所需要的延时
                # IStatus
                new_IStatus['RO'][i] = cycle
                # FUStatus
                new_FUStatus[FU]['Time'] = self.FUStatus[FU]['FullTime']

                # simulate calculation
                status = self.FUStatus[FU] #将当前进行中的指令状态赋给status，以下进行指令的判断进而调取self.Register中的数据进行运算
                if status['Op'] == 'LD': 
                    result = self.Register[status['Fk']] + float(status['Fj'])
                elif status['Op'] == 'MULTD': 
                    result = self.Register[status['Fj']] * self.Register[status['Fk']]
                elif status['Op'] == 'SUBD':
                    result = self.Register[status['Fj']] - self.Register[status['Fk']]
                elif status['Op'] == 'DIVD':
                    result = self.Register[status['Fj']] / self.Register[status['Fk']]
                elif status['Op'] == 'ADDD':
                    result = self.Register[status['Fj']] + self.Register[status['Fk']]
                self.instructions[i].append(result)  #将得出的结果加到该指令所在数据行的后面

    def step_execusion_complete(self, new_IStatus, new_FUStatus, new_RRStatus, cycle):
        # for all insts blocked in readoperands
        for i, v in enumerate(self.IStatus['RO']): #遍历self.IStatus['RO']，如果发现其值都为None，或者是存在正在进行的执行阶段，那么不进行后续代码
            if v is None or self.IStatus['EC'][i] is not None: #该语句条件项可以通过我们需要的正向条件取反得到
                continue
            FU = self.instructions[i][4]
            if self.FUStatus[FU]['Rj']:
                new_FUStatus[FU]['Qj'] = None
                new_FUStatus[FU]['Rj'] = False
            if self.FUStatus[FU]['Rk']:
                new_FUStatus[FU]['Qk'] = None
                new_FUStatus[FU]['Rk'] = False
            new_FUStatus[FU]['Time'] = self.FUStatus[FU]['Time'] - 1 #到此时，对应FU的延迟时间减少1
            if self.FUStatus[FU]['Time'] == 1: # means new_FUStatus[FU]['Time'] == 0, but we can only touch table in the last cycle
                new_IStatus['EC'][i] = cycle  #此时进入到Exec环节，记录此时的时钟数

    def step_write_register(self, new_IStatus, new_FUStatus, new_RRStatus, cycle):
        # for all insts blocked in execusion_complete
        for i, v in enumerate(self.IStatus['EC']):  #遍历EC状态
            if v is None or self.IStatus['WR'][i] is not None:
                continue
            FU = self.instructions[i][4]
            status = self.FUStatus[FU]
            # check WAR
            WAR_harzard = False
            # for FU_, status_ in self.FUStatus.items():
            #此处是检查遍历中的已有源寄存器中（即前面记录的至少都是已经发射过的指令的源寄存器）有没有与当前执行指令的目的寄存器相同的，有的话就halt此WR过程
            for FU_, status_ in new_FUStatus.items(): 
                if status_['Fj'] == status['Fi'] and status_['Rj']:
                    WAR_harzard = True 
                    break
                if status_['Fk'] == status['Fi'] and status_['Rk']:
                    WAR_harzard = True
                    break
            if WAR_harzard:
                continue
            new_IStatus['WR'][i] = cycle #执行该WR过程记录下到此刻的时钟数
            new_RRStatus[status['Fi']] = None #指令不再占用该目的寄存器
            new_FUStatus[FU]['Busy'] = False #该FU不再被占用
            for key in ['Op', 'Fi', 'Fj', 'Fk', 'Qj', 'Qk', 'Rj', 'Rk']:
                new_FUStatus[FU][key] = None #而且该FU中其他的key所对应的value都赋为None（初始化了）
            for FU_, status_ in self.FUStatus.items(): #此时WAR已经结束；而对于整个FU表而言：如果存在Qj或者是Qk等于当前这个FU，那么需要进行限制的清空来允许其他指令的RO
                if status_['Qj'] == FU:
                    new_FUStatus[FU_]['Qj'] = None    #第一个操作数的读取不受限制
                    new_FUStatus[FU_]['Rj'] = True
                if status_['Qk'] == FU:
                    new_FUStatus[FU_]['Qk'] = None    #第二个操作数的读取不受限制
                    new_FUStatus[FU_]['Rk'] = True

            # simulate write register
            self.Register[status['Fi']] = self.instructions[i][5] #status['Fi']对应的是当前被占用的FU所对应的目标寄存器，此时对应的self.instructions的第六个元素为该FU计算出的结果

    def print_status(self): 
        print('Instruction Status')
        print('%10s'%'', end="")
        for v in self.instructions:
            print('%10s'%v[0], end="")
        print()
        for k, v in self.IStatus.items():
            print('%10s'%k, end="")
            for c in v:
                print('%10s'%(str(c) if c is not None else '_'), end="")
            print()
        print()


        print('Function Unit Status')
        for k in ['', 'Busy', 'Op', 'Fi', 'Fj', 'Fk', 'Qj', 'Qk', 'Rj', 'Rk', 'Time', 'FullTime']:
            print('%10s'%k, end="")
        print()
        for k, v in self.FUStatus.items():
            print('%10s'%k, end="")
            for _, v_ in v.items():
                print('%10s'%(v_ if v_ is not None else '_'), end="")
            print()
        print()

        print('Register Result Status')
        for k in ['F0', 'F2', 'F4', 'F6', 'F8', 'F10']:
            print('%10s'%k, end="")
        print()
        for k , v in self.RRStatus.items():
            print('%10s'%v, end="")
        print('\n'+'*'*120)

    def step(self):    
        cycle = 1
        while True:
            new_IStatus = copy.deepcopy(self.IStatus)
            new_FUStatus = copy.deepcopy(self.FUStatus)
            new_RRStatus = copy.deepcopy(self.RRStatus)
            self.step_issue(new_IStatus, new_FUStatus, new_RRStatus, cycle)
            self.step_read_operands(new_IStatus, new_FUStatus, new_RRStatus, cycle)
            self.step_execusion_complete(new_IStatus, new_FUStatus, new_RRStatus, cycle)
            self.step_write_register(new_IStatus, new_FUStatus, new_RRStatus, cycle)
            self.IStatus = new_IStatus
            self.FUStatus = new_FUStatus
            self.RRStatus = new_RRStatus
            print('Cycle %d:'%cycle)
            self.print_status()
            # input()
            cycle += 1
            if self.pc == len(self.instructions) and all(not v['Busy'] for k, v in self.FUStatus.items()):
                break

Scoreboard(instructions).step()
