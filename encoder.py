from constants import pseudo_assembly as a, segment_base_addr, equivalent_data_segments


class Encoder:
    EQ_COUNTER = 0
    GT_COUNTER = 0
    LT_COUNTER = 0
    PT_COUNTER = 0
    CALL_COUNTER = 0

    @classmethod
    def encode_add(cls):
        return f'''
            // add
            {a['D=*(SP-1)']}
            A=A-1
            M=M+D
            {a['SP=A+1']}
        '''

    @classmethod
    def encode_sub(cls):
        return f'''
            // sub
            {a['D=*(SP-1)']}
            A=A-1
            M=M-D
            {a['SP=A+1']}
        '''

    @classmethod
    def encode_neg(cls):
        return '''
            // neg
            @SP
            A=M-1
            M=-M
        '''

    @classmethod
    def encode_eq(cls):
        cls.EQ_COUNTER += 1

        return f'''
            // eq
            {a['D=*(SP-1)']}
            A=A-1
            D=M-D
            @TRUE_EQ{cls.EQ_COUNTER}
            D;JEQ
            D=0
            @END_EQ{cls.EQ_COUNTER}
            0;JMP
        (TRUE_EQ{cls.EQ_COUNTER})
            D=-1
        (END_EQ{cls.EQ_COUNTER})
            @SP
            A=M-1
            A=A-1
            M=D
            {a['SP=A+1']}
        '''

    @classmethod
    def encode_gt(cls):
        cls.GT_COUNTER += 1

        return f'''
            // gt
            {a['D=*(SP-1)']}
            A=A-1
            D=M-D
            @TRUE_GT{cls.GT_COUNTER}
            D;JGT
            D=0
            @END_GT{cls.GT_COUNTER}
            0;JMP
        (TRUE_GT{cls.GT_COUNTER})
            D=-1
        (END_GT{cls.GT_COUNTER})
            @SP
            A=M-1
            A=A-1
            M=D
            {a['SP=A+1']}
        '''

    @classmethod
    def encode_lt(cls):
        cls.LT_COUNTER += 1

        return f'''
            // lt
            {a['D=*(SP-1)']}
            A=A-1
            D=M-D
            @TRUE_LT{cls.LT_COUNTER}
            D;JLT
            D=0
            @END_LT{cls.LT_COUNTER}
            0;JMP
        (TRUE_LT{cls.LT_COUNTER})
            D=-1
        (END_LT{cls.LT_COUNTER})
            @SP
            A=M-1
            A=A-1
            M=D
            {a['SP=A+1']}
        '''

    @classmethod
    def encode_and(cls):
        return f'''
            // and
            {a['D=*(SP-1)']}
            A=A-1
            M=M&D
            {a['SP=A+1']}
        '''

    @classmethod
    def encode_or(cls):
        return f'''
            // or
            {a['D=*(SP-1)']}
            A=A-1
            M=M|D
            {a['SP=A+1']}
        '''

    @classmethod
    def encode_not(cls):
        return '''
            // not
            @SP
            A=M-1
            M=!M
        '''

    @classmethod
    def encode_push(cls, file_name, segment, i):
        if segment in equivalent_data_segments:
            return f'''
                // push {segment} {i}
                @{i}
                D=A
                @{segment_base_addr[segment]}
                A=D+M
                D=M
                {a['*SP=D']}
                {a['SP=A+1']}
            '''

        if segment == 'temp':
            return f'''
                // push {segment} {i}
                @{i}
                D=A
                @{segment_base_addr[segment]}
                A=D+A
                D=M
                {a['*SP=D']}
                {a['SP=A+1']}
            '''

        if segment == 'static':
            return f'''
                // push {segment} {i}
                @{file_name}.static.{i}
                D=M
                {a['*SP=D']}
                {a['SP=A+1']}
            '''

        if segment == 'constant':
            return f'''
                // push {segment} {i}
                @{i}
                D=A
                {a['*SP=D']}
                {a['SP=A+1']}
            '''

        if segment == 'pointer':
            cls.PT_COUNTER += 1
            return f'''
                // push {segment} {i}
                @{i}
                D=A
                @THAT_PT{cls.PT_COUNTER}
                D;JGT
                @THIS
                D=M
                @END_PT_{cls.PT_COUNTER}
                0;JMP
            (THAT_PT{cls.PT_COUNTER})
                @THAT
                D=M
            (END_PT_{cls.PT_COUNTER})
                {a['*SP=D']}
                {a['SP=A+1']}
            '''

    @classmethod
    def encode_pop(cls, file_name, segment, i):
        if segment in equivalent_data_segments:
            return f'''
                // pop {segment} {i}
                @{segment_base_addr[segment]}
                D=M     // D = 1000
                @{i}
                D=A+D   // D = 1003
                @SP
                A=M-1
                D=D+M   // D = 1503
                A=D-M   // A = 1003
                M=D-A   // *(seg+i) = 500
                @SP     // SP--
                M=M-1
            '''

        if segment == 'temp':
            return f'''
                // pop {segment} {i}
                @{segment_base_addr[segment]}
                D=A     // D = 5
                @{i}
                D=A+D   // D = 5+3 = 8
                @SP
                A=M-1
                D=D+M   // D = 508
                A=D-M   // A = 8
                M=D-A   // *(seg+i) = 500
                @SP     // SP--
                M=M-1
            '''

        if segment == 'static':
            return f'''
                // pop {segment} {i}
                {a['D=*(SP-1)']}
                @SP
                M=M-1
                @{file_name}.static.{i}
                M=D
            '''

        if segment == 'pointer':
            cls.PT_COUNTER += 1
            return f'''
                // pop {segment} {i}
                @{i}
                D=A
                @THAT_PT{cls.PT_COUNTER}
                D;JGT
                {a['D=*(SP-1)']}
                @THIS
                M=D
                @END_PT_{cls.PT_COUNTER}
                0;JMP
            (THAT_PT{cls.PT_COUNTER})
                {a['D=*(SP-1)']}
                @THAT
                M=D
            (END_PT_{cls.PT_COUNTER})
                @SP
                M=M-1
            '''

    @classmethod
    def encode_return(cls):
        return f'''
            // return
            @LCL
            D=M
            @endFrame
            M=D
            @5
            A=D-A
            D=M
            @retAddress
            M=D
            {a['D=*(SP-1)']}  // *ARG = *(SP-1)
            @ARG
            A=M
            M=D
            @ARG  // SP = ARG + 1
            D=M+1
            @SP
            M=D
            @endFrame
            M=M-1
            A=M
            D=M
            @THAT
            M=D
            @endFrame
            M=M-1
            A=M
            D=M
            @THIS
            M=D
            @endFrame
            M=M-1
            A=M
            D=M
            @ARG
            M=D
            @endFrame
            M=M-1
            A=M
            D=M
            @LCL
            M=D
            @retAddress
            A=M
            0;JMP
        '''

    @classmethod
    def encode_call(cls, function_name, n):
        cls.CALL_COUNTER += 1

        return f'''
            // call {function_name}
            @{function_name}.ret{cls.CALL_COUNTER}
            D=A
            {a['*SP=D']}
            {a['SP=A+1']}
            @LCL
            D=M
            {a['*SP=D']}
            {a['SP=A+1']}
            @ARG
            D=M
            {a['*SP=D']}
            {a['SP=A+1']}
            @THIS
            D=M
            {a['*SP=D']}
            {a['SP=A+1']}
            @THAT
            D=M
            {a['*SP=D']}
            {a['SP=A+1']}
            @5  // reposition ARG
            D=A
            @{n}
            D=D+A
            @SP
            D=M-D
            @ARG
            M=D
            @SP  // reposition LCL
            D=M
            @LCL
            M=D
            @{function_name}
            0;JMP
            ({function_name}.ret{cls.CALL_COUNTER})
        '''

    @classmethod
    def encode_function(cls, function_name, n):
        return f'''
        // function {function_name}
        ({function_name})
            @{n}
            D=A
            ({function_name}START_INIT_LOOP)
                @{function_name}END_INIT_LOOP
                D;JEQ  // if d == 0 -> exit loop
                @SP
                A=M
                M=0
                D=D-1
                @SP
                M=M+1
                @{function_name}START_INIT_LOOP
                0;JMP
            ({function_name}END_INIT_LOOP)
        '''

    @classmethod
    def encode_label(cls, file_name, label):
        return f'({file_name}.{label})'

    @classmethod
    def encode_goto(cls, file_name, label):
        return f'''
            // goto {label}
            @{file_name}.{label}
            0;JMP
        '''

    @classmethod
    def encode_ifgoto(cls, file_name, label):
        return f'''
            // if-goto {label}
            {a['D=*(SP-1)']}
            @SP
            M=M-1
            @{file_name}.{label}
            D;JNE
        '''

    @classmethod
    def bootstrap_code(cls):
        return f'''
            @256
            D=A
            @SP
            M=D
            {cls.encode_call('Sys.init', 0)}
        '''
