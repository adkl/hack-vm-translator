import re
from typing import Union

from src.constants import re_group_separator, arithmetic_instructions, data_segments, ArithmeticInstructionMapping, \
    MemoryInstructionMapping
from src.enumerations import ArithmeticInstruction, MemoryInstruction


class Parser:
    ARITHMETIC_PATTERN = re.compile(f'^({re_group_separator.join(arithmetic_instructions)})')
    MEMORY_PATTERN = re.compile('^(?P<stack_op>pop|push) '
                                f'(?P<segment>{re_group_separator.join(data_segments)}) '
                                '(?P<i>[0-9]+)')

    def __init__(self, instruction: str):
        self._instruction_type = None
        self._segment = None
        self._i = None

        self.instruction = instruction.strip()

        self._decode_instruction_type()

    @property
    def instruction_type(self) -> Union[ArithmeticInstruction, MemoryInstruction]:
        return self._instruction_type

    @property
    def i(self):
        return self._i

    @property
    def segment(self):
        return self._segment

    def _decode_instruction_type(self):
        arithmetic_matched = self.ARITHMETIC_PATTERN.match(self.instruction)
        memory_matched = self.MEMORY_PATTERN.match(self.instruction)

        if arithmetic_matched:
            self._instruction_type = ArithmeticInstructionMapping[arithmetic_matched.group(0)]

        elif memory_matched:
            stack_op = memory_matched.group(self.MEMORY_PATTERN.groupindex['stack_op'])
            segment = memory_matched.group(self.MEMORY_PATTERN.groupindex['segment'])
            i = memory_matched.group(self.MEMORY_PATTERN.groupindex['i'])

            self._instruction_type = MemoryInstructionMapping[stack_op]
            self._segment = segment
            self._i = i
