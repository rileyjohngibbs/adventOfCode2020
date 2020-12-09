import re
from typing import List, Optional, Set, Tuple, Type, TypeVar, Union, cast


def main():
    input_ = load_input()
    print(part1(input_))
    print(part2(input_))


def load_input():
    with open('input.txt') as f:
        return [r.strip() for r in f.readlines()]


def part1(input_: list):
    instructions = [
        [*cast(re.Match, re.match(r'(.{3}) (.*)', row)).groups(), 0]
        for row in input_
    ]
    _, acc = run_to_loop(instructions)
    return acc


def run_to_loop(instructions):
    instructions = [i[:] for i in instructions]
    acc, index = 0, 0
    while index < len(instructions) and instructions[index][-1] == 0:
        op = instructions[index][0]
        instructions[index][-1] += 1
        if op == 'nop':
            index += 1
        elif op == 'acc':
            acc += int(instructions[index][1])
            index += 1
        else:
            index += int(instructions[index][1])
    looped = index < len(instructions)
    return looped, acc


I = TypeVar('I', bound='Instruction')


class Instruction:

    def __init__(self, operation: str, value: Union[str, int]):
        self._operation = operation
        self.value = int(value)
        self.flipped = False

    @classmethod
    def from_string(cls: Type[I], string: str) -> I:
        match = re.match(r'(.{3}) (.*)', string)
        if match is None:
            raise ValueError()
        actual_match: re.Match = match
        return cls(*actual_match.groups())

    @property
    def operation(self) -> str:
        if self.flipped:
            op = {'jmp': 'nop', 'nop': 'jmp', 'acc': 'acc'}[self._operation]
        else:
            op = self._operation
        return op

    def index_delta(self, override_op: Optional[str] = None) -> int:
        operation = override_op if override_op is not None else self.operation
        return self.value if operation == 'jmp' else 1

    def flipped_index_delta(self) -> int:
        if self.operation == 'jmp':
            override_op = 'nop'
        elif self.operation == 'nop':
            override_op = 'jmp'
        else:
            override_op = self.operation
        return self.index_delta(override_op)

    def flip(self):
        self.flipped = not self.flipped

    def acc(self) -> int:
        return self.value * (self.operation == 'acc')


class ProgramLine:

    index: int
    instruction: Instruction
    pre: List[int]
    fpre: List[int]

    def __init__(self, index: int, instruction: Instruction):
        self.index = index
        self.instruction = instruction
        self.pre = []
        self.fpre = []


class Program:

    def __init__(self, instructions: List[Instruction]):
        self.program_lines = [
            ProgramLine(index, instruction)
            for index, instruction in enumerate(instructions)
        ]
        self.exit = ProgramLine(len(self.program_lines), Instruction('nop', 0))
        for program_line in self.program_lines:
            move_index = program_line.instruction.index_delta() + program_line.index
            if move_index >= self.exit.index:
                self.exit.pre.append(program_line.index)
            else:
                self.program_lines[move_index].pre.append(program_line.index)
            fmove_index = program_line.instruction.flipped_index_delta() + program_line.index
            if fmove_index >= self.exit.index:
                self.exit.fpre.append(program_line.index)
            else:
                self.program_lines[fmove_index].fpre.append(program_line.index)

    def run_program(self, flip: Optional[int] = None) -> Tuple[Set[int], int]:
        node_set = set()
        acc, index = 0, 0
        while index < self.exit.index and index not in node_set:
            node_set.add(index)
            acc += self.program_lines[index].instruction.acc()
            index = index + self.program_lines[index].instruction.index_delta()
        node_set.add(index)
        return node_set, acc

    def expand_boundary(self, boundary: List[ProgramLine]) -> List[ProgramLine]:
        return [self.program_lines[pre] for program_line in boundary for pre in program_line.pre]


def part2(input_: list):
    instructions = [Instruction.from_string(row) for row in input_]
    program = Program(instructions)
    loop, _ = program.run_program()
    boundary: List[ProgramLine] = [program.exit]
    index_to_flip = flipper(loop, boundary)
    while index_to_flip is None:
        boundary = program.expand_boundary(boundary)
        index_to_flip = flipper(loop, boundary)
    program.program_lines[index_to_flip].instruction.flip()
    _, acc = program.run_program()
    return acc


def flipper(loop: set, boundary: List[ProgramLine]) -> Optional[int]:
    return next((
        fpre
        for node in boundary
        for fpre in node.fpre
        if fpre in loop
    ), None)



if __name__ == '__main__':
    main()
