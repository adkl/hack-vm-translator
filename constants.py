from enumerations import ArithmeticInstruction, MemoryInstruction

arithmetic_instructions = [
    'add',
    'sub',
    'neg',
    'eq',
    'gt',
    'lt',
    'and',
    'or',
    'not'
]

data_segments = [
    'this',
    'that',
    'constant',
    'local',
    'argument',
    'temp',
    'static',
    'pointer'
]

equivalent_data_segments = [
    'this', 'that', 'argument', 'local'
]

segment_base_addr = {
    'this': 'THIS',
    'that': 'THAT',
    'argument': 'ARG',
    'local': 'LCL',
    'temp': 5,
    'static': 16
}

re_group_separator = '|'

ArithmeticInstructionMapping = {
    arithmetic_instructions[enum_item.value-1]: enum_item for enum_item in ArithmeticInstruction
}

MemoryInstructionMapping = {
    'push': MemoryInstruction.push,
    'pop': MemoryInstruction.pop
}

pseudo_assembly = {
    'D=*SP': '''
        @SP
        A=M
        D=M
    ''',
    '*SP=D': '''
        @SP
        A=M
        M=D
    ''',
    'D=*(SP-1)': '''
        @SP
        A=M-1
        D=M
    ''',
    'SP=A': '''
        D=A
        @SP
        M=D
    ''',
    'SP=A+1': '''
        D=A+1
        @SP
        M=D
    '''
}
