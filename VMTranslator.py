import sys

from encoder import Encoder
from enumerations import ArithmeticInstruction, MemoryInstruction
from parser import Parser


class VMTranslator:

    def __init__(self, vm_file_path: str):
        self.vm_file_path = vm_file_path

        self.asm_file_path = vm_file_path.replace(vm_file_path.split('.')[-1], 'asm')

    def run(self):
        vm_file = open(file=self.vm_file_path, mode='r')
        file_lines = vm_file.readlines()

        asm_file = open(self.asm_file_path, 'w')

        for line in file_lines:
            parser = Parser(line)

            print(parser.instruction_type, parser.segment, parser.i)

            asm_code = self._generate_asm_code(parser)

            if asm_code:
                asm_file.write(asm_code)

        vm_file.close()
        asm_file.close()

    def _generate_asm_code(self, parser: Parser):
        if parser.instruction_type == ArithmeticInstruction.add:
            return Encoder._encode_add()
        if parser.instruction_type == ArithmeticInstruction.sub:
            return Encoder._encode_sub()
        if parser.instruction_type == ArithmeticInstruction.eq:
            return Encoder._encode_eq()
        if parser.instruction_type == ArithmeticInstruction.and_:
            return Encoder._encode_and()
        if parser.instruction_type == ArithmeticInstruction.gt:
            return Encoder._encode_gt()
        if parser.instruction_type == ArithmeticInstruction.or_:
            return Encoder._encode_or()
        if parser.instruction_type == ArithmeticInstruction.lt:
            return Encoder._encode_lt()
        if parser.instruction_type == ArithmeticInstruction.not_:
            return Encoder._encode_not()
        if parser.instruction_type == ArithmeticInstruction.neg:
            return Encoder._encode_neg()

        if parser.instruction_type == MemoryInstruction.push:
            return Encoder._encode_push(parser.segment, parser.i)

        if parser.instruction_type == MemoryInstruction.pop:
            return Encoder._encode_pop(parser.segment, parser.i)


if __name__ == '__main__':
    VMTranslator(sys.argv[1]).run()
