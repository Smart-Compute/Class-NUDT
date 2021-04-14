import copy

instructionSet = [
    ['LD', 'F6', '34', 'R2'],
    ['LD', 'F2', '45', 'R3'],
    ['MULTD', 'F0', 'F2', 'F4'],
    ['SUBD', 'F8', 'F6', 'F2'],
    ['DIVD', 'F10', 'F0', 'F6'],
    ['ADDD', 'F6', 'F8', 'F2'],
]

class Scoreboard:
    def init(self, instructionSet):
        n=len(instructionSet)
        self.instructionSet = instructionSet
        self.instructionState = {state:[None]*n for state in ['IS','RO','EC','WR']}
        self.fuState = {State: {content:None for content in ['Busy','Op','Fi','Fj','Fk','Qj','Qk','Rj','Rk','Time','Latency'] for type in ['Integer','Mult1','Mult2','Add','Divide']}
            for k, v in self.fuState.items():
              v['Busy'] = False 
            if k == 'Integer':
               v['Latency'] = 1
            elif k == 'Add':
               v['Latency'] = 2
            elif k == 'Mult':
               v['Latency'] = 10
            elif k == 'Divide':
               v['Latency'] = 40

        self.rrState = {register: None for register in ['F0','F2','F4','F6','F8','F10']}
        self.Register['R2'] = 10
        self.Register['R3'] = 20
        self.Register = {reg: 0 for reg in 'F0','F2','F4','F6','F8','F10']}
        self.pc = 0

    def instruction_Issue(self,new_instructionState,new_rrState,cycle)
            instruction_element = {'Op', 'dest', 's1', 's2'}
        if self.pc == len(instructionSet):
            return
        next_instruction = self.instructionSet[self.pc]
        instruction_element = next_instruction
        #Check the structual hazards
        if instruction_element[0] == 'LD':
        if not self.fuState['Integer']['Busy']: FU = 'Integer'
            else: return
        if instruction_element[0] == 'SUBD' or  instruction_element[0] == 'ADDD':
            if not self.fuState['Add']['Busy']: FU = 'Add'
            else：return
        if instruction_element[0] == 'MULTD':
            if not self.fuState['Mult']['Busy']: FU = 'Mult'
            else: return
        if instruction_element[0] == 'DIVD'：
            if not self.fuState['Divide']['Busy']：FU = 'Divide'
            else: return
        #至此已经完成了该指令对于相应FU的占用
       
        #Check the WAW hazard
        for _, v in self.fuState.items():
        if instruction_element[1] == v['Fi']: # check if there is a reg occupation
               return 
        # new instruction
        next_instruction.append(FU)
        new_instructionState['IS'][self.pc] = cycle # record the 1st instruction time info 
        # instruction_element = {'Op', 'dest', 's1', 's2'}
        new_fuState[FU]['Busy'] = True
        new_fuState[FU]['Op'] = instruction_element[0]
        new_fuState[FU]['Fi'] = instruction_element[1]
        new_fuState[FU]['Fj'] = instruction_element[2]
        new_fuState[FU]['Fk'] = instruction_element[3]
        new_fuState[FU]['Qj'] = self.rrState[instruction_element[2]] if instruction_element[2] in self.rrState.keys() else None
        new_fuState[FU]['Qk'] = self.rrState[instruction_element[3]] if instruction_element[3] in self.rrState.keys() else None
        new_fuState[FU]['Rj'] = self.rrState[instruction_element[2]] is None if instruction_element[2] in self.rrState.keys() else True
        new_fuState[FU]['Rk'] = self.rrState[instruction_element[3]] is None if instruction_element[3] in self.rrState.keys() else True
        # new Register result state
        new_rrState.append(instruction_element[0]) = FU 
        self.pc += 1 

    def read_operands(self, new_instructionState, new_fuState, new_rrState, cycle)
        for i, v in enumerate(self.instructionState['IS']): #遍历指令状态['IS']行的数据
            if v is None or self.instructionState['RO'][i] is not None:
                continue #如果IS状态都是None或者存在不为None的数据载入，那么不执行后续语句
            FU = self.instructionSet[i][4] #在发射阶段self.instruction后加了一项FU
            if self.fuState[FU]['Rj'] and self.fuState[FU]['Rk']: #如果 功能单元中对应的Rj和Rk的状态都为true，记录下此时的时钟数，并且更新接下来进入Exec阶段前所需要的延时
                # Instruction state
                new_instructionState['RO'][i] = cycle
                # Fucntional unit state 
                new_fuState[FU]['Time'] = self.fuState[FU]['FullTime']
                # caculation
                state = self.fuState[FU] #将当前进行中的指令状态赋给status，以下进行指令的判断进而调取self.Register中的数据进行运算
                if state['Op'] == 'LD': 
                    result = self.Register[state['Fk']] + float(state['Fj'])
                elif state['Op'] == 'MULTD': 
                    result = self.Register[state['Fj']] * self.Register[state['Fk']]
                elif state['Op'] == 'SUBD':
                    result = self.Register[state['Fj']] - self.Register[state['Fk']]
                elif state['Op'] == 'DIVD':
                    result = self.Register[state['Fj']] / self.Register[state['Fk']]
                elif state['Op'] == 'ADDD':
                    result = self.Register[state['Fj']] + self.Register[state['Fk']]
                # new result of the instruction
                self.instructionState[i].append(result)  #将得出的结果加到该指令所在数据行的后面

    def execusion_complete(self, new_instructionState, new_fuState, new_rrState, cycle):
        # for all insts blocked in readoperands
        for i, v in enumerate(self.instructionState['RO']): #遍历self.IStatus['RO']，如果发现其值都为None，或者是存在正在进行的执行阶段，那么不进行后续代码
            if v is None or self.instructionState['EC'][i] is not None: #该语句条件项可以通过我们需要的正向条件取反得到
                continue
            FU = self.instructionsSet[i][4]
            if self.fuState[FU]['Rj']:
                new_fuState[FU]['Qj'] = None
                new_fuState[FU]['Rj'] = False
            if self.fuState[FU]['Rk']:
                new_fuState[FU]['Qk'] = None
                new_fuState[FU]['Rk'] = False
            new_fuState[FU]['Time'] = self.fuState[FU]['Time'] - 1 #到此时，对应FU的延迟时间减少1
            if self.fuState[FU]['Time'] == 1: # means new_FUStatus[FU]['Time'] == 0, but we can only touch table in the last cycle
                new_instructionState['EC'][i] = cycle  #此时进入到Exec环节，记录此时的时钟数

    def write_register(self, new_instructionState, new_fuState, new_rrState, cycle):
        # for all insts blocked in execusion_complete
        for i, v in enumerate(self.instructionState['EC']):  #遍历EC状态
            if v is None or self.instructionState['WR'][i] is not None:
                continue
            FU = self.instructionSet[i][4]
            state = self.fuState[FU]
            # check WAR
            WAR_harzard = False
            # for FU_, status_ in self.FUStatus.items():
            #此处是检查遍历中的已有源寄存器中（即前面记录的至少都是已经发射过的指令的源寄存器）有没有与当前执行指令的目的寄存器相同的，有的话就halt此WR过程
            for FU_temp , state_temp in new_FUStatus.items(): 
                if state_temp['Fj'] == state['Fi'] and state_temp['Rj']:
                    WAR_harzard = True 
                    break
                if state_temp['Fk'] == state['Fi'] and state_temp['Rk']:
                    WAR_harzard = True
                    break
            if WAR_harzard:
                continue
            new_instructionState['WR'][i] = cycle #执行该WR过程记录下到此刻的时钟数
            new_rrState[state['Fi']] = None #指令不再占用该目的寄存器
            new_fuState[FU]['Busy'] = False #该FU不再被占用
            for key in ['Op', 'Fi', 'Fj', 'Fk', 'Qj', 'Qk', 'Rj', 'Rk']:
                new_fuState[FU][key] = None #而且该FU中其他的key所对应的value都赋为None（初始化了）
            for FU_temp, state_temp in self.fuState.items(): #此时WAR已经结束；而对于整个FU表而言：如果存在Qj或者是Qk等于当前这个FU，那么需要进行限制的清空来允许其他指令的RO
                if state_temp['Qj'] == FU:
                    new_fuState[FU_temp]['Qj'] = None    #第一个操作数的读取不受限制
                    new_fuState[FU_temp]['Rj'] = True
                if state_temp['Qk'] == FU:
                    new_fuState[FU_]['Qk'] = None    #第二个操作数的读取不受限制
                    new_fuState[FU_]['Rk'] = True
            # write the register
            self.Register[state['Fi']] = self.instructions[i][5] #status['Fi']对应的是当前被占用的FU所对应的目标寄存器，此时对应的self.instructions的第六个元素为该FU计算出的结果
        
        # 三个状态表的打印
    def print_state(self):
        print('Instruction State')
        print('%10s'%'', end="")
        for v in self.instructionSet:
            print('%10s'%v[0], end="")
        print()
        for k, v in self.instructionState.items():
            print('%10s'%k, end="")
            for c in v:
                print('%10s'%(str(c) if c is not None else '_'), end="")
            print()
        print()


        print('Function Unit State')
        for k in ['', 'Busy', 'Op', 'Fi', 'Fj', 'Fk', 'Qj', 'Qk', 'Rj', 'Rk', 'Time', 'Latency']:
            print('%10s'%k, end="")
        print()
        for k, v in self.fuState.items():
            print('%10s'%k, end="")
            for _, v_ in v.items():
                print('%10s'%(v_ if v_ is not None else '_'), end="")
            print()
        print()

        print('Register Result State')
        for k in ['F0', 'F2', 'F4', 'F6', 'F8', 'F10']:
            print('%10s'%k, end="")
        print()
        for k , v in self.rrState.items():
            print('%10s'%v, end="")
        print('\n'+'*'*120)

    def step(self):
    cycle = 1
    while True:
        new_instructionState = copy.deepcopy(self.instructionState)
        new_fuState = copy.deepcopy(self.fuState)
        new_rrState= copy.deepcopy(self.rrState)
        self.instruction_Issue(new_IStatus, new_FUStatus, new_RRStatus, cycle)
        self.read_operands(new_IStatus, new_FUStatus, new_RRStatus, cycle)
        self.execusion_complete(new_IStatus, new_FUStatus, new_RRStatus, cycle)
        self.write_register(new_IStatus, new_FUStatus, new_RRStatus, cycle)
        self.instructionState = new_instructionState
        self.fuState = new_fuState
        self.rrState = new_rrState
        print('Cycle %d:'%cycle)
        self.print_state()
        # input()
        cycle += 1
        if self.pc == len(self.instructionSet) and all(not v['Busy'] for k, v in self.fuState.items()):
            break

Scoreboard(instructionSet).step()

 

 