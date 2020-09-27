from constants import pseudo_assembly as a, segment_base_addr, equivalent_data_segments


class Encoder:
    EQ_COUNTER = 0
    GT_COUNTER = 0
    LT_COUNTER = 0
    PT_COUNTER = 0

    @classmethod
    def _encode_add(cls):
        return f'''
            // add
            {a['D=*(SP-1)']}
            A=A-1
            M=M+D
            {a['SP=A+1']}
        '''

    @classmethod
    def _encode_sub(cls):
        return f'''
            // sub
            {a['D=*(SP-1)']}
            A=A-1
            M=M-D
            {a['SP=A+1']}
        '''

    @classmethod
    def _encode_neg(cls):
        return '''
            // neg
            @SP
            A=M-1
            M=-M
        '''

    @classmethod
    def _encode_eq(cls):
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
    def _encode_gt(cls):
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
    def _encode_lt(cls):
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
    def _encode_and(cls):
        return f'''
            // and
            {a['D=*(SP-1)']}
            A=A-1
            M=M&D
            {a['SP=A+1']}
        '''

    @classmethod
    def _encode_or(cls):
        return f'''
            // or
            {a['D=*(SP-1)']}
            A=A-1
            M=M|D
            {a['SP=A+1']}
        '''

    @classmethod
    def _encode_not(cls):
        return '''
            // not
            @SP
            A=M-1
            M=!M
        '''

    @classmethod
    def _encode_push(cls, segment, i):
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

        if segment in ['temp', 'static']:
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
    def _encode_pop(cls, segment, i):
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

        if segment in ['temp', 'static']:
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
