import sys
from pathlib import Path

from encoder import Encoder
from enumerations import ArithmeticInstruction, MemoryInstruction, FunctionInstruction, BranchingInstruction
from parser import Parser


class VMTranslator:

    def __init__(self, vm_code_path: str):
        self.is_dir = False

        self.vm_files_paths = self._vm_file_paths(vm_code_path)
        self.asm_file_path = self._resolve_asm_file_path(vm_code_path)

    def _vm_file_paths(self, input_path: str):
        path = Path(input_path)

        if path.is_dir():
            self.is_dir = True
            return list(map(lambda e: str(e), filter(lambda e: e.suffix == '.vm', path.iterdir())))

        return [input_path]

    def _resolve_asm_file_path(self, input_path: str) -> str:
        path = Path(input_path)

        if path.is_dir():
            return str(path.joinpath(path.name).with_suffix('.asm'))

        return str(Path(input_path).with_suffix('.asm'))

    def run(self):
        asm_file = open(self.asm_file_path, 'w')

        if self.is_dir:
            asm_file.write(Encoder.bootstrap_code())

        for vm_file_path in self.vm_files_paths:
            vm_file = open(file=vm_file_path, mode='r')
            file_lines = vm_file.readlines()

            for line in file_lines:
                parser = Parser(line)

                asm_code = self._generate_asm_code(parser, Path(vm_file_path).name)

                if asm_code:
                    asm_file.write(asm_code)

            vm_file.close()
        asm_file.close()

    def _generate_asm_code(self, parser: Parser, file_name: str):
        if parser.instruction_type == ArithmeticInstruction.add:
            return Encoder.encode_add()
        if parser.instruction_type == ArithmeticInstruction.sub:
            return Encoder.encode_sub()
        if parser.instruction_type == ArithmeticInstruction.eq:
            return Encoder.encode_eq()
        if parser.instruction_type == ArithmeticInstruction.and_:
            return Encoder.encode_and()
        if parser.instruction_type == ArithmeticInstruction.gt:
            return Encoder.encode_gt()
        if parser.instruction_type == ArithmeticInstruction.or_:
            return Encoder.encode_or()
        if parser.instruction_type == ArithmeticInstruction.lt:
            return Encoder.encode_lt()
        if parser.instruction_type == ArithmeticInstruction.not_:
            return Encoder.encode_not()
        if parser.instruction_type == ArithmeticInstruction.neg:
            return Encoder.encode_neg()

        if parser.instruction_type == BranchingInstruction.goto:
            return Encoder.encode_goto(file_name, parser.label)
        if parser.instruction_type == BranchingInstruction.ifgoto:
            return Encoder.encode_ifgoto(file_name, parser.label)
        if parser.instruction_type == BranchingInstruction.label:
            return Encoder.encode_label(file_name, parser.label)

        if parser.instruction_type == FunctionInstruction.call:
            return Encoder.encode_call(parser.function_name, parser.n)
        if parser.instruction_type == FunctionInstruction.function:
            return Encoder.encode_function(parser.function_name, parser.n)
        if parser.instruction_type == FunctionInstruction.return_:
            return Encoder.encode_return()

        if parser.instruction_type == MemoryInstruction.push:
            return Encoder.encode_push(file_name, parser.segment, parser.i)

        if parser.instruction_type == MemoryInstruction.pop:
            return Encoder.encode_pop(file_name, parser.segment, parser.i)


if __name__ == '__main__':
    VMTranslator(sys.argv[1]).run()
