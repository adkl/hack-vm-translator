import re
from typing import Union

from constants import re_group_separator, arithmetic_instructions, data_segments, ArithmeticInstructionMapping, \
    MemoryInstructionMapping
from enumerations import ArithmeticInstruction, MemoryInstruction, FunctionInstruction, BranchingInstruction


class Parser:
    ARITHMETIC_PATTERN = re.compile(f'^({re_group_separator.join(arithmetic_instructions)})')
    MEMORY_PATTERN = re.compile('^(?P<stack_op>pop|push) '
                                f'(?P<segment>{re_group_separator.join(data_segments)}) '
                                '(?P<i>[0-9]+)')
    FUNCTION_PATTERN = re.compile('function (?P<name>.+) (?P<n>[0-9]+)')
    RETURN_PATTERN = re.compile('return')
    CALL_PATTERN = re.compile('call (?P<name>.+) (?P<n>[0-9]+)')
    BRANCHING_PATTERN = re.compile('(?P<cmd>goto|if-goto|label) (?P<label>.+)')

    def __init__(self, instruction: str):
        self._instruction_type = None
        self._segment = None
        self._i = None

        self._branching_cmd = None
        self._label = None

        self.instruction = instruction.strip()

        self._decode_instruction_type()

    @property
    def function_name(self):
        return self._function_name

    @property
    def n(self):
        return self._n

    @property
    def instruction_type(self) -> Union[ArithmeticInstruction, MemoryInstruction]:
        return self._instruction_type

    @property
    def i(self):
        return self._i

    @property
    def label(self):
        return self._label

    @property
    def segment(self):
        return self._segment

    def _decode_instruction_type(self):
        arithmetic_matched = self.ARITHMETIC_PATTERN.match(self.instruction)
        memory_matched = self.MEMORY_PATTERN.match(self.instruction)
        call_matched = self.CALL_PATTERN.match(self.instruction)
        function_matched = self.FUNCTION_PATTERN.match(self.instruction)
        return_matched = self.RETURN_PATTERN.match(self.instruction)
        branching_matched = self.BRANCHING_PATTERN.match(self.instruction)

        if arithmetic_matched:
            self._instruction_type = ArithmeticInstructionMapping[arithmetic_matched.group(0)]

        elif memory_matched:
            stack_op = memory_matched.group(self.MEMORY_PATTERN.groupindex['stack_op'])
            segment = memory_matched.group(self.MEMORY_PATTERN.groupindex['segment'])
            i = memory_matched.group(self.MEMORY_PATTERN.groupindex['i'])

            self._instruction_type = MemoryInstructionMapping[stack_op]
            self._segment = segment
            self._i = i

        elif call_matched:
            self._instruction_type = FunctionInstruction.call
            self._function_name = call_matched.group(self.CALL_PATTERN.groupindex['name'])
            self._n = call_matched.group(self.CALL_PATTERN.groupindex['n'])

        elif function_matched:
            self._instruction_type = FunctionInstruction.function
            self._function_name = function_matched.group(self.CALL_PATTERN.groupindex['name'])
            self._n = function_matched.group(self.CALL_PATTERN.groupindex['n'])

        elif return_matched:
            self._instruction_type = FunctionInstruction.return_

        elif branching_matched:
            cmd = branching_matched.group(self.BRANCHING_PATTERN.groupindex['cmd'])
            self._instruction_type = BranchingInstruction(cmd)

            self._label = branching_matched.group(self.BRANCHING_PATTERN.groupindex['label'])
