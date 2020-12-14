import math
import re
import sys
import time
from typing import Dict, List, Tuple

def main(*args):
    input_ = load_input('test' in args)
    start = time.time()
    print(part1(input_, 'test' in args))
    mid = time.time()
    print(f'Part 1 time: {mid - start}')
    print(part2(input_, 'test' in args))
    end = time.time()
    print(f'Part 2 time: {end - mid}')


def load_input(test: bool = False) -> Tuple[int, List[str]]:
    filename = f'{"test" * test}input.txt'
    with open(filename) as f:
        return [r.strip() for r in f.readlines()]


def part1(input_: List[str], test: bool = False) -> int:
    compy = Compy()
    for instruction in input_:
        compy.follow_instruction(instruction)
        if test:
            print(compy.mask)
            for k, v in compy.memory.items():
                print(f'{k}: {v}')
            print('-'*10)
    return compy.add_values()


def part2(input_: List[str], test: bool = False) -> int:
    compy = CompyTwo()
    for instruction in input_:
        compy.follow_instruction(instruction)
        if test:
            print(compy.mask)
            for k, v in compy.memory.items():
                print(f'{k}: {v}')
            print('-'*10)
    return compy.add_values()


class Compy:

    mask: Dict[int, str]
    memory: Dict[int, int]

    MEM_RE = r'mem\[(\d+)\] = (\d+)'

    def __init__(self):
        self.mask = {}
        self.memory = {}

    def follow_instruction(self, instruction: str) -> None:
        if instruction.startswith('mask'):
            new_mask = instruction[7:]
            self.update_mask(new_mask)
        else:
            groups = re.match(self.MEM_RE, instruction).groups()
            index, new_value = map(int, groups)
            self.update_memory(index, new_value)

    def update_mask(self, new_val: str) -> None:
        self.mask = {}
        for i, b in enumerate(new_val[::-1]):
            if b in ('0', '1'):
                self.mask[i] = b

    def update_memory(self, index: int, new_val: int) -> None:
        masked_value = self.apply_mask_to_value(new_val)
        self.memory[index] = masked_value

    def apply_mask_to_value(self, value: int) -> int:
        bits = list(bin(value)[:1:-1].ljust(36, '0'))
        for k, b in self.mask.items():
            bits[k] = b
        str_bits = ''.join(bits[::-1])
        masked_value = int(str_bits, base=2)
        return masked_value

    def add_values(self) -> int:
        return sum(self.memory.values())


class CompyTwo(Compy):

    def update_mask(self, new_val: str) -> None:
        self.mask = {}
        for i, b in enumerate(new_val[::-1]):
            self.mask[i] = b

    def update_memory(self, index: int, new_val: int) -> None:
        masked_indices = self.apply_mask_to_index(index)
        for masked_index in masked_indices:
            self.memory[masked_index] = new_val


    def apply_mask_to_index(self, index: int) -> None:
        bits_list = [list(bin(index)[:1:-1].ljust(36, '0'))]
        for k, b in self.mask.items():
            if b == '0':
                pass
            elif b == '1':
                for bits in bits_list:
                    bits[k] = b
            else:
                bits_list = [
                    bits[:k] + [newb] + bits[k+1:]
                    for newb in ('0', '1')
                    for bits in bits_list
                ]
        masked_indices_list = [
            int(''.join(bits[::-1]), base=2)
            for bits in bits_list
        ]
        return masked_indices_list

if __name__ == '__main__':
    main(*sys.argv)
